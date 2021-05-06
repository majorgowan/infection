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

    amplitude = (temperature.intensity / (4 * np.pi)
                 / temperature.hotspot_radius)
    density_factor = (1 +
                      4 * np.pi * len(people) * temperature.hotspot_radius ** 2)

    levels = np.linspace(0, density_factor * amplitude, 40)

    vmax = 1.2 * density_factor * amplitude
    contour_cmap = matplotlib.cm.get_cmap("Reds").copy()
    contour_norm = matplotlib.colors.Normalize(vmin=0, vmax=vmax)
    contour_cmap.set_over(color="darkred")

    # plot the temperature field
    qcs = ax.contourf(temperature.xx, temperature.yy, temperature.temperature,
                      levels=levels, cmap=contour_cmap,
                      norm=contour_norm, extend="max")
    # hide contours
    for coll in qcs.collections:
        coll.set_edgecolor("face")

    point_size = int(10000 / len(people))
    wall_width = int(np.sqrt(point_size))

    # draw walls
    for wall in walls:
        if wall.orient == "h":
            ax.hlines(wall.y, *wall.x, linewidth=wall_width, color="k",
                      zorder=5)
        else:
            ax.vlines(wall.x, *wall.y, linewidth=wall_width, color="k",
                      zorder=5)

    scatter_cmap = matplotlib.cm.get_cmap("copper")
    scatter_norm = matplotlib.colors.Normalize(vmin=-0.2, vmax=1.2)

    # plot the people
    healths = np.array([scatter_cmap(scatter_norm(p.health))
                        for p in people])
    positions = Person.positions(people)
    scatter = ax.scatter(positions[:, 0], positions[:, 1],
                         zorder=4, s=point_size, c=healths, marker="o",
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
    amplitude = (temperature.intensity / (4 * np.pi)
                 / temperature.hotspot_radius)
    density_factor = (1 +
                      4 * np.pi * len(people) * temperature.hotspot_radius ** 2)
    levels = np.linspace(0, density_factor * amplitude, 40)

    vmax = 1.2 * density_factor * amplitude
    contour_cmap = matplotlib.cm.get_cmap("Reds").copy()
    contour_norm = matplotlib.colors.Normalize(vmin=0, vmax=vmax)
    contour_cmap.set_over(color="darkred")

    # plot the new temperature field
    qcs = ax.contourf(temperature.xx, temperature.yy, temperature.temperature,
                      levels=levels, cmap=contour_cmap,
                      norm=contour_norm, extend="max")
    # hide contours
    for coll in qcs.collections:
        coll.set_edgecolor("face")

    # update people positions
    scatter_cmap = matplotlib.cm.get_cmap("copper")
    scatter_norm = matplotlib.colors.Normalize(vmin=-0.2, vmax=1.2)
    scatter_cmap2 = matplotlib.cm.get_cmap("Blues")
    immunity_max = max([p.full_immunity for p in people])
    scatter_norm2 = matplotlib.colors.Normalize(vmin=-1, vmax=immunity_max)

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
