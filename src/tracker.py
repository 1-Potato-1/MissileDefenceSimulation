from .defences import IDefenceProjectile
from .missiles import IMissile


class Tracker:
    """
    Tracks various statistics during the simulation.
    """
    def __init__(self):
        self.missiles_launched = {}
        self.projectiles_fired = {}
        self.missiles_hit_target = {}
        self.missiles_intercepted = {}
        self.damage_received = 0

    def register_missile_launch(self, missile: IMissile):
        name = missile.__class__.__name__
        self.default_register(self.missiles_launched, name)

    def register_projectile_fire(self, projectile: IDefenceProjectile):
        name = projectile.__class__.__name__
        self.default_register(self.projectiles_fired, name)

    def register_missile_hit_target(self, missile: IMissile):
        name = missile.__class__.__name__
        self.default_register(self.missiles_hit_target, name)
        self.damage_received += missile.get_damage()

    def register_missile_intercept(self, missile: IMissile):
        name = missile.__class__.__name__
        self.default_register(self.missiles_intercepted, name)

    def results(self):
        """
        Prints statistics results to the console.
        :return:
        """
        print(f"Missile launches: {self.sum_register(self.missiles_launched)}\n"
              f"Projectiles fired: {self.sum_register(self.projectiles_fired)}\n"
              f"Missiles hit target: {self.sum_register(self.missiles_hit_target)}\n"
              f"Missiles intercepted: {self.sum_register(self.missiles_intercepted)}\n"
              f"Damage received: {self.damage_received:.2f}\n")

    @staticmethod
    def sum_register(register: dict):
        sum_ = 0
        for key in register.keys():
            sum_ += register[key]
        return sum_

    @staticmethod
    def default_register(register: dict, name: str):
        if name not in register.keys():
            register[name] = 1
        else:
            register[name] += 1
