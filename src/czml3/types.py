import datetime as dt

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


class FontValue(BaseCZMLObject):
    """A font, specified using the same syntax as the CSS "font" property."""

    def __init__(self, *, font=None):
        self._font = font

    @property
    def font(self):
        """The font to use for the label."""
        return self._font

    def to_json(self):
        return self._font


class RgbafValue(BaseCZMLObject):
    """A color specified as an array of color components [Red, Green, Blue, Alpha]
     where each component is in the range 0.0-1.0. If the array has four elements,
    the color is constant. If it has five or more elements, they are time-tagged
    samples arranged as [Time, Red, Green, Blue, Alpha, Time, Red, Green, Blue, Alpha, ...],
    where Time is an ISO 8601 date and time string or seconds since epoch.

    """

    def __init__(self, *, values):
        if not (len(values) == 4 or len(values) % 5 == 0):
            raise ValueError(
                "Input values must have either 4 or N * 5 values, "
                "where N is the number of time-tagged samples."
            )

        if len(values) == 4:
            if not all([0 <= val <= 1 for val in values]):
                raise ValueError("Color values must be floats in the range 0-1.")

        else:
            for i in range(0, len(values), 5):
                v = values[i + 1 : i + 5]

                if not all([0 <= val <= 1 for val in v]):
                    raise ValueError("Color values must be floats in the range 0-1.")

        self._values = values

    @property
    def values(self):
        return self._values

    def to_json(self):
        return list(self.values)


class RgbaValue(BaseCZMLObject):
    """A color specified as an array of color components [Red, Green, Blue, Alpha]
     where each component is in the range 0-255. If the array has four elements,
     the color is constant.

      If it has five or more elements, they are time-tagged samples arranged as
     [Time, Red, Green, Blue, Alpha, Time, Red, Green, Blue, Alpha, ...], where Time
     is an ISO 8601 date and time string or seconds since epoch.

     """

    def __init__(self, *, values):
        if not (len(values) == 4 or len(values) % 5 == 0):
            raise ValueError(
                "Input values must have either 4 or N * 5 values, "
                "where N is the number of time-tagged samples."
            )

        if len(values) == 4:
            if not all([type(val) is int and 0 <= val <= 255 for val in values]):
                raise ValueError("Color values must be integers in the range 0-255.")

        else:
            for i in range(0, len(values), 5):
                v = values[i + 1 : i + 5]

                if not all([type(val) is int and 0 <= val <= 255 for val in v]):
                    raise ValueError(
                        "Color values must be integers in the range 0-255."
                    )

        self._values = values

    @property
    def values(self):
        return self._values

    def to_json(self):
        return list(self.values)


class Cartesian3Value(BaseCZMLObject):
    """A three-dimensional Cartesian value specified as [X, Y, Z].

    If the values has three elements, the value is constant.
    If it has four or more elements, they are time-tagged samples
    arranged as [Time, X, Y, Z, Time, X, Y, Z, ...],
    where Time is an ISO 8601 date and time string or seconds since epoch.

    """

    def __init__(self, *, values):
        if not (len(values) == 3 or len(values) % 4 == 0):
            raise ValueError(
                "Input values must have either 3 or N * 4 values, "
                "where N is the number of time-tagged samples."
            )

        self._values = values

    @property
    def values(self):
        return self._values

    def to_json(self):
        return list(self.values)


class StringValue(BaseCZMLObject, Deletable):
    """A string value.

    The string can optionally vary with time.
    """

    def __init__(self, *, delete=None, string=None):
        self._delete = delete
        self._string = string

    @property
    def string(self):
        """The string value."""
        return self._string

    def to_json(self):
        return self.string


class Uri(BaseCZMLObject, Deletable):
    """A URI value.

    The URI can optionally vary with time.
    """

    def __init__(self, *, delete=None, uri=None):
        try:
            parse_data_uri(uri)
        except ValueError as e:
            if not is_url(uri):
                raise ValueError("uri must be a URL or a data URI") from e

        self._delete = delete
        self._uri = uri

    @property
    def uri(self):
        """The URI value."""
        return self._uri

    def to_json(self):
        return self.uri


class TimeInterval(BaseCZMLObject):
    """A time interval, specified in ISO8601 interval format."""

    def __init__(self, *, start=None, end=None):
        self._start = format_datetime_like(start)
        self._end = format_datetime_like(end)

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


class IntervalValue(BaseCZMLObject):
    """Value over some interval."""

    def __init__(self, *, start, end, value):
        self._interval = TimeInterval(start=start, end=end)
        self._value = value

    def to_json(self):
        obj_dict = {"interval": self._interval}

        try:
            obj_dict.update(**self._value.to_json())
        except AttributeError:
            key = TYPE_MAPPING[type(self._value)]
            obj_dict[key] = self._value

        return obj_dict


class Sequence(BaseCZMLObject):
    """Sequence, list, array of objects."""

    def __init__(self, values):
        self._values = values

    def to_json(self):
        return list(self._values)
