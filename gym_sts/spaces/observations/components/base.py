from abc import ABC, abstractmethod

from pydantic import BaseModel


class ObsComponent(ABC):
    @abstractmethod
    def serialize(self):
        raise NotImplementedError("Not implemented")

    # @abstractmethod
    # def deserialize(self, data: dict):
    #     raise NotImplementedError("Not implemented")

    @staticmethod
    @abstractmethod
    def space():
        raise NotImplementedError("Not implemented")


class PydanticComponent(ObsComponent, BaseModel):
    pass
