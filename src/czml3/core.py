from typing import Any
from uuid import uuid4

from pydantic import Field, model_serializer

from czml3.types import StringValue

from .base import BaseCZMLObject
from .properties import (
    Billboard,
    Box,
    Clock,
    Corridor,
    Cylinder,
    Ellipse,
    Ellipsoid,
    Label,
    Model,
    Orientation,
    Path,
    Point,
    Polygon,
    Polyline,
    Position,
    Rectangle,
    Tileset,
    ViewFrom,
    Wall,
)
from .types import IntervalValue, Sequence, TimeInterval

CZML_VERSION = "1.0"


class Preamble(BaseCZMLObject):
    """The preamble packet."""

    id: str = Field(default="document")
    version: str = Field(default=CZML_VERSION)
    name: None | str = Field(default=None)
    description: None | str = Field(default=None)
    clock: None | Clock | IntervalValue = Field(default=None)


class Packet(BaseCZMLObject):
    """A CZML Packet.

    See https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Packet
    for further information.
    """

    id: str = Field(default=str(uuid4()))
    delete: None | bool = Field(default=None)
    name: None | str = Field(default=None)
    parent: None | str = Field(default=None)
    description: None | str | StringValue = Field(default=None)
    availability: None | TimeInterval | list[TimeInterval] | Sequence = Field(
        default=None
    )
    properties: None | Any = Field(default=None)
    position: None | Position = Field(default=None)
    orientation: None | Orientation = Field(default=None)
    viewFrom: None | ViewFrom = Field(default=None)
    billboard: None | Billboard = Field(default=None)
    box: None | Box = Field(default=None)
    corridor: None | Corridor = Field(default=None)
    cylinder: None | Cylinder = Field(default=None)
    ellipse: None | Ellipse = Field(default=None)
    ellipsoid: None | Ellipsoid = Field(default=None)
    label: None | Label = Field(default=None)
    model: None | Model = Field(default=None)
    path: None | Path = Field(default=None)
    point: None | Point = Field(default=None)
    polygon: None | Polygon = Field(default=None)
    polyline: None | Polyline = Field(default=None)
    rectangle: None | Rectangle = Field(default=None)
    tileset: None | Tileset = Field(default=None)
    wall: None | Wall = Field(default=None)


class Document(BaseCZMLObject):
    """A CZML document, consisting on a list of packets."""

    packets: list[Packet | Preamble]

    @model_serializer
    def custom_serializer(self):
        return list(self.packets)
