from abc import ABC, abstractmethod


class ObsComponent(ABC):
    @abstractmethod
    def serialize(self):
        raise NotImplementedError("Not implemented")

    @staticmethod
    @abstractmethod
    def space():
        raise NotImplementedError("Not implemented")
