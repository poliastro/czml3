from typing import Optional

from w3lib.url import is_url, parse_data_uri

from .base import BaseCZMLObject
from .common import DeletableProperty


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
    """A string value. The string can optionally vary with time."""

    def __init__(self, *, delete: Optional[bool] = None, string: Optional[str] = None):
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

    def __init__(self, *, delete: Optional[bool] = None, uri: Optional[str] = None):
        super().__init__(delete=delete)

        try:
            parse_data_uri(uri)
        except ValueError:
            if not is_url(uri):
                raise ValueError("uri must be a URL or a data URI")

        self._uri = uri

    @property
    def uri(self):
        """The URI value."""
        return self._uri

    def to_json(self):
        return self.uri
