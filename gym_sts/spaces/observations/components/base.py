from abc import ABC, abstractmethod

from pydantic import BaseModel


class ObsComponent(ABC):
    @abstractmethod
    def serialize(self):
        """
        Convert the component instance into a data structure
        conforming to the shape of the component's gym space.
        """

        raise NotImplementedError("Not implemented")

    # TODO @kronion: uncomment once EventStateObs conforms to the API.
    # @classmethod
    # @abstractmethod
    # def deserialize(cls, data):
    #     """
    #     Convert data matching the shape of the component's
    #     gym space into a new component instance.
    #     """
    #
    #     raise NotImplementedError("Not implemented")

    @staticmethod
    @abstractmethod
    def space():
        """
        Returns the shape of the component's gym space.
        """

        raise NotImplementedError("Not implemented")


class PydanticComponent(ObsComponent, BaseModel):
    """
    A subclass of ObsComponent that is also a Pydantic model. In cases where you don't
    need an __init__() method to perform more complex parsing of the CommunicationMod
    state, you can use this class to define a dataclass-style component.
    """

    pass
