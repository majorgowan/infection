"""
-------------------------------------------------------
Base class for temperature field
-------------------------------------------------------
Author:  Mark Fruman
Email:   majorgowan@yahoo.com
-------------------------------------------------------
"""
import numpy as np
from pprint import pformat


class Temperature:
    """
    Class representing a temperature field

    Parameters
    ----------
    gridsize : int
        number of points in each direction
    hotspot_radius : float
        gaussian width of hotspot surrounding infected person
    linger : float
        fraction of current field to preserve on next time-step
        (temperature at next time is weighted average of current field
        and field due to new positions of people)
    intensity : float
        amplitude of temperature perturbation around infected person
    """
    def __init__(self, gridsize, hotspot_radius=0.1, linger=0,
                 intensity=1):
        self.gridsize = gridsize
        self.hotspot_radius = hotspot_radius
        self.linger = linger
        self.intensity = intensity

        buffer_points = 1
        buffer_width = (buffer_points / gridsize)
        xx, yy = np.meshgrid(np.linspace(-1 * buffer_width,
                                         1 + buffer_width, gridsize),
                             np.linspace(-1 * buffer_width,
                                         1 + buffer_width, gridsize))

        self.xx = xx
        self.yy = yy
        self.dx = xx[0, 1] - xx[0, 0]
        self.dy = yy[1, 0] - yy[0, 0]
        self.temperature = np.zeros(shape=xx.shape)
        self.gradx = np.zeros(shape=xx.shape)
        self.grady = np.zeros(shape=xx.shape)

    def update(self, people):
        """
        Update field based on positions of people

        Parameters
        ----------
        people : People objects
            determine new temperature field after update
        """
        amplitude = self.intensity / np.sqrt(2 * np.pi) / self.hotspot_radius

        temp0 = np.zeros(shape=self.temperature.shape)
        for person in people:
            if person.infected:
                dist2 = (self.xx - person.x) ** 2 + (self.yy - person.y) ** 2
                temp0 += (amplitude
                          * np.exp(-0.5 * dist2 / self.hotspot_radius ** 2))
        self.temperature = self.linger * self.temperature + temp0

        # compute gradient
        gradx = -0.5 * (self.temperature[:, 2:]
                        - self.temperature[:, :-2]) / self.dx
        grady = -0.5 * (self.temperature[2:, :]
                        - self.temperature[:-2, :]) / self.dy
        self.gradx[:, 1:-1] = gradx
        self.grady[1:-1, :] = grady

    def __repr__(self):
        max_temperature = self.temperature.max(initial=0.0)
        mean_temperature = self.temperature.mean()
        max_gradient = (np.sqrt(self.gradx ** 2 + self.grady ** 2)).max()

        return pformat(
            {
                "gridsize": self.gridsize,
                "max_temperature": f"{max_temperature:.3f}",
                "mean_temperature": f"{mean_temperature:.3f}",
                "max_gradient": f"{max_gradient:.3f}"
            }
        )
