from abc import ABC, abstractmethod
from typing import List

import numpy as np

from .drawable import Drawable, Square
from .json_loadable import JSONLoadable
from .missiles import IMissile
from .util import distance, Vector, intercept


class IDefenceProjectile(Drawable, ABC):
    """
    The interface for projectiles fired by defences
    """
    target: IMissile
    p: Vector
    v: Vector

    @abstractmethod
    def update(self, delta_time: float):
        """Update state of projectile"""
        pass

    @abstractmethod
    def hit(self) -> bool:
        """Make check if projectile has hit a target"""
        pass

    @abstractmethod
    def miss(self) -> bool:
        """Make check if projectile has missed its target"""
        pass


class IDefence(JSONLoadable, Drawable, ABC):
    """
    The interface for the defence systems. Fill fire on missiles in range
    """
    p: Vector

    @abstractmethod
    def update(self, delta_time: float, missiles_world: List[IMissile]) -> List[IDefenceProjectile]:
        """
        Update state of defence system. Might fire one or more Projectiles
        """
        pass


class BulletProjectile(IDefenceProjectile):
    """Projectile is launched at a fixed trajectory"""
    def __init__(self, p: Vector, v: Vector, accuracy: float, target: IMissile):
        Drawable.__init__(self, Square, rgb=(0, 0, 0), scale=3)
        self.p = p
        self.v = v
        self.target = target
        self.accuracy = accuracy
        self.hit_flag = False
        self.miss_flag = False

    def update(self, delta_time: float):
        delta_p: Vector = self.v * delta_time
        target_distance = distance(self.p, self.target.p)
        delta_norm = delta_p.get_norm()
        # TODO there is a bug here, hit based on being close enough, where close enough metric
        #  depends on numerical settings. Should be replaced hit system based on object sizes
        if delta_norm > target_distance:
            self.hit_flag = True
        self.p = self.p + delta_p

    def hit(self) -> bool:
        if self.hit_flag:
            if np.random.random() < self.accuracy:
                return True
            else:
                self.miss_flag = True
        return False

    def miss(self) -> bool:
        return self.miss_flag


class BulletDefence(IDefence):
    """Defence system firring BulletProjectiles"""
    def __init__(self):
        Drawable.__init__(self, Square, scale=10)
        self.p = Vector()
        self.reload_time = 0
        self.projectile_speed = 0
        self.accuracy = 0
        self.range = 0
        self.count_down = 0

    @staticmethod
    def get_json_name() -> str:
        return "bullet defence"

    @classmethod
    def load_from_json(cls, json_data: dict):
        new = BulletDefence()
        try:
            new.p.x = json_data["location (m)"]
            new.p.y = 0
            new.reload_time = json_data["reload time (s)"]
            new.projectile_speed = json_data["projectile speed (m/s)"]
            new.accuracy = json_data["accuracy (%)"]
            new.range = json_data["range (m)"]
        except KeyError:
            raise Exception(f"Error loading: {cls.get_json_name()}")

        return new

    def update(self, delta_time: float, missiles_world: List[IMissile]) -> List[IDefenceProjectile]:
        if self.count_down <= 0:
            in_range_missiles = [missile for missile in missiles_world
                                 if distance(self.p, missile.p) < self.range]
            if len(in_range_missiles) > 0:
                missile = self.fire(in_range_missiles)
                self.count_down = self.reload_time - delta_time
                return [missile]

        self.count_down -= delta_time
        return []

    def fire(self, in_range_missiles: List[IMissile]) -> IDefenceProjectile:
        missile_target = in_range_missiles[np.random.randint(len(in_range_missiles))]
        velocity: Vector = intercept(missile_target.p, missile_target.v, self.p, self.projectile_speed)
        velocity.normalize(self.projectile_speed)
        bullet = BulletProjectile(self.p, velocity, self.accuracy, missile_target)
        return bullet


class SeekerProjectile(IDefenceProjectile):
    """Projectile that will continuously reorient its velocity to the target"""
    def __init__(self, p: Vector, v: Vector, explosion_radius: float, target: IMissile):
        Drawable.__init__(self, Square, rgb=(100, 0, 100), scale=5)
        self.p = p
        self.v = v
        self.target = target
        self.hit_flag = False
        self.explosion_radius = explosion_radius

    def update(self, delta_time: float):
        original_speed = self.v.get_norm()
        self.v = self.target.p - self.p
        self.v.normalize(original_speed)
        # TODO there is a chance to overshoot (possibly loop) if frame rate is too high.
        self.p = self.p + self.v * delta_time
        target_distance = distance(self.p, self.target.p)
        if self.explosion_radius > target_distance:
            self.hit_flag = True

    def hit(self) -> bool:
        if self.hit_flag:
            return True
        return False

    def miss(self) -> bool:
        if self.target.p.y < 0:
            # Target hit ground, in future a flag on the target if it is still in existence
            return True
        else:
            return False


class SeekerDefence(IDefence):
    """Defence system firring SeekerProjectiles"""
    def __init__(self):
        Drawable.__init__(self, Square, scale=12, rgb=(0, 0, 0))
        self.p = Vector()
        self.reload_time = 0
        self.projectile_speed = 0
        self.range = 0
        self.count_down = 0
        self.explosion_radius = 0

    @staticmethod
    def get_json_name() -> str:
        return "seeker defence"

    @classmethod
    def load_from_json(cls, json_data: dict):
        new = SeekerDefence()
        try:
            new.p.x = json_data["location (m)"]
            new.p.y = 0
            new.reload_time = json_data["reload time (s)"]
            new.projectile_speed = json_data["projectile speed (m/s)"]
            new.explosion_radius = json_data["explosion radius (m)"]
            new.range = json_data["range (m)"]
        except KeyError:
            raise Exception(f"Error loading: {cls.get_json_name()}")

        return new

    def update(self, delta_time: float, missiles_world: List[IMissile]) -> List[IDefenceProjectile]:
        if self.count_down <= 0:
            in_range_missiles = [missile for missile in missiles_world
                                 if distance(self.p, missile.p) < self.range]
            if len(in_range_missiles) > 0:
                missile = self.fire(in_range_missiles)
                self.count_down = self.reload_time - delta_time
                return [missile]

        self.count_down -= delta_time
        return []

    def fire(self, in_range_missiles: List[IMissile]) -> IDefenceProjectile:
        missile_target = in_range_missiles[np.random.randint(len(in_range_missiles))]
        velocity: Vector = missile_target.p - self.p
        velocity.normalize(self.projectile_speed)
        bullet = SeekerProjectile(self.p, velocity, self.explosion_radius, missile_target)
        return bullet
