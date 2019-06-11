from typing import Any, Dict, List, Optional, Union
from uuid import uuid4

from .base import BaseCZMLObject
from .properties import Billboard, Position
from .values import StringValue

CZML_VERSION = "1.0"


class Preamble(BaseCZMLObject):
    """The preamble packet."""

    KNOWN_PROPERTIES = ["id", "version", "name"]

    def __init__(
        self,
        *,
        version: str = CZML_VERSION,
        name: Optional[str] = None,
    ):
        self._id = "document"
        self._version = version
        self._name = name

    @property
    def id(self):
        return self._id

    @property
    def version(self):
        return self._version

    @property
    def name(self):
        return self._name


class Packet(BaseCZMLObject):
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
        description: Union[str, StringValue, None] = None,
        properties: Optional[Dict[str, Any]] = None,
        position: Optional[Position] = None,
        billboard: Optional[Billboard] = None,
    ):
        if id is None:
            id = str(uuid4())

        self._id = id
        self._delete = delete
        self._name = name
        self._parent = parent
        self._description = description
        self._properties = properties
        self._position = position
        self._billboard = billboard

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
    def description(self):
        """An HTML description of the object."""
        return self._description

    @property
    def properties(self):
        """A set of custom properties for this object."""
        return self._properties

    @property
    def position(self):
        """The position of the object in the world.

        The position has no direct visual representation,
        but it is used to locate billboards, labels,
        and other graphical items attached to the object.
        """
        return self._position

    @property
    def billboard(self):
        """A billboard, or viewport-aligned image, sometimes called a marker.

        The billboard is positioned in the scene by the position property.

        """
        return self._billboard


class Document(BaseCZMLObject):
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
