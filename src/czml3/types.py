import datetime as dt

import attr
from dateutil.parser import isoparse as parse_iso_date
from w3lib.url import is_url, parse_data_uri

from .base import BaseCZMLObject
from .common import Deletable
from .constants import ISO8601_FORMAT_Z

TYPE_MAPPING = {bool: "boolean"}


def format_datetime_like(dt_object):
    if dt_object is None:
        result = dt_object

    elif isinstance(dt_object, str):
        try:
            parse_iso_date(dt_object)
        except Exception:
            raise
        else:
            result = dt_object

    elif isinstance(dt_object, dt.datetime):
        result = dt_object.astimezone(dt.timezone.utc).strftime(ISO8601_FORMAT_Z)

    else:
        result = dt_object.strftime(ISO8601_FORMAT_Z)

    return result


@attr.s(repr=False, frozen=True, kw_only=True)
class _TimeTaggedCoords(BaseCZMLObject):

    NUM_COORDS: int

    values = attr.ib()

    def __attrs_post_init__(self):
        if not (
            len(self.values) == self.NUM_COORDS
            or len(self.values) % (self.NUM_COORDS + 1) == 0
        ):
            raise ValueError(
                "Input values must have either 3 or N * 4 values, "
                "where N is the number of time-tagged samples."
            )

    def to_json(self):
        return list(self.values)


@attr.s(repr=False, frozen=True, kw_only=True)
class FontValue(BaseCZMLObject):
    """A font, specified using the same syntax as the CSS "font" property."""

    font = attr.ib(default=None)

    def to_json(self):
        return self.font


@attr.s(repr=False, frozen=True, kw_only=True)
class RgbafValue(BaseCZMLObject):
    """A color specified as an array of color components [Red, Green, Blue, Alpha]
     where each component is in the range 0.0-1.0. If the array has four elements,
    the color is constant. If it has five or more elements, they are time-tagged
    samples arranged as [Time, Red, Green, Blue, Alpha, Time, Red, Green, Blue, Alpha, ...],
    where Time is an ISO 8601 date and time string or seconds since epoch.

    """

    values = attr.ib()

    def __attrs_post_init__(self):
        if not (len(self.values) == 4 or len(self.values) % 5 == 0):
            raise ValueError(
                "Input values must have either 4 or N * 5 values, "
                "where N is the number of time-tagged samples."
            )

        if len(self.values) == 4:
            if not all([0 <= val <= 1 for val in self.values]):
                raise ValueError("Color values must be floats in the range 0-1.")

        else:
            for i in range(0, len(self.values), 5):
                v = self.values[i + 1 : i + 5]

                if not all([0 <= val <= 1 for val in v]):
                    raise ValueError("Color values must be floats in the range 0-1.")

    def to_json(self):
        return list(self.values)


@attr.s(repr=False, frozen=True, kw_only=True)
class RgbaValue(BaseCZMLObject):
    """A color specified as an array of color components [Red, Green, Blue, Alpha]
     where each component is in the range 0-255. If the array has four elements,
     the color is constant.

      If it has five or more elements, they are time-tagged samples arranged as
     [Time, Red, Green, Blue, Alpha, Time, Red, Green, Blue, Alpha, ...], where Time
     is an ISO 8601 date and time string or seconds since epoch.

     """

    values = attr.ib()

    def __attrs_post_init__(self):
        if not (len(self.values) == 4 or len(self.values) % 5 == 0):
            raise ValueError(
                "Input values must have either 4 or N * 5 values, "
                "where N is the number of time-tagged samples."
            )

        if len(self.values) == 4:
            if not all([type(val) is int and 0 <= val <= 255 for val in self.values]):
                raise ValueError("Color values must be integers in the range 0-255.")

        else:
            for i in range(0, len(self.values), 5):
                v = self.values[i + 1 : i + 5]

                if not all([type(val) is int and 0 <= val <= 255 for val in v]):
                    raise ValueError(
                        "Color values must be integers in the range 0-255."
                    )

    def to_json(self):
        return list(self.values)


@attr.s(repr=False, frozen=True, kw_only=True)
class ReferenceValue(BaseCZMLObject):
    """ Represents a reference to another property. References can be used to specify that two properties on different
    objects are in fact, the same property.

    """

    string = attr.ib(default=None)

    def __attrs_post_init__(self):
        if not isinstance(self.string, str):
            raise ValueError("Reference must be a string")
        if "#" not in self.string:
            raise ValueError(
                "Invalid reference string format. Input must be of the form id#property"
            )

    def to_json(self):
        return self.string


@attr.s(repr=False, frozen=True, kw_only=True)
class Cartesian3Value(_TimeTaggedCoords):
    """A three-dimensional Cartesian value specified as [X, Y, Z].

    If the values has three elements, the value is constant.
    If it has four or more elements, they are time-tagged samples
    arranged as [Time, X, Y, Z, Time, X, Y, Z, ...],
    where Time is an ISO 8601 date and time string or seconds since epoch.

    """

    NUM_COORDS = 3


@attr.s(repr=False, frozen=True, kw_only=True)
class CartographicRadiansValue(_TimeTaggedCoords):
    """A geodetic, WGS84 position specified as [Longitude, Latitude, Height].

    Longitude and Latitude are in radians and Height is in meters.
    If the array has three elements, the value is constant.
    If it has four or more elements, they are time-tagged samples
    arranged as [Time, Longitude, Latitude, Height, Time, Longitude, Latitude, Height, ...],
    where Time is an ISO 8601 date and time string or seconds since epoch.

    """

    NUM_COORDS = 3


@attr.s(repr=False, frozen=True, kw_only=True)
class CartographicDegreesValue(_TimeTaggedCoords):
    """A geodetic, WGS84 position specified as [Longitude, Latitude, Height].

    Longitude and Latitude are in degrees and Height is in meters.
    If the array has three elements, the value is constant.
    If it has four or more elements, they are time-tagged samples
    arranged as [Time, Longitude, Latitude, Height, Time, Longitude, Latitude, Height, ...],
    where Time is an ISO 8601 date and time string or seconds since epoch.

    """

    NUM_COORDS = 3


@attr.s(repr=False, frozen=True, kw_only=True)
class StringValue(BaseCZMLObject, Deletable):
    """A string value.

    The string can optionally vary with time.
    """

    delete = attr.ib(default=None)
    string = attr.ib(default=None)

    def to_json(self):
        return self.string


@attr.s(repr=False, frozen=True, kw_only=True)
class CartographicRadiansListValue(BaseCZMLObject):
    """A list of geodetic, WGS84 positions specified as [Longitude, Latitude, Height, Longitude, Latitude, Height, ...],
     where Longitude and Latitude are in radians and Height is in meters."""

    values = attr.ib()

    def __attrs_post_init__(self):
        if len(self.values) % 3 != 0:
            raise ValueError(
                "Invalid values. Input values should be arrays of size 3 * N"
            )

    def to_json(self):
        return list(self.values)


@attr.s(repr=False, frozen=True, kw_only=True)
class CartographicDegreesListValue(BaseCZMLObject):
    """A list of geodetic, WGS84 positions specified as [Longitude, Latitude, Height, Longitude, Latitude, Height, ...],
    where Longitude and Latitude are in degrees and Height is in meters."""

    values = attr.ib()

    def __attrs_post_init__(self):
        if len(self.values) % 3 != 0:
            raise ValueError(
                "Invalid values. Input values should be arrays of size 3 * N"
            )

    def to_json(self):
        return list(self.values)


@attr.s(repr=False, frozen=True, kw_only=True)
class DistanceDisplayConditionValue(BaseCZMLObject):
    """A value indicating the visibility of an object based on the distance to the camera, specified as two values
    [NearDistance, FarDistance]. If the array has two elements, the value is constant. If it has three or more elements,
    they are time-tagged samples arranged as [Time, NearDistance, FarDistance, Time, NearDistance, FarDistance, ...],
    where Time is an ISO 8601 date and time string or seconds since epoch.
    """

    values = attr.ib(default=None)

    def __attrs_post_init__(self):
        if len(self.values) != 2 and len(self.values) % 3 != 0:
            raise ValueError(
                "Invalid values. Input values should be arrays of size either 2 or 3 * N"
            )

    def to_json(self):
        return list(self.values)


@attr.s(repr=False, frozen=True, kw_only=True)
class NearFarScalarValue(BaseCZMLObject, Deletable):
    """A near-far scalar value specified as four values [NearDistance, NearValue, FarDistance, FarValue].

     If the array has four elements, the value is constant. If it has five or more elements, they are time-tagged
    samples arranged as [Time, NearDistance, NearValue, FarDistance, FarValue, Time, NearDistance, NearValue,
    FarDistance, FarValue, ...], where Time is an ISO 8601 date and time string or seconds since epoch.
    """

    values = attr.ib(default=None)

    def __attrs_post_init__(self):
        if not (len(self.values) == 4 or len(self.values) % 5 == 0):
            raise ValueError(
                "Input values must have either 4 or N * 5 values, "
                "where N is the number of time-tagged samples."
            )

    def to_json(self):
        return list(self.values)


@attr.s(repr=False, frozen=True, kw_only=True)
class Uri(BaseCZMLObject, Deletable):
    """A URI value.

    The URI can optionally vary with time.
    """

    delete = attr.ib(default=None)
    uri = attr.ib(default=None)

    def __attrs_post_init__(self):
        try:
            parse_data_uri(self.uri)
        except ValueError as e:
            if not is_url(self.uri):
                raise ValueError("uri must be a URL or a data URI") from e

    def to_json(self):
        return self.uri


@attr.s(repr=False, frozen=True, kw_only=True)
class TimeInterval(BaseCZMLObject):
    """A time interval, specified in ISO8601 interval format."""

    _start = attr.ib(default=None, converter=format_datetime_like)
    _end = attr.ib(default=None, converter=format_datetime_like)

    def to_json(self):
        if self._start is None:
            start = "0000-00-00T00:00:00Z"
        else:
            start = self._start

        if self._end is None:
            end = "9999-12-31T24:00:00Z"
        else:
            end = self._end

        return "{start}/{end}".format(start=start, end=end)


@attr.s(repr=False, frozen=True, kw_only=True)
class IntervalValue(BaseCZMLObject):
    """Value over some interval."""

    _start = attr.ib()
    _end = attr.ib()
    _value = attr.ib()

    def to_json(self):
        obj_dict = {"interval": TimeInterval(start=self._start, end=self._end)}

        try:
            obj_dict.update(**self._value.to_json())
        except AttributeError:
            key = TYPE_MAPPING[type(self._value)]
            obj_dict[key] = self._value

        return obj_dict


@attr.s(repr=False, frozen=True)
class Sequence(BaseCZMLObject):
    """Sequence, list, array of objects."""

    _values = attr.ib()

    def to_json(self):
        return list(self._values)


@attr.s(repr=False, frozen=True, kw_only=True)
class UnitQuaternionValue(_TimeTaggedCoords):
    """A set of 4-dimensional coordinates used to represent rotation in 3-dimensional space.

    It's specified as [X, Y, Z, W]. If the array has four elements, the value is constant.
    If it has five or more elements, they are time-tagged samples arranged as
    [Time, X, Y, Z, W, Time, X, Y, Z, W, ...],
    where Time is an ISO 8601 date and time string or seconds since epoch.

    """

    NUM_COORDS = 4
