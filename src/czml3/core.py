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
    PositionList,
    PositionListOfLists,
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

    id: str = Field(default_factory=lambda _: str(uuid4()))
    delete: None | bool = Field(default=None)
    name: None | str | Sequence = Field(default=None)
    parent: None | str | Sequence = Field(default=None)
    description: None | str | StringValue | Sequence = Field(default=None)
    availability: None | TimeInterval | list[TimeInterval] | Sequence | Sequence = (
        Field(default=None)
    )
    properties: None | Any | Sequence = Field(default=None)
    position: None | Position | PositionList | PositionListOfLists | Sequence = Field(
        default=None
    )
    orientation: None | Orientation | Sequence = Field(default=None)
    viewFrom: None | ViewFrom | Sequence = Field(default=None)
    billboard: None | Billboard | Sequence = Field(default=None)
    box: None | Box | Sequence = Field(default=None)
    corridor: None | Corridor | Sequence = Field(default=None)
    cylinder: None | Cylinder | Sequence = Field(default=None)
    ellipse: None | Ellipse | Sequence = Field(default=None)
    ellipsoid: None | Ellipsoid | Sequence = Field(default=None)
    label: None | Label | Sequence = Field(default=None)
    model: None | Model | Sequence = Field(default=None)
    path: None | Path | Sequence = Field(default=None)
    point: None | Point | Sequence = Field(default=None)
    polygon: None | Polygon | Sequence = Field(default=None)
    polyline: None | Polyline | Sequence = Field(default=None)
    rectangle: None | Rectangle | Sequence = Field(default=None)
    tileset: None | Tileset | Sequence = Field(default=None)
    wall: None | Wall | Sequence = Field(default=None)


class Document(BaseCZMLObject):
    """A CZML document, consisting on a list of packets."""

    packets: list[Packet | Preamble]

    @model_serializer
    def custom_serializer(self):
        return list(self.packets)
