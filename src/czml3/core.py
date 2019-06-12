from uuid import uuid4

from .base import BaseCZMLObject
from .types import Sequence

CZML_VERSION = "1.0"


class Preamble(BaseCZMLObject):
    """The preamble packet."""

    KNOWN_PROPERTIES = ["id", "version", "name", "clock"]

    def __init__(self, *, version=CZML_VERSION, name=None, clock=None):
        self._id = "document"
        self._version = version
        self._name = name
        self._clock = clock

    @property
    def id(self):
        return self._id

    @property
    def version(self):
        """The CZML version being written."""
        return self._version

    @property
    def name(self):
        return self._name

    @property
    def clock(self):
        """The clock settings for the entire data set."""
        return self._clock


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
        id=None,
        delete=None,
        name=None,
        parent=None,
        description=None,
        availability=None,
        properties=None,
        position=None,
        billboard=None,
        label=None,
        path=None,
    ):
        if id is None:
            id = str(uuid4())

        self._id = id
        self._delete = delete
        self._name = name
        self._parent = parent
        self._description = description
        self._availability = availability
        self._properties = properties
        self._position = position
        self._billboard = billboard
        self._label = label
        self._path = path

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
    def availability(self):
        """The set of time intervals over which data for an object is available.

        The property can be a single string specifying a single interval,
        or an array of strings representing intervals.
        A later CZML packet can update this availability
        if it changes or is found to be incorrect.
        For example, an SGP4 propagator may initially report availability for all time,
        but then later the propagator throws an exception
        and the availability can be adjusted to end at that time.
        If this optional property is not present,
        the object is assumed to be available for all time.
        Availability is scoped to a particular CZML stream,
        so two different streams can list different availability for a single object.
        Within a single stream,
        the last availability stated for an object is the one in effect
        and any availabilities in previous packets are ignored.
        If an object is not available at a time,
        the client will not draw that object.
        """
        return self._availability

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

    @property
    def label(self):
        """A string of text.

        The label is positioned in the scene by the position property.

        """
        return self._label

    @property
    def path(self):
        """A path, which is a polyline defined by the motion of an object over time.

        The possible vertices of the path are specified by the position property.

        """
        return self._path


class Document(Sequence):
    """A CZML document, consisting on a list of packets."""

    @property
    def packets(self):
        return self._values
