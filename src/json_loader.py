import json
from pathlib import Path
from typing import List, Type

from .defences import IDefence, BulletDefence, SeekerDefence
from .json_loadable import JSONLoadable
from .missiles import IMissileGenerator, DefaultMissileGenerator, BoostMissileGenerator
from .simulation_settings import SimulationSettings
from .viewer_settings import ViewerSettings


class JSONLoader:
    """
    Manages the loading of JSONLoadable objects from a JSON file.
    """
    def __init__(self, file: Path):
        """

        :param file: The JSON parameter file.
        """
        if not file.exists():
            raise FileNotFoundError(f"Could not find JSON file: {str(file)}")

        with open(str(file)) as file_obj:
            json_data = json.load(file_obj)
        self.data = json_data

    def load_simulation_settings(self) -> SimulationSettings:
        return self._unique_loader(SimulationSettings)

    def load_viewer_settings(self) -> ViewerSettings:
        return self._unique_loader(ViewerSettings)

    def load_missiles(self) -> List[IMissileGenerator]:
        # TODO Has a small code weakness, each new instance must also be added to available_classes to work
        available_classes = [DefaultMissileGenerator, BoostMissileGenerator]
        return self._multiple_instance_loader(available_classes)

    def load_defences(self) -> List[IDefence]:
        available_classes = [BulletDefence, SeekerDefence]
        return self._multiple_instance_loader(available_classes)

    def _unique_loader(self, class_: Type[JSONLoadable]):
        """
        Loads JSON loadable object.
        Loads only one object and JSON node must match exactly to JSON name specified in the class
        :param class_: The desired class to be loaded
        :return: New JSON loadable object
        """
        key = class_.get_json_name()
        if key in self.data:
            return class_.load_from_json(self.data[key])
        else:
            raise Exception(f"Could not find in JSON: {key}")

    def _multiple_instance_loader(self, classes: List[Type[JSONLoadable]]):
        """
        Loads multiple JSON loadable objects.
        May load zero or multiple objects per class.
        Multiple loading is possible due to JSON node name not being matched exactly,
        but it must contain JSON name specified in the class.
        :param classes: List of classes to be loaded
        :return: List of new JSON loadable objects
        """
        for class_ in classes:
            assert issubclass(class_, JSONLoadable)
        class_keys = [class_.get_json_name() for class_ in classes]

        instances = []
        for class_key, class_ in zip(class_keys, classes):
            matching_keys = [key for key in self.data.keys() if class_key in key]
            for matching_key in matching_keys:
                instance = class_.load_from_json(self.data[matching_key])
                instances.append(instance)
        return instances
