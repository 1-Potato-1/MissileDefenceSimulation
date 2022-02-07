import numpy as np

from .simulation_settings import SimulationSettings
from .util import Vector


class Spawner:
    """
    The spawner is responsible for generating initial world location and a ground target of a Missile.
    """
    def __init__(self, simulation_settings: SimulationSettings):
        self.spawn_radius = simulation_settings.missile_spawn_radius
        self.target_area_radius = simulation_settings.target_radius
        self.minimum_theta = np.deg2rad(simulation_settings.minimum_incoming_missile_angle)

    def generate(self, velocity: float) -> (Vector, Vector):
        """
        Generates a position and velocity for a Missile such that it targets a certain target on the ground.
        :param velocity: Absolute velocity of the missile.
        :return: A tuple of two vectors, position and velocity
        """
        theta = self.minimum_theta + np.random.random() * (np.pi - 2 * self.minimum_theta)
        p = Vector()
        p.x = np.cos(theta) * self.spawn_radius
        p.y = np.sin(theta) * self.spawn_radius

        target_x = (1. - 2. * np.random.random()) * self.target_area_radius

        v = Vector()
        v.x = target_x - p.x
        v.y = 0. - p.y
        v.normalize(velocity)

        return p, v
