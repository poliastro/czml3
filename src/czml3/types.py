import datetime as dt

from w3lib.url import is_url, parse_data_uri

from .base import BaseCZMLObject
from .common import DeletableProperty
from .constants import ISO8601_FORMAT_Z

TYPE_MAPPING = {bool: "boolean"}


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


class StringValue(BaseCZMLObject, DeletableProperty):
    """A string value.

    The string can optionally vary with time.
    """

    def __init__(self, *, delete=None, string=None):
        super().__init__(delete=delete)
        self._string = string

    @property
    def string(self):
        """The string value."""
        return self._string

    def to_json(self):
        return self.string


class Uri(BaseCZMLObject, DeletableProperty):
    """A URI value.

    The URI can optionally vary with time.
    """

    def __init__(self, *, delete=None, uri=None):
        super().__init__(delete=delete)

        try:
            parse_data_uri(uri)
        except ValueError as e:
            if not is_url(uri):
                raise ValueError("uri must be a URL or a data URI") from e

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
        self._start = start
        self._end = end

    def to_json(self):
        if self._start is None:
            start = "0000-00-00T00:00:00Z"
        else:
            start = self._start.astimezone(dt.timezone.utc).strftime(ISO8601_FORMAT_Z)

        if self._end is None:
            end = "9999-12-31T24:00:00Z"
        else:
            end = self._end.astimezone(dt.timezone.utc).strftime(ISO8601_FORMAT_Z)

        return "{start}/{end}".format(start=start, end=end)


class IntervalValue(BaseCZMLObject):
    """Value over some interval."""

    def __init__(self, *, start, end, value):
        self._interval = TimeInterval(start=start, end=end)
        self._value = value

    @property
    def interval(self):
        return self._interval

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
