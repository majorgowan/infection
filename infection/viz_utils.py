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
import matplotlib.cm
import matplotlib.colors
from infection.base import Person

plt.style.use("bmh")


def init_frame(infection0, figsize=None):
    """
    Initialize figure for plotting animation frames

    Parameters
    ----------
    infection0 : Infection object
        initialized simulation object
    figsize : tuple
        size of figure canvas

    Returns
    -------
    matplotlib.pyplot.Figure
        main figure object
    matplotlib.collections.PathCollection
        scatter plot data
    matplotlib.contour.QuadContourSet
        contour plot data
    """
    if figsize is None:
        figsize = (12, 10)

    fig = plt.figure(figsize=figsize)

    temperature = infection0.temperature_
    people = infection0.people_
    walls = infection0.walls_

    ax = fig.gca()

    amplitude = (temperature.intensity / np.sqrt(2 * np.pi)
                 / temperature.hotspot_radius)

    levels = np.linspace(0, 4 * amplitude, 40)

    contour_cmap = matplotlib.cm.get_cmap("Reds")
    contour_norm = matplotlib.colors.Normalize(vmin=-0.2,
                                               vmax=1.2 * 4 * amplitude)

    # plot the temperature field
    qcs = ax.contourf(temperature.xx, temperature.yy, temperature.temperature,
                      levels=levels, alpha=0.5, cmap=contour_cmap,
                      norm=contour_norm, extend="max")

    point_size = int(10000 / len(people))
    wall_width = int(np.sqrt(point_size))

    # draw walls
    for wall in walls:
        if wall.orient == "h":
            ax.hlines(wall.y, *wall.x, linewidth=wall_width, color="k")
        else:
            ax.vlines(wall.x, *wall.y, linewidth=wall_width, color="k")

    scatter_cmap = matplotlib.cm.get_cmap("copper")
    scatter_norm = matplotlib.colors.Normalize(vmin=-0.2, vmax=1.2)

    # plot the people
    healths = np.array([scatter_cmap(scatter_norm(p.health))
                        for p in people])
    positions = Person.positions(people)
    scatter = ax.scatter(positions[:, 0], positions[:, 1],
                         s=point_size, c=healths, marker="o",
                         cmap=scatter_cmap, norm=scatter_norm)

    ax.grid(None)

    ax.set_xticks([])
    ax.set_yticks([])

    ax.set_ylim((0, 1))
    ax.set_xlim((0, 1))

    return fig, scatter, qcs


def update_frame(fig, scatter, qcs, infection0):
    """
    Plot current state of people and temperature in figure object

    Parameters
    ----------
    fig : matplotlib.pyplot.Figure object
        figure in which to plot current frame
    scatter : matplotlib.collections.PathCollection
        scatter plot data
    qcs: matplotlib.contour.QuadContourSet
        contour plot data
    infection0 : Infection object
        with updated state

    Returns
    -------
    matplotlib.pyplot.Figure
        main figure object
    matplotlib.collections.PathCollection
        scatter plot data
    matplotlib.contour.QuadContourSet
        contour plot data
    """
    temperature = infection0.temperature_
    people = infection0.people_

    ax = fig.gca()

    # clear existing contours
    for coll in qcs.collections:
        coll.remove()

    # plot new temperature field
    amplitude = (temperature.intensity / np.sqrt(2 * np.pi)
                 / temperature.hotspot_radius)

    levels = np.linspace(0, 4 * amplitude, 40)

    vmax = 1.2 * 4 * amplitude
    contour_cmap = matplotlib.cm.get_cmap("Reds").copy()
    contour_norm = matplotlib.colors.Normalize(vmin=-0.2, vmax=vmax)
    contour_cmap.set_over(color="orchid")

    # plot the new temperature field
    qcs = ax.contourf(temperature.xx, temperature.yy, temperature.temperature,
                      levels=levels, alpha=0.5, cmap=contour_cmap,
                      norm=contour_norm, extend="max")

    # update people positions
    scatter_cmap = matplotlib.cm.get_cmap("copper")
    scatter_norm = matplotlib.colors.Normalize(vmin=-0.2, vmax=1.2)
    scatter_cmap2 = matplotlib.cm.get_cmap("Blues")
    scatter_norm2 = matplotlib.colors.Normalize(vmin=-0.2, vmax=2.5)

    # colour the people
    new_colours = np.array([scatter_cmap(scatter_norm(p.health))
                            if not p.immune(temperature)
                            else scatter_cmap2(scatter_norm2(p.immunity_))
                            for p in people])
    scatter.set_facecolor(new_colours)

    # reposition the people
    positions = Person.positions(people)
    scatter.set_offsets(positions)

    return fig, scatter, qcs
