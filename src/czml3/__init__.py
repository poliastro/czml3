import json
import warnings
from json import JSONEncoder
from typing import List, Optional
from uuid import uuid4

from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions


# https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Packet
PACKET_PROPERTIES = [
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


class _BaseCZMLObject:
    def __repr__(self):
        return self.dumps(indent=4)

    def dumps(self, *args, **kwargs):
        if "cls" in kwargs:
            warnings.warn("Ignoring specified cls", UserWarning)

        kwargs["cls"] = _CZMLEncoder
        return json.dumps(self, *args, **kwargs)

    def dump(self, fp, *args, **kwargs):
        for chunk in _CZMLEncoder(*args, **kwargs).iterencode(self):
            fp.write(chunk)


class _CZMLEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, Packet):
            obj_dict = {}
            for property_name in PACKET_PROPERTIES:
                if getattr(o, property_name, None) is not None:
                    obj_dict[property_name] = getattr(o, property_name)

            return obj_dict

        elif isinstance(o, Document):
            obj_list = []
            for packet in o.packets:
                obj_list.append(self.default(packet))

            return obj_list

        return super().default(o)


class Packet(_BaseCZMLObject):
    """A CZML Packet.

    See https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Packet
    for further information.
    """

    def __init__(
        self,
        *,
        id: Optional[str] = None,
        delete: Optional[bool] = None,
        name: Optional[str] = None,
        parent: Optional[str] = None,
    ):
        if id is None:
            id = str(uuid4())

        self._id = id
        self._delete = delete
        self._name = name
        self._parent = parent

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


class Document(_BaseCZMLObject):
    def __init__(self, packets: List[Packet]):
        self._packets = packets

    @property
    def packets(self):
        return self._packets
