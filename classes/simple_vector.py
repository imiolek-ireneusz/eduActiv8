# -*- coding: utf-8 -*-

import math


class Vector2(object):
    def __init__(self, x=0., y=0.):
        if hasattr(x, "__getitem__"):
            x, y = x
            self._v = [float(x), float(y)]
        else:
            self._v = [float(x), float(y)]

    def __str__(self):
        return "(%s, %s)" % (self._v[0], self._v[1])

    def __getitem__(self, index):
        """Gets a component as though the vector were a list."""
        try:
            return self._v[index]
        except IndexError:
            pass
            # raise IndexError, "There are 2 values in this object, index should be 0 or 1"

    def __setitem__(self, index, value):
        """Sets a component as though the vector were a list."""
        try:
            self._v[index] = 1.0 * value
        except IndexError:
            pass
            # raise IndexError, "There are 2 values in this object, index should be 0 or 1!"
        except TypeError:
            pass
            # raise TypeError, "Must be a number"

    @staticmethod
    def from_points(P1, P2):
        return Vector2(P2[0] - P1[0], P2[1] - P1[1])

    @classmethod
    def from_floats(cls, x, y):
        vec = cls.__new__(cls, object)
        vec._v = [x, y]
        return vec

    @classmethod
    def dot_prod(cls, v1, v2):
        dot = v1[0] * v2[0] + v1[1] * v2[1]
        return dot

    @classmethod
    def scale(cls, scalar, v):
        vec = cls.__new__(cls, object)
        vec._v = [scalar * v[0], scalar * v[1]]
        return vec

    def get_magnitude(self):
        return math.sqrt(self._v[0] ** 2 + self._v[1] ** 2)

    def normalize(self):
        magnitude = self.get_magnitude()
        if magnitude != 0:
            self._v[0] /= magnitude
            self._v[1] /= magnitude
        else:
            self._v = [0., 0.]

    def __iter__(self):
        return iter(self._v[:])

    def __len__(self):
        return 2

    def __add__(self, rhs):
        return Vector2(self._v[0] + rhs._v[0], self._v[1] + rhs._v[1])

    def __sub__(self, rhs):
        return Vector2(self._v[0] - rhs._v[0], self._v[1] - rhs._v[1])

    def __neg__(self):
        return Vector2(-self._v[0], -self._v[1])

    """
    def __mul__(self, scalar):
        return Vector2(self._v[0] * scalar, self._v[1] * scalar)
    """

    def __mul__(self, rhs):
        """Return the result of multiplying this vector with a scalar or a vector-list object."""
        x, y = self._v
        if hasattr(rhs, "__getitem__"):
            xx, yy = rhs
            return Vector2.from_floats(x * xx, y * yy)
        else:
            return Vector2.from_floats(x * rhs, y * rhs)

    def __div__(self, scalar):
        return Vector2(self._v[0] / scalar, self._v[1] / scalar)


"""
A = (10.0, 20.0)
B = (30.0, 35.0)
AB = Vector2.from_points(A, B)
step = AB * .1
position = Vector2(*A)
for n in range(10):
    position += step
    #print position
"""
