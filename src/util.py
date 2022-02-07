import numpy as np


class Vector:
    """
    A helper class for storing world information.
    """
    def __init__(self, x=0, y=0):
        self.x: float = x
        self.y: float = y

    def __add__(self, other):
        new = Vector()
        new.x = self.x + other.x
        new.y = self.y + other.y
        return new

    def __iadd__(self, other):
        assert isinstance(other, Vector)
        self.x += other.x
        self.y += other.y

    def __sub__(self, other: 'Vector'):
        assert isinstance(other, Vector)
        new = Vector()
        new.x = self.x - other.x
        new.y = self.y - other.y
        return new

    def __mul__(self, other: float):
        other = float(other)
        new = Vector()
        new.x = self.x * other
        new.y = self.y * other
        return new

    def __rmul__(self, other):
        return self.__mul__(other)

    def normalize(self, r: float = 1.):
        """
        Normalize the absolute value Vector.
        :param r: New absolute value of the vector.
        :return:
        """
        norm = self.get_norm()
        self.x *= r/norm
        self.y *= r/norm

    def get_norm(self):
        """Get the absolute value of the Vector."""
        return np.sqrt(np.square(self.x) + np.square(self.y))


def distance(p1: Vector, p2: Vector):
    """Calculate the distance between two points."""
    return np.sqrt(np.square(p1.x-p2.x) + np.square(p1.y-p2.y))


def intercept(target_p: Vector, target_v: Vector, intercept_p: Vector, intercept_speed: float) ->Vector:
    """
    Creates an interception trajectory for the target.
    :param target_p: Target position
    :param target_v: Target velocity
    :param intercept_p: Starting location of interception projectile.
    :param intercept_speed: Absolute speed of interception projectile.
    :return: A velocity that results in interception with the target.
    """
    p = intercept_p - target_p
    # This code is implementing solution to numerical equation done on paper.
    # find roots of interception equation using "ABC" formula
    firing_solution = Vector()
    firing_solution.y = intercept_speed
    if p.y != 0.0:
        Q = target_v.x - p.x/p.y * target_v.y
        A = 1 + np.square(p.x/p.y)
        B = 2 * Q * p.y/p.x
        C = np.square(Q) - np.square(intercept_speed)
        roots = np.roots([A, B, C])
        roots = [root for root in roots if root > 0 and np.isreal(root)]

        if len(roots) > 0:
            v_y = roots[0]
            v_x = Q + p.x/p.y * v_y
            firing_solution.x = v_x
            firing_solution.y = v_y

    # TODO p.y==0  This also has a possible firing solution
    # TODO not all targets may be intercepted with the intercept_speed given,
    #  but taking this into account would require some code rework, so now a projectile is launched in up y

    return firing_solution
