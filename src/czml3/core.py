from uuid import uuid4

import attr

from .base import BaseCZMLObject
from .types import Sequence

CZML_VERSION = "1.0"


@attr.s(str=False, frozen=True, kw_only=True)
class Preamble(BaseCZMLObject):
    """The preamble packet."""

    id = attr.ib(init=False, default="document")

    version = attr.ib(default=CZML_VERSION)
    name = attr.ib(default=None)
    description = attr.ib(default=None)
    clock = attr.ib(default=None)


@attr.s(str=False, frozen=True, kw_only=True)
class Packet(BaseCZMLObject):
    """A CZML Packet.

    See https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Packet
    for further information.
    """

    id = attr.ib(factory=lambda: str(uuid4()))
    delete = attr.ib(default=None)
    name = attr.ib(default=None)
    parent = attr.ib(default=None)
    description = attr.ib(default=None)
    availability = attr.ib(default=None)
    properties = attr.ib(default=None)
    position = attr.ib(default=None)
    orientation = attr.ib(default=None)
    viewFrom = attr.ib(default=None)
    billboard = attr.ib(default=None)
    box = attr.ib(default=None)
    corridor = attr.ib(default=None)
    cylinder = attr.ib(default=None)
    ellipse = attr.ib(default=None)
    ellipsoid = attr.ib(default=None)
    label = attr.ib(default=None)
    model = attr.ib(default=None)
    path = attr.ib(default=None)
    point = attr.ib(default=None)
    polygon = attr.ib(default=None)
    polyline = attr.ib(default=None)
    rectangle = attr.ib(default=None)
    tileset = attr.ib(default=None)
    wall = attr.ib(default=None)


@attr.s(str=False, frozen=True)
class Document(Sequence):
    """A CZML document, consisting on a list of packets."""

    @property
    def packets(self):
        return self._values
