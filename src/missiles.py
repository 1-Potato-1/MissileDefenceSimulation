from abc import ABC, abstractmethod
from typing import List

import numpy as np

from .drawable import Drawable, Circle
from .json_loadable import JSONLoadable
from .spawner import Spawner
from .util import Vector


class IMissile(ABC, Drawable):
    """
    Interface for missiles.
    Missiles are world objects that are generated by MissileGenerator objects during the simulation.
    """
    p: Vector  # position
    v: Vector  # velocity

    @abstractmethod
    def update(self, delta_time: float):
        """
        Update state of missile.
        """
        pass

    @abstractmethod
    def get_damage(self) -> float:
        """
        Calculate the damage the missile causes.
        :return:
        """
        pass


class IMissileGenerator(JSONLoadable, ABC):
    """
    Interface for MissileGenerators. MissileGenerators generate missiles of their respective type.
    Requires a spawner to be set to function.
    """
    spawner: Spawner

    @abstractmethod
    def update(self, delta_time: float) -> List[IMissile]:
        """
        Update state of MissileGenerator. Returns a list of new missiles.
        :param delta_time: time increment of frame.
        :return: List of new missiles, possibly empty
        """
        pass

    def set_spawner(self, spawner: Spawner):
        self.spawner = spawner


class DefaultMissile(IMissile):
    """
    A missile that will move on a straight line with constant speed.
    """
    def __init__(self, p: Vector, v: Vector):
        Drawable.__init__(self, shape=Circle, rgb=(255, 0, 0), scale=4)
        self.p = p
        self.v = v

    def update(self, delta_time: float):
        self.p = self.p + delta_time * self.v

    def get_damage(self):
        return 1.0


class DefaultMissileGenerator(IMissileGenerator):
    """
    Creates default missiles.
    """
    def __init__(self):
        self.frequency = 0
        self.velocity = 0
        self.spawner: Spawner = None

    def update(self, delta_time: float) -> List[IMissile]:
        assert isinstance(self.spawner, Spawner)
        lambda_ = self.frequency * delta_time
        new_missiles_num = np.random.poisson(lambda_)
        new_missiles = []

        for _ in range(new_missiles_num):

            missile = DefaultMissile(*(self.spawner.generate(self.velocity)))
            new_missiles.append(missile)

        return new_missiles

    @classmethod
    def load_from_json(cls, json_data: dict):
        new = DefaultMissileGenerator()
        try:
            new.frequency = json_data["frequency (missiles/second)"]
            new.velocity = json_data["speed (m/s)"]
        except KeyError:
            raise Exception(f"Error loading: {cls.get_json_name()}")

        return new

    @staticmethod
    def get_json_name() -> str:
        return "default missile"


class BoostMissile(IMissile):
    """
    Missile that will receive a speed boost at set time before impact.
    """
    def __init__(self, p: Vector, v: Vector, boost: float, countdown: float):
        Drawable.__init__(self, shape=Circle, rgb=(120, 120, 0), scale=5)
        self.p = p
        self.v = v
        self.boost = boost
        self.countdown = countdown
        self.boost_triggered_flag = False

    def update(self, delta_time: float):
        self.p = self.p + delta_time * self.v
        self.countdown -= delta_time
        if self.countdown < 0 and not self.boost_triggered_flag:
            original_speed = self.v.get_norm()
            self.v.normalize(original_speed + self.boost)
            self.boost_triggered_flag = True
            self.rgb = (255, 255, 255)

    def get_damage(self):
        return 1.0


class BoostMissileGenerator(IMissileGenerator):
    """
    Creates BoostMissiles.
    """
    def __init__(self):
        self.frequency = 0
        self.velocity = 0
        self.boost = 0
        self.boost_timer = 0
        self.spawner: Spawner = None

    def update(self, delta_time: float) -> List[IMissile]:
        assert isinstance(self.spawner, Spawner)
        lambda_ = self.frequency * delta_time
        new_missiles_num = np.random.poisson(lambda_)
        new_missiles = []

        for _ in range(new_missiles_num):

            p, v = self.spawner.generate(self.velocity)
            # TODO currently boost timer is seconds before impact with original speed.
            #  It is possible to compute the timer such that the boost timer will be actual seconds to impact.
            time_before_impact = -p.y / v.y
            missile = BoostMissile(p, v, self.boost, time_before_impact - self.boost_timer)
            new_missiles.append(missile)

        return new_missiles

    @classmethod
    def load_from_json(cls, json_data: dict):
        new = BoostMissileGenerator()
        try:
            new.frequency = json_data["frequency (missiles/second)"]
            new.velocity = json_data["speed (m/s)"]
            new.boost = json_data["boost (m/s)"]
            new.boost_timer = json_data["boost timer (s)"]

        except KeyError:
            raise Exception(f"Error loading: {cls.get_json_name()}")

        return new

    @staticmethod
    def get_json_name() -> str:
        return "boost missile"
