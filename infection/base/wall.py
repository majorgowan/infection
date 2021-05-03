"""
-------------------------------------------------------
Base class for wall
-------------------------------------------------------
Author:  Mark Fruman
Email:   majorgowan@yahoo.com
-------------------------------------------------------
"""
from pprint import pformat


class Wall:
    """
    Class representing a temperature field

    Parameters
    ----------
    orient : str
        either "h" or "v"
    x : float or list
        x coordinate(s) of wall
    y : float or list
        y coordinate(s) of wall
    """
    def __init__(self, orient, x, y):
        self.orient = orient
        self.x = x
        self.y = y

    def bounce(self, pos1, pos2):
        """
        Determine if the line segment connecting pos1 and pos2 intersects
        the wall; if intersects, return the coordinates of the new
        landing point

        Parameters
        ----------
        pos1 : list[float]
            [x, y] coordinates of starting point
        pos2 : list[float]
            [x, y] coordinates of end point

        Returns
        -------
        list or None
        """
        if self.orient == "h":
            # test if segment is above or below wall
            if min(pos1[1], pos2[1]) > self.y:
                return None
            if max(pos1[1], pos2[1]) < self.y:
                return None
            # test if segment is fully left or right of the wall
            if max(pos1[0], pos2[0]) < self.x[0]:
                return None
            if min(pos1[0], pos2[0]) > self.x[1]:
                return None
            # exclude case of horizontal displacement
            if pos1[1] != pos2[1]:
                # find intersection point
                slope = (pos2[0] - pos1[0]) / (pos2[1] - pos1[1])
                xwall = pos1[0] + slope * (self.y - pos1[1])
                # check if intersection point is outside limits of wall
                if not self.x[0] <= xwall <= self.x[1]:
                    return None
            # find new landing point
            return [pos2[0], 2 * self.y - pos2[1]]
        else:
            # wall is vertical
            # test if segment is left or right of wall
            if min(pos1[0], pos2[0]) > self.x:
                return None
            if max(pos1[0], pos2[0]) < self.x:
                return None
            # test if segment is fully above or below the wall
            if max(pos1[1], pos2[1]) < self.y[0]:
                return None
            if min(pos1[1], pos2[1]) > self.y[1]:
                return None
            # exclude case of vertical displacement
            if pos1[0] != pos2[0]:
                # find intersection point
                slope = (pos2[1] - pos1[1]) / (pos2[0] - pos1[0])
                ywall = pos1[1] + slope * (self.x - pos1[0])
                # check if intersection point is outside limits of wall
                if not self.y[0] <= ywall <= self.y[1]:
                    return None
            # find new landing point
            return [2 * self.x - pos2[0], pos2[1]]

    def __repr__(self):
        return pformat(
            {
                "orient": self.orient,
                "x": self.x,
                "y": self.y
            }
        )
