from typing import List, Optional
from uuid import uuid4

from ._version import get_versions
from .base import BaseCZMLObject as _BaseCZMLObject
from .properties import Position

__version__ = get_versions()["version"]
del get_versions


class Packet(_BaseCZMLObject):
    """A CZML Packet.

    See https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Packet
    for further information.
    """

    # https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Packet
    KNOWN_PROPERTIES = [
        "id",
        "delete",
        "name",
        "parent",
        "description",
        "clock",
        "version",
        "availability",
        "properties",
        "position",
        "orientation",
        "viewFrom",
        "billboard",
        "box",
        "corridor",
        "cylinder",
        "ellipse",
        "ellipsoid",
        "label",
        "model",
        "path",
        "polygon",
        "polyline",
        "rectangle",
        "wall",
    ]

    def __init__(
        self,
        *,
        id: Optional[str] = None,
        delete: Optional[bool] = None,
        name: Optional[str] = None,
        parent: Optional[str] = None,
        position: Optional[Position] = None,
    ):
        if id is None:
            id = str(uuid4())

        self._id = id
        self._delete = delete
        self._name = name
        self._parent = parent
        self._position = position

    @property
    def id(self):
        """The ID of the object described by this packet.

        IDs do not need to be GUIDs,
        but they do need to uniquely identify a single object within a CZML source
        and any other CZML sources loaded into the same scope.
        If this property is not specified,
        the client will automatically generate a unique one.
        However,
        this prevents later packets from referring to this object
        in order to add more data to it.
        """
        return self._id

    @property
    def delete(self):
        """Whether the client should delete all existing data for this object.

        If true, all other properties in this packet will be ignored.
        """
        return self._delete

    @property
    def name(self):
        """The name of the object.

        It does not have to be unique and is intended for user consumption.
        """
        return self._name

    @property
    def parent(self):
        """An HTML description of the object."""
        return self._parent

    @property
    def position(self):
        """The position of the object in the world.

        The position has no direct visual representation,
        but it is used to locate billboards, labels,
        and other graphical items attached to the object.
        """
        return self._position


class Document(_BaseCZMLObject):
    def __init__(self, packets: List[Packet]):
        self._packets = packets

    @property
    def packets(self):
        return self._packets

    def to_json(self):
        obj_list = []
        for packet in self.packets:
            obj_list.append(packet.to_json())

        return obj_list
