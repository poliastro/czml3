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
from .types import IntervalValue, TimeInterval, TimeIntervalCollection

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
    name: None | str | TimeIntervalCollection = Field(default=None)
    parent: None | str | TimeIntervalCollection = Field(default=None)
    description: None | str | StringValue | TimeIntervalCollection = Field(default=None)
    availability: None | TimeInterval | TimeIntervalCollection = Field(default=None)
    properties: None | Any | TimeIntervalCollection = Field(default=None)
    position: (
        None | Position | PositionList | PositionListOfLists | TimeIntervalCollection
    ) = Field(default=None)
    orientation: None | Orientation | TimeIntervalCollection = Field(default=None)
    viewFrom: None | ViewFrom | TimeIntervalCollection = Field(default=None)
    billboard: None | Billboard | TimeIntervalCollection = Field(default=None)
    box: None | Box | TimeIntervalCollection = Field(default=None)
    corridor: None | Corridor | TimeIntervalCollection = Field(default=None)
    cylinder: None | Cylinder | TimeIntervalCollection = Field(default=None)
    ellipse: None | Ellipse | TimeIntervalCollection = Field(default=None)
    ellipsoid: None | Ellipsoid | TimeIntervalCollection = Field(default=None)
    label: None | Label | TimeIntervalCollection = Field(default=None)
    model: None | Model | TimeIntervalCollection = Field(default=None)
    path: None | Path | TimeIntervalCollection = Field(default=None)
    point: None | Point | TimeIntervalCollection = Field(default=None)
    polygon: None | Polygon | TimeIntervalCollection = Field(default=None)
    polyline: None | Polyline | TimeIntervalCollection = Field(default=None)
    rectangle: None | Rectangle | TimeIntervalCollection = Field(default=None)
    tileset: None | Tileset | TimeIntervalCollection = Field(default=None)
    wall: None | Wall | TimeIntervalCollection = Field(default=None)


class Document(BaseCZMLObject):
    """A CZML document, consisting on a list of packets."""

    packets: list[Packet | Preamble]

    @model_serializer
    def custom_serializer(self):
        return list(self.packets)
