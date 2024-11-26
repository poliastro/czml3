from typing import Any, List, Union
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

    id: Union[str] = Field(default="document")
    version: Union[str] = Field(default=CZML_VERSION)
    name: Union[None, str] = Field(default=None)
    description: Union[None, str] = Field(default=None)
    clock: Union[None, Clock, IntervalValue] = Field(default=None)


class Packet(BaseCZMLObject):
    """A CZML Packet.

    See https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Packet
    for further information.
    """

    id: str = Field(default=str(uuid4()))
    delete: Union[None, bool] = Field(default=None)
    name: Union[None, str] = Field(default=None)
    parent: Union[None, str] = Field(default=None)
    description: Union[None, str, StringValue] = Field(default=None)
    availability: Union[None, TimeInterval, List[TimeInterval], Sequence] = Field(
        default=None
    )
    properties: Union[None, Any] = Field(default=None)
    position: Union[None, Position] = Field(default=None)
    orientation: Union[None, Orientation] = Field(default=None)
    viewFrom: Union[None, ViewFrom] = Field(default=None)
    billboard: Union[None, Billboard] = Field(default=None)
    box: Union[None, Box] = Field(default=None)
    corridor: Union[None, Corridor] = Field(default=None)
    cylinder: Union[None, Cylinder] = Field(default=None)
    ellipse: Union[None, Ellipse] = Field(default=None)
    ellipsoid: Union[None, Ellipsoid] = Field(default=None)
    label: Union[None, Label] = Field(default=None)
    model: Union[None, Model] = Field(default=None)
    path: Union[None, Path] = Field(default=None)
    point: Union[None, Point] = Field(default=None)
    polygon: Union[None, Polygon] = Field(default=None)
    polyline: Union[None, Polyline] = Field(default=None)
    rectangle: Union[None, Rectangle] = Field(default=None)
    tileset: Union[None, Tileset] = Field(default=None)
    wall: Union[None, Wall] = Field(default=None)


class Document(BaseCZMLObject):
    """A CZML document, consisting on a list of packets."""

    packets: List[Union[Packet, Preamble]]

    @model_serializer
    def custom_serializer(self):
        return list(self.packets)
