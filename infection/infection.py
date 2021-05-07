import numpy as np
from pprint import pformat
from infection import Person, Temperature, Wall
from infection.utils import supdate, random_choice


class Infection:
    def __init__(self, **kwargs):
        configuration = {
            "n_people": 100,
            "gridsize": 200,
            "initial_infection_fraction": 0.05,
            "infection": {
                "infectiousness": 0.1,
                "linger": 0.1,
                "hotspot_radius": 0.04,
                "incubation": 0,
                "immunity": 2,
                "healing_rate": 0.1,
                "severity": 1,
                "seasonality": 0.2
            },
            "mobility": {
                "speed": 0.02,
                "hypochondria": 0.05,
                "walls": [
                    {"orient": "h",
                     "x": [0, 1],
                     "y": 0},
                    {"orient": "h",
                     "x": [0, 1],
                     "y": 1},
                    {"orient": "v",
                     "x": 0,
                     "y": [0, 1]},
                    {"orient": "v",
                     "x": 1,
                     "y": [0, 1]}
                ]
            }
        }
        supdate(configuration, kwargs)
        self.configuration = configuration
        # build walls
        self.walls_ = []
        self.day_ = 0
        self.people_ = []
        self.temperature_ = None
        self.infections_ = []
        # set walls
        for wall_config in configuration["mobility"]["walls"]:
            self.walls_.append(Wall(**wall_config))

    def initialize_people(self):
        """
        Initialize the people in the simulation
        """
        n_people = self["n_people"]
        initial_infection_fraction = self["initial_infection_fraction"]
        mobility = self["mobility"]
        infect0 = self["infection"]

        # generate initial positions and speeds for people
        positions = np.random.random(size=(n_people, 2))
        speeds = random_choice(mobility["speed"], size=n_people)
        directions = 2 * np.pi * np.random.random(size=n_people)

        self.people_ = []
        for position, speed, direction in zip(positions, speeds, directions):
            immunity = random_choice(infect0["immunity"])
            hypochondria = random_choice(mobility["hypochondria"])
            self.people_.append(Person(x=position[0], y=position[1],
                                       mobility=speed, direction=direction,
                                       hypochondria=hypochondria,
                                       immunity=immunity))

        # randomly pick the infected
        n_infected = int(initial_infection_fraction * n_people)
        infected = np.random.choice(a=np.arange(n_people),
                                    size=n_infected)

        for inf0 in infected:
            incubation = random_choice(infect0["incubation"])
            severity = random_choice(infect0["severity"])
            healing_rate = random_choice(infect0["healing_rate"])
            self.people_[inf0].infect(incubation=incubation,
                                      healing_rate=healing_rate,
                                      severity=severity)

    def initialize_temperature(self):
        """
        Initialize the temperature object based on current configuration
        """
        hotspot_radius = self["infection"]["hotspot_radius"]
        linger = self["infection"]["linger"]
        infectiousness = self["infection"]["infectiousness"]

        self.temperature_ = Temperature(
            gridsize=self.configuration["gridsize"],
            hotspot_radius=hotspot_radius,
            linger=linger,
            intensity=infectiousness
        )

    def update_people(self):
        """
        Update the movement and health of the people
        """
        infect0 = self["infection"]
        infectiousness = infect0["infectiousness"]
        seasonality = infect0["seasonality"]

        if seasonality > 0:
            infectiousness = (infectiousness
                              * (1 + seasonality * np.cos(2 * np.pi
                                                          * self.day_ / 365)))

        # update people's health
        for person in self.people_:
            person.update_health()

        # infect new people
        for person in Person.susceptible_people(self.people_,
                                                self.temperature_):
            if np.random.random() < infectiousness:
                incubation = random_choice(infect0["incubation"])
                severity = random_choice(infect0["severity"])
                healing_rate = random_choice(infect0["healing_rate"])
                result = person.infect(incubation=incubation,
                                       healing_rate=healing_rate,
                                       severity=severity,
                                       temperature=self.temperature_)
                if result is not None:
                    # log the infection event
                    result["day"] = self.day_
                    self.infections_.append(result)

        # update people movement
        for person in self.people_:
            person.accelerate(self.temperature_)
        for person in self.people_:
            person.move(self.walls_)

    def initialize_all(self, random_seed=None):
        """
        Parameters
        ----------
        random_seed : int
            seed for initializing random generator
        """
        if random_seed is not None:
            np.random.seed(random_seed)

        self.initialize_people()
        self.initialize_temperature()
        return self

    def run(self, steps):
        """
        Run the simulation

        Parameters
        ----------
        steps : int
            number of steps to run

        Returns
        -------
        generator
        """
        if self.temperature_ is None:
            # initialize people and temperature
            self.initialize_all()

        for _ in range(steps):
            self.day_ += 1
            self.update_people()
            self.temperature_.update(self.people_)
            yield (self.day_,
                   len(Person.infected_people(self.people_)),
                   len(Person.immune_people(self.people_,
                                            self.temperature_)))

    def __getitem__(self, item):
        return self.configuration.get(item, None)

    def configure(self, update):
        supdate(self.configuration, update)
        # reset walls
        self.walls_ = []
        for wall_config in self.configuration["mobility"]["walls"]:
            self.walls_.append(Wall(**wall_config))
        return self

    def __repr__(self):
        return pformat({
            **self.configuration,
            **{
                "state": {
                    "day": self.day_,
                    "temperature": self.temperature_,
                    "n_infected": len(Person.infected_people(self.people_)),
                    "n_immune": len(Person.immune_people(self.people_,
                                                         self.temperature_))
                }
            }
        })
