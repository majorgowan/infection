"""
-------------------------------------------------------
Base class for person in population
-------------------------------------------------------
Author:  Mark Fruman
Email:   majorgowan@yahoo.com
-------------------------------------------------------
"""
import numpy as np
from pprint import pformat


class Person:
    """
    Class representing a person in the population

    Parameters
    ----------
    x : float
        x-coordinate of initial position
    y : float
        y-coordinate of initial position
    mobility : float
        initial speed when fully healthy
    direction : float
        angle to horizontal of initial velocity
    hypochondria : float
        extent to which person accelerates away from hotspots
    immunity : float
        initial level of immunity
    """
    def __init__(self, x, y, mobility, direction,
                 hypochondria, immunity):
        self.x = x
        self.y = y
        self.dx = np.cos(direction)
        self.dy = np.sin(direction)
        self.mobility = mobility
        self.hypochondria = hypochondria
        self.health_ = 1
        self.incubation_ = 0
        self.severity_ = 0
        self.immunity = immunity
        self.immunity_ = 0
        self.infected = False
        self.incubating = False
        self.healing_rate_ = None

    @property
    def health(self):
        return self.health_

    @property
    def speed(self):
        return self.mobility * self.health

    @property
    def velocity(self):
        vx = self.dx * self.speed
        vy = self.dy * self.speed
        return np.array([vx, vy])

    @staticmethod
    def get_next(array):
        """
        Return index of first True value in array

        Parameters
        ----------
        array : 1-d numpy.array of bool
            array to parse

        Returns
        -------
        int
        """
        for ii, b in enumerate(array):
            if b:
                return ii
        return len(array)

    def get_temperature(self, temperature):
        """
        Get local temperature at current position of person

        Parameters
        ----------
        temperature : Temperature object
            with keys "xx", "yy", and "temperature"

        Returns
        -------
        float
        """
        nextx = self.get_next(temperature.xx[0, :] >= self.x)
        nexty = self.get_next(temperature.yy[:, 0] >= self.y)
        return temperature.temperature[nexty, nextx]

    def get_temperature_gradient(self, temperature):
        """
        Compute (negative) gradient of temperature field, i.e. direction
        of maximum _decrease_ of temperature

        Parameters
        ----------
        temperature : Temperature object
            with keys "xx", "yy", and "temperature"

        Returns
        -------
        gradx : float
            x-coordinate of gradient
        grady : float
            y-coordinate of gradient
        """
        nextx = self.get_next(temperature.xx[0, :] >= self.x)
        nexty = self.get_next(temperature.yy[:, 0] >= self.y)
        return (temperature.gradx[nexty, nextx],
                temperature.grady[nexty, nextx])

    def immune(self, temperature):
        """
        Return True if the person is immune (with buffer) given local
        temperature.

        Parameters
        ----------
        temperature : Temperature object
            temperature field

        Returns
        -------
        bool
        """
        return self.immunity_ > self.get_temperature(temperature) + 0.1

    def update_health(self):
        """
        Update person's health
            - if infected and incubating, count down incubation time
            - if infected and sick, increment health (recover)
            - if not infected, do nothing
        """
        if not self.infected:
            return
        if not self.incubating:
            # heal
            self.health_ += self.healing_rate_ * (1 - self.health_)
            if self.health_ >= 0.9:
                # fully healed
                self.immunity_ = self.immunity
                self.health_ = 1
                self.infected = False
        else:
            # still in incubation period
            if self.incubation_ < 0.01:
                self.incubating = False
                self.health_ = 1.0 - self.severity_
            else:
                # count down incubation
                self.incubation_ -= 1

        # wear off immunity
        if self.immunity_ > 0.02:
            self.immunity_ -= 0.02

    def move(self, walls):
        """
        Move person based on current velocity and range

        Parameters
        ----------
        walls : list
            descriptions of horizontal and vertical walls at which person
            reflects
        """
        vx, vy = self.velocity

        pos1 = [self.x, self.y]
        pos2 = [self.x + vx, self.y + vy]

        # check if displacement hits a wall (two passes)
        for _ in range(2):
            for wall in walls:
                landing = wall.bounce(pos1, pos2)
                if landing is not None:
                    pos2 = landing
                    # flip the velocity direction
                    if wall.orient == "h":
                        self.dy *= -1
                    else:
                        # vertical wall
                        self.dx *= -1

        # apply periodic bc at open boundary
        pos2[0] = pos2[0] % 1
        pos2[1] = pos2[1] % 1

        self.x, self.y = pos2

    def accelerate(self, temperature):
        """
        Accelerate away from hotspots

        Parameters
        ----------
        temperature : Temperature object
            temperature field
        """
        if not self.infected:
            dx, dy = self.get_temperature_gradient(temperature)
            self.dx += self.hypochondria * dx
            self.dy += self.hypochondria * dy

    def infect(self, incubation, healing_rate, severity, temperature=None):
        """
        (Try to) infect this person if immunity is weaker than local
        temperature is hot.

        Parameters
        ----------
        incubation : int
            time before the person will become ill if infected
        healing_rate : float
            rate of recovery if infected
        severity : float
            initial severity of disease if infected
        temperature : Temperature object
            temperature field
        """
        if temperature is None:
            temp0 = 1
        else:
            temp0 = self.get_temperature(temperature)
        if np.random.random() < severity * (temp0 - self.immunity_):
            self.severity_ = max(1.0, severity)
            self.healing_rate_ = healing_rate
            self.incubation_ = incubation
            self.incubating = True
            self.infected = True

    def __repr__(self):
        return pformat({
            "x": self.x,
            "y": self.y,
            "dx": self.dx,
            "dy": self.dy,
            "mobility": self.mobility,
            "hypochondria": self.hypochondria,
            "health": self.health_,
            "incubation": self.incubation_,
            "severity": self.severity_,
            "immunity": self.immunity_,
            "infected": self.infected
        })

    @staticmethod
    def positions(people):
        x = [person.x for person in people]
        y = [person.y for person in people]
        return np.array([x, y]).T

    @staticmethod
    def velocities(people):
        dx = [np.cos(person.direction) * person.speed
              for person in people]
        dy = [np.sin(person.direction) * person.speed
              for person in people]
        return np.array([dx, dy]).T

    @staticmethod
    def healths(people):
        return np.array([person.health for person in people])

    @staticmethod
    def immunities(people):
        return np.array([person.immunity_ for person in people])

    @staticmethod
    def infected_people(people):
        return [person for person in people if person.infected]

    @staticmethod
    def immune_people(people, temperature):
        return [person for person in people if person.immune(temperature)]

    @staticmethod
    def non_immune_people(people, temperature):
        return [person for person in people if not person.immune(temperature)]

    @staticmethod
    def susceptible_people(people, temperature):
        return [person for person in people
                if not person.immune(temperature)
                and not person.infected]
