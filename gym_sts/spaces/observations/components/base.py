from abc import ABC, abstractmethod


class ObsComponent(ABC):
    @abstractmethod
    def serialize(self):
        raise RuntimeError("Not implemented")
