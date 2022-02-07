from .json_loadable import JSONLoadable


class SimulationSettings(JSONLoadable):
    """
    A container for various settings affecting the simulation. Is loaded from a JSON.
    """
    def __init__(self):
        self.simulation_time: float = 0
        self.frame_rate: float = 0
        self.target_radius: float = 0
        self.missile_spawn_radius: float = 0
        self.minimum_incoming_missile_angle: float = 0

    @staticmethod
    def get_json_name() -> str:
        return "simulation settings"

    @classmethod
    def load_from_json(cls, json_data: dict):
        new = SimulationSettings()
        try:
            new.simulation_time = json_data["simulation time (s)"]
            new.frame_rate = json_data["frame rate(hz)"]
            new.target_radius = json_data["target radius (m)"]
            new.missile_spawn_radius = json_data['missile spawn radius (m)']
            new.minimum_incoming_missile_angle = json_data["minimum incoming missile angle (deg)"]
        except KeyError:
            raise Exception(f"Error loading: {cls.get_json_name()}")

        return new



