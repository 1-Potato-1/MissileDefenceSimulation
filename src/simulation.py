from typing import List, Optional

from .defences import IDefence, IDefenceProjectile
from .missiles import IMissile, IMissileGenerator
from .simulation_settings import SimulationSettings
from .tracker import Tracker
from .viewer import Viewer


class Simulation:
    def __init__(self, simulation_settings: SimulationSettings,
                 defences: List[IDefence],
                 missile_generators: List[IMissileGenerator],
                 viewer: Optional[Viewer] = None):
        """
        Setup simulation environment.
        """
        self.simulation_settings = simulation_settings
        self.defences = defences
        self.missile_generators = missile_generators
        self.missiles: List[IMissile] = []
        self.projectiles: List[IDefenceProjectile] = []
        self.tracker = Tracker()
        self.viewer = viewer

    def update(self, delta_time: float):
        """
        Run a single frame of the simulation.
        :param delta_time: real time increment of the frame.
        """
        for projectile in self.projectiles:
            projectile.update(delta_time)

            if projectile.hit():
                if projectile.target in self.missiles:
                    self.missiles.remove(projectile.target)
                self.projectiles.remove(projectile)
                self.tracker.register_missile_intercept(projectile.target)
            if projectile.miss():
                self.projectiles.remove(projectile)

        for missile in self.missiles:
            missile.update(delta_time)

            if missile.p.y < 0:
                self.ground_hit_program(missile)

        for defence in self.defences:
            new_projectiles = defence.update(delta_time, self.missiles)

            for new in new_projectiles:
                self.tracker.register_projectile_fire(new)
            self.projectiles += new_projectiles

        for generator in self.missile_generators:
            new_missiles = generator.update(delta_time)

            for new in new_missiles:
                self.tracker.register_missile_launch(new)
            self.missiles += new_missiles

    def run(self, time: float):
        """
        Run the simulation.
        :param time: End time of the simulation in seconds.
        """
        frames = int(time * self.simulation_settings.frame_rate)
        time_delta = 1/self.simulation_settings.frame_rate
        for _ in range(frames):
            self.update(time_delta)

            if self.viewer:
                self.viewer.draw_frame(self.missiles, self.projectiles, self.defences)

        self.tracker.results()

    def ground_hit_program(self, missile: IMissile):
        """
        Calculate effect of a missile hitting the ground.
        :param missile: Missile hitting the ground
        """
        # TODO currently a small stub, may be expanded to have a more complex model of the area to be protected.
        if abs(missile.p.x) < self.simulation_settings.target_radius:
            missile.get_damage()
            self.tracker.register_missile_hit_target(missile)

        self.missiles.remove(missile)


