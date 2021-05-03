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
    n_points : int
        number of points in each direction
    spatial_decay : float
        gaussian width of hotspot surrounding infected person
    linger_decay : float
        fraction of current field to preserve on next time-step
        (temperature at next time is weighted average of current field
        and field due to new positions of people)
    intensity : float
        amplitude of temperature perturbation around infected person
    """
    def __init__(self, n_points, spatial_decay=0.1, linger_decay=0,
                 intensity=1):
        self.n_points = n_points
        self.spatial_decay = spatial_decay
        self.linger_decay = linger_decay
        self.intensity = intensity

        buffer_points = 1
        buffer_width = (buffer_points / n_points)
        xx, yy = np.meshgrid(np.linspace(-1 * buffer_width,
                                         1 + buffer_width, n_points),
                             np.linspace(-1 * buffer_width,
                                         1 + buffer_width, n_points))

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
        amplitude = self.intensity / np.sqrt(2 * np.pi) / self.spatial_decay

        temp0 = np.zeros(shape=self.temperature.shape)
        for person in people:
            if person.infected:
                dist2 = (self.xx - person.x) ** 2 + (self.yy - person.y) ** 2
                temp0 += (amplitude
                          * np.exp(-0.5 * dist2 / self.spatial_decay ** 2))
        self.temperature = self.linger_decay * self.temperature + temp0

        # compute gradient
        gradx = -0.5 * (self.temperature[:, 2:]
                        - self.temperature[:, :-2]) / self.dx
        grady = -0.5 * (self.temperature[2:, :]
                        - self.temperature[:-2, :]) / self.dy
        self.gradx[:, 1:-1] = gradx
        self.grady[1:-1, :] = grady

    def __repr__(self):
        return pformat(
            {
                "n_points": self.n_points,
                "max_temperature": self.temperature.max(),
                "mean_temperature": self.temperature.mean(),
                "max_gradient": max(np.sqrt(self.gradx ** 2
                                            + self.grady ** 2))
            }
        )
