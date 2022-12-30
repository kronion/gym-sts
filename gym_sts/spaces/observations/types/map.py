from typing import Union

from pydantic import BaseModel


class MapCoordinates(BaseModel):
    x: int
    y: int


class StandardNode(MapCoordinates):
    symbol: str
    children: list[MapCoordinates]


class EliteNode(StandardNode):
    is_burning: bool


Node = Union[StandardNode, EliteNode]
