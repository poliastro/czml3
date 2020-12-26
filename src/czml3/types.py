import datetime as dt

import attr
from dateutil.parser import isoparse as parse_iso_date

from .base import BaseCZMLObject
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


@attr.s(str=False, frozen=True, kw_only=True)
class _TimeTaggedCoords(BaseCZMLObject):

    NUM_COORDS: int

    values = attr.ib()

    @values.validator
    def _check_values(self, attribute, value):
        if not (
            len(value) == self.NUM_COORDS or len(value) % (self.NUM_COORDS + 1) == 0
        ):
            raise ValueError(
                "Input values must have either 3 or N * 4 values, "
                "where N is the number of time-tagged samples."
            )

    def to_json(self):
        return list(self.values)


@attr.s(str=False, frozen=True, kw_only=True)
class FontValue(BaseCZMLObject):
    """A font, specified using the same syntax as the CSS "font" property."""

    font = attr.ib(default=None)

    def to_json(self):
        return self.font


@attr.s(str=False, frozen=True, kw_only=True)
class RgbafValue(BaseCZMLObject):
    """A color specified as an array of color components [Red, Green, Blue, Alpha]
     where each component is in the range 0.0-1.0. If the array has four elements,
    the color is constant. If it has five or more elements, they are time-tagged
    samples arranged as [Time, Red, Green, Blue, Alpha, Time, Red, Green, Blue, Alpha, ...],
    where Time is an ISO 8601 date and time string or seconds since epoch.

    """

    values = attr.ib()

    @values.validator
    def _check_values(self, attribute, value):
        if not (len(value) == 4 or len(value) % 5 == 0):
            raise ValueError(
                "Input values must have either 4 or N * 5 values, "
                "where N is the number of time-tagged samples."
            )

        if len(value) == 4:
            if not all([0 <= val <= 1 for val in value]):
                raise ValueError("Color values must be floats in the range 0-1.")

        else:
            for i in range(0, len(value), 5):
                v = value[i + 1 : i + 5]

                if not all([0 <= val <= 1 for val in v]):
                    raise ValueError("Color values must be floats in the range 0-1.")

    def to_json(self):
        return list(self.values)


@attr.s(str=False, frozen=True, kw_only=True)
class RgbaValue(BaseCZMLObject):
    """A color specified as an array of color components [Red, Green, Blue, Alpha]
    where each component is in the range 0-255. If the array has four elements,
    the color is constant.

    If it has five or more elements, they are time-tagged samples arranged as
    [Time, Red, Green, Blue, Alpha, Time, Red, Green, Blue, Alpha, ...], where Time
    is an ISO 8601 date and time string or seconds since epoch.

    """

    values = attr.ib()

    @values.validator
    def _check_values(self, attribute, value):
        if not (len(value) == 4 or len(value) % 5 == 0):
            raise ValueError(
                "Input values must have either 4 or N * 5 values, "
                "where N is the number of time-tagged samples."
            )

        if len(value) == 4:
            if not all([type(val) is int and 0 <= val <= 255 for val in value]):
                raise ValueError("Color values must be integers in the range 0-255.")

        else:
            for i in range(0, len(value), 5):
                v = value[i + 1 : i + 5]

                if not all([type(val) is int and 0 <= val <= 255 for val in v]):
                    raise ValueError(
                        "Color values must be integers in the range 0-255."
                    )

    def to_json(self):
        return list(self.values)


@attr.s(str=False, frozen=True, kw_only=True)
class ReferenceValue(BaseCZMLObject):
    """Represents a reference to another property. References can be used to specify that two properties on different
    objects are in fact, the same property.

    """

    string = attr.ib(default=None)

    @string.validator
    def _check_string(self, attribute, value):
        if not isinstance(value, str):
            raise ValueError("Reference must be a string")
        if "#" not in value:
            raise ValueError(
                "Invalid reference string format. Input must be of the form id#property"
            )

    def to_json(self):
        return self.string


@attr.s(str=False, frozen=True, kw_only=True)
class Cartesian3Value(_TimeTaggedCoords):
    """A three-dimensional Cartesian value specified as [X, Y, Z].

    If the values has three elements, the value is constant.
    If it has four or more elements, they are time-tagged samples
    arranged as [Time, X, Y, Z, Time, X, Y, Z, ...],
    where Time is an ISO 8601 date and time string or seconds since epoch.

    """

    NUM_COORDS = 3


@attr.s(str=False, frozen=True, kw_only=True)
class CartographicRadiansValue(_TimeTaggedCoords):
    """A geodetic, WGS84 position specified as [Longitude, Latitude, Height].

    Longitude and Latitude are in radians and Height is in meters.
    If the array has three elements, the value is constant.
    If it has four or more elements, they are time-tagged samples
    arranged as [Time, Longitude, Latitude, Height, Time, Longitude, Latitude, Height, ...],
    where Time is an ISO 8601 date and time string or seconds since epoch.

    """

    NUM_COORDS = 3


@attr.s(str=False, frozen=True, kw_only=True)
class CartographicDegreesValue(_TimeTaggedCoords):
    """A geodetic, WGS84 position specified as [Longitude, Latitude, Height].

    Longitude and Latitude are in degrees and Height is in meters.
    If the array has three elements, the value is constant.
    If it has four or more elements, they are time-tagged samples
    arranged as [Time, Longitude, Latitude, Height, Time, Longitude, Latitude, Height, ...],
    where Time is an ISO 8601 date and time string or seconds since epoch.

    """

    NUM_COORDS = 3


@attr.s(str=False, frozen=True, kw_only=True)
class StringValue(BaseCZMLObject):
    """A string value.

    The string can optionally vary with time.
    """

    string = attr.ib(default=None)

    def to_json(self):
        return self.string


@attr.s(str=False, frozen=True, kw_only=True)
class CartographicRadiansListValue(BaseCZMLObject):
    """A list of geodetic, WGS84 positions specified as [Longitude, Latitude, Height, Longitude, Latitude, Height, ...],
    where Longitude and Latitude are in radians and Height is in meters."""

    values = attr.ib()

    @values.validator
    def _check_values(self, attribute, value):
        if len(value) % 3 != 0:
            raise ValueError(
                "Invalid values. Input values should be arrays of size 3 * N"
            )

    def to_json(self):
        return list(self.values)


@attr.s(str=False, frozen=True, kw_only=True)
class CartographicDegreesListValue(BaseCZMLObject):
    """A list of geodetic, WGS84 positions specified as [Longitude, Latitude, Height, Longitude, Latitude, Height, ...],
    where Longitude and Latitude are in degrees and Height is in meters."""

    values = attr.ib()

    @values.validator
    def _check_values(self, attribute, value):
        if len(value) % 3 != 0:
            raise ValueError(
                "Invalid values. Input values should be arrays of size 3 * N"
            )

    def to_json(self):
        return list(self.values)


@attr.s(str=False, frozen=True, kw_only=True)
class DistanceDisplayConditionValue(BaseCZMLObject):
    """A value indicating the visibility of an object based on the distance to the camera, specified as two values
    [NearDistance, FarDistance]. If the array has two elements, the value is constant. If it has three or more elements,
    they are time-tagged samples arranged as [Time, NearDistance, FarDistance, Time, NearDistance, FarDistance, ...],
    where Time is an ISO 8601 date and time string or seconds since epoch.
    """

    values = attr.ib(default=None)

    @values.validator
    def _check_values(self, attribute, value):
        if len(value) != 2 and len(value) % 3 != 0:
            raise ValueError(
                "Invalid values. Input values should be arrays of size either 2 or 3 * N"
            )

    def to_json(self):
        return list(self.values)


@attr.s(str=False, frozen=True, kw_only=True)
class NearFarScalarValue(BaseCZMLObject):
    """A near-far scalar value specified as four values [NearDistance, NearValue, FarDistance, FarValue].

     If the array has four elements, the value is constant. If it has five or more elements, they are time-tagged
    samples arranged as [Time, NearDistance, NearValue, FarDistance, FarValue, Time, NearDistance, NearValue,
    FarDistance, FarValue, ...], where Time is an ISO 8601 date and time string or seconds since epoch.
    """

    values = attr.ib(default=None)

    @values.validator
    def _check_values(self, attribute, value):
        if not (len(value) == 4 or len(value) % 5 == 0):
            raise ValueError(
                "Input values must have either 4 or N * 5 values, "
                "where N is the number of time-tagged samples."
            )

    def to_json(self):
        return list(self.values)


@attr.s(str=False, frozen=True, kw_only=True)
class TimeInterval(BaseCZMLObject):
    """A time interval, specified in ISO8601 interval format."""

    _start = attr.ib(default=None)
    _end = attr.ib(default=None)

    def to_json(self):
        if self._start is None:
            start = "0000-00-00T00:00:00Z"
        else:
            start = format_datetime_like(self._start)

        if self._end is None:
            end = "9999-12-31T24:00:00Z"
        else:
            end = format_datetime_like(self._end)

        return "{start}/{end}".format(start=start, end=end)


@attr.s(str=False, frozen=True, kw_only=True)
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


@attr.s(str=False, frozen=True)
class Sequence(BaseCZMLObject):
    """Sequence, list, array of objects."""

    _values = attr.ib()

    def to_json(self):
        return list(self._values)


@attr.s(str=False, frozen=True, kw_only=True)
class UnitQuaternionValue(_TimeTaggedCoords):
    """A set of 4-dimensional coordinates used to represent rotation in 3-dimensional space.

    It's specified as [X, Y, Z, W]. If the array has four elements, the value is constant.
    If it has five or more elements, they are time-tagged samples arranged as
    [Time, X, Y, Z, W, Time, X, Y, Z, W, ...],
    where Time is an ISO 8601 date and time string or seconds since epoch.

    """

    NUM_COORDS = 4
