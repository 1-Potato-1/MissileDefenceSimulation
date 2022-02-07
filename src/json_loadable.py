from abc import ABC, abstractmethod


class JSONLoadable(ABC):
    @classmethod
    @abstractmethod
    def load_from_json(cls, json_data: dict):
        """
        Creates an instance of a JSON loadable class.
        :param json_data: A dictionary containing data from a JSON file
        """
        pass

    @staticmethod
    @abstractmethod
    def get_json_name() -> str:
        """
        Returns the string corresponding to the node for a JSON loadable class in a JSON file
        """
        pass
