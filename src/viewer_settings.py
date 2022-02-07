
from .json_loadable import JSONLoadable


class ViewerSettings(JSONLoadable):
    """
    A container for various settings affecting the viewer. Is loaded from a JSON.
    """
    def __init__(self):
        self.pixels_x: int = 0
        self.pixels_y: int = 0

    @staticmethod
    def get_json_name() -> str:
        return "viewer settings"

    @classmethod
    def load_from_json(cls, json_data: dict):
        new = ViewerSettings()
        try:
            new.pixels_x = json_data["pixels x"]
            new.pixels_y = json_data["pixels y"]
        except KeyError:
            raise Exception(f"Error loading: {cls.get_json_name()}")

        return new
