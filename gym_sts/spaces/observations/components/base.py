from abc import ABC, abstractmethod, abstractclassmethod

import gym

class ObsComponent(ABC):
    @abstractmethod
    def serialize(self):
        """Turns this component into a gym-compatible datastructure."""

    @abstractclassmethod
    def space(cls) -> gym.Space:
        """The gym space for this component type."""
