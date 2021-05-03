"""
-------------------------------------------------------
Utils for visualizing simulation
-------------------------------------------------------
Author:  Mark Fruman
Email:   majorgowan@yahoo.com
-------------------------------------------------------
"""
import numpy as np
import matplotlib.pyplot as plt
from base import Person

plt.style.use("bmh")


def plot_init():
    """
    Initialize figure for plotting animation frames

    Returns
    -------
    matplotlib.pyplot.Figure object
    """
    fig = plt.figure(figsize=(12, 10))
    return fig


def plot_frame(fig, people, temperature):
    """
    Plot current state of people and temperature in figure object

    Parameters
    ----------
    fig : matplotlib.pyplot.Figure object
        figure in which to plot current frame
    people : list
        Person objects to visualize
    temperature : Temperature object
        temperature field to visualize
    """
    ax = fig.gca()

    amplitude = (temperature.intensity / np.sqrt(2 * np.pi)
                 / temperature.spatial_decay)

    levels = np.linspace(0, 3 * amplitude, 40)

    # plot the temperature field
    qcf = ax.contourf(temperature.xx, temperature.yy,
                      temperature.temperature,
                      levels=levels, alpha=0.5, cmap="Reds",
                      extend="max")

    # plot the immune people
    immune_people = Person.immune_people(people, temperature)
    positions = Person.positions(immune_people)
    immunities = Person.immunities(immune_people)
    ax.scatter(positions[:, 0], positions[:, 1],
               s=100, c=immunities, marker="o",
               cmap="Blues", vmin=-0.2, vmax=1)

    # plot the infected and susceptible people
    susceptible_people = Person.susceptible_people(people, temperature)
    healths = Person.healths(susceptible_people)
    positions = Person.positions(susceptible_people)
    ax.scatter(positions[:, 0], positions[:, 1],
               s=100, c=healths, marker="o",
               vmin=-0.2, vmax=1.5, cmap="copper")

    # plot speeds
    for person in people:
        ax.arrow(x=person.x,
                 y=person.y,
                 dx=person.velocity[0],
                 dy=person.velocity[1],
                 head_width=0.01, color="blue", alpha=0.3)

    ax.grid(None)

    ax.set_xticks([])
    ax.set_yticks([])

    ax.set_ylim((0, 1))
    ax.set_xlim((0, 1))
