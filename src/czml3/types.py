import datetime as dt
import re
import sys
from typing import Any

from dateutil.parser import isoparse as parse_iso_date
from pydantic import (
    Field,
    field_validator,
    model_serializer,
    model_validator,
)

from .base import BaseCZMLObject
from .constants import ISO8601_FORMAT_Z

if sys.version_info[1] >= 11:
    from typing import Self
else:
    from typing_extensions import Self

TYPE_MAPPING = {bool: "boolean"}


def get_color(color):
    """Determines if the input is a valid color"""
    if color is None or (
        isinstance(color, list)
        and all(issubclass(type(v), int | float) for v in color)
        and len(color) == 4
        and (all(0 <= v <= 255 for v in color) or all(0 <= v <= 1 for v in color))
    ):
        return color
    elif (
        isinstance(color, list)
        and all(issubclass(type(v), int | float) for v in color)
        and len(color) == 3
        and all(0 <= v <= 255 for v in color)
    ):
        return color + [255]
    # rgbf or rgbaf
    # if (
    #     isinstance(color, list)
    #     and all(issubclass(type(v), int | float) for v in color)
    #     and (3 <= len(color) <= 4)
    #     and not all(0 <= v <= 1 for v in color)
    # ):
    #     raise TypeError("RGBF or RGBAF values must be between 0 and 1")
    elif (
        isinstance(color, list)
        and all(issubclass(type(v), int | float) for v in color)
        and len(color) == 3
        and all(0 <= v <= 1 for v in color)
    ):
        return color + [1.0]
    # Hexadecimal RGBA
    # elif issubclass(type(color), int) and not (0 <= color <= 0xFFFFFFFF):
    #     raise TypeError("Hexadecimal RGBA not valid")
    elif (
        issubclass(type(color), int) and (0 <= color <= 0xFFFFFFFF) and color > 0xFFFFFF
    ):
        return [
            (color & 0xFF000000) >> 24,
            (color & 0x00FF0000) >> 16,
            (color & 0x0000FF00) >> 8,
            (color & 0x000000FF) >> 0,
        ]
    elif issubclass(type(color), int) and (0 <= color <= 0xFFFFFFFF):
        return [
            (color & 0xFF0000) >> 16,
            (color & 0x00FF00) >> 8,
            (color & 0x0000FF) >> 0,
            0xFF,
        ]
    # RGBA string
    elif isinstance(color, str):
        n = int(color.rsplit("#")[-1], 16)
        if not (0 <= n <= 0xFFFFFFFF):
            raise TypeError("RGBA string not valid")
        if n > 0xFFFFFF:
            return [
                (n & 0xFF000000) >> 24,
                (n & 0x00FF0000) >> 16,
                (n & 0x0000FF00) >> 8,
                (n & 0x000000FF) >> 0,
            ]
        else:
            return [
                (n & 0xFF0000) >> 16,
                (n & 0x00FF00) >> 8,
                (n & 0x0000FF) >> 0,
                0xFF,
            ]
    raise TypeError("Colour type not supported")


def check_reference(r):
    if r is None:
        return
    elif re.search(r"^.+#.+$", r) is None:
        raise TypeError(
            "Invalid reference string format. Input must be of the form id#property"
        )


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
        result = dt_object.strftime(ISO8601_FORMAT_Z)

    else:
        result = dt_object.strftime(ISO8601_FORMAT_Z)

    return result


class FontValue(BaseCZMLObject):
    """A font, specified using the same syntax as the CSS "font" property."""

    font: str

    @model_serializer
    def custom_serializer(self):
        return self.font


class RgbafValue(BaseCZMLObject):
    """A color specified as an array of color components [Red, Green, Blue, Alpha]
     where each component is in the range 0.0-1.0. If the array has four elements,
    the color is constant. If it has five or more elements, they are time-tagged
    samples arranged as [Time, Red, Green, Blue, Alpha, Time, Red, Green, Blue, Alpha, ...],
    where Time is an ISO 8601 date and time string or seconds since epoch.

    """

    values: list[float] | list[int]

    @model_validator(mode="after")
    def _check_values(self) -> Self:
        num_coords = 4
        if not (
            len(self.values) == num_coords or len(self.values) % (num_coords + 1) == 0
        ):
            raise TypeError(
                f"Input values must have either {num_coords} or N * {num_coords + 1} values, "
                "where N is the number of time-tagged samples."
            )
        if len(self.values) == num_coords:
            if not all(0 <= val <= 1 for val in self.values):
                raise TypeError("Color values must be floats in the range 0-1.")

        else:
            for i in range(0, len(self.values), num_coords + 1):
                v = self.values[i + 1 : i + num_coords + 1]

                if not all(0 <= val <= 1 for val in v):
                    raise TypeError("Color values must be floats in the range 0-1.")
        return self

    @model_serializer
    def custom_serializer(self):
        return list(self.values)


class RgbaValue(BaseCZMLObject):
    """A color specified as an array of color components [Red, Green, Blue, Alpha]
    where each component is in the range 0-255. If the array has four elements,
    the color is constant.

    If it has five or more elements, they are time-tagged samples arranged as
    [Time, Red, Green, Blue, Alpha, Time, Red, Green, Blue, Alpha, ...], where Time
    is an ISO 8601 date and time string or seconds since epoch.

    """

    values: list[float] | list[int]

    @model_validator(mode="after")
    def _check_values(self) -> Self:
        num_coords = 4
        if not (
            len(self.values) == num_coords or len(self.values) % (num_coords + 1) == 0
        ):
            raise TypeError(
                f"Input values must have either {num_coords} or N * {num_coords + 1} values, "
                "where N is the number of time-tagged samples."
            )

        if len(self.values) == num_coords and not all(
            isinstance(val, int) and 0 <= val <= 255 for val in self.values
        ):
            raise TypeError("Color values must be integers in the range 0-255.")

        else:
            for i in range(0, len(self.values), num_coords + 1):
                v = self.values[i + 1 : i + num_coords + 1]

                if not all(isinstance(val, int) and 0 <= val <= 255 for val in v):
                    raise TypeError("Color values must be integers in the range 0-255.")
        return self

    @model_serializer
    def custom_serializer(self):
        return self.values


class ReferenceValue(BaseCZMLObject):
    """Represents a reference to another property. References can be used to specify that two properties on different
    objects are in fact, the same property.

    """

    string: str

    @field_validator("string")
    @classmethod
    def _check_string(cls, v):
        if "#" not in v:
            raise TypeError(
                "Invalid reference string format. Input must be of the form id#property"
            )
        return v

    @model_serializer
    def custom_serializer(self):
        return self.string


class Cartesian3Value(BaseCZMLObject):
    """A three-dimensional Cartesian value specified as [X, Y, Z].

    If the values has three elements, the value is constant.
    If it has four or more elements, they are time-tagged samples
    arranged as [Time, X, Y, Z, Time, X, Y, Z, ...],
    where Time is an ISO 8601 date and time string or seconds since epoch.

    """

    values: None | list[Any] = Field(default=None)

    @model_validator(mode="after")
    def _check_values(self) -> Self:
        if self.values is None:
            return self
        num_coords = 3
        if not (
            len(self.values) == num_coords or len(self.values) % (num_coords + 1) == 0
        ):
            raise TypeError(
                f"Input values must have either {num_coords} or N * {num_coords + 1} values, "
                "where N is the number of time-tagged samples."
            )
        return self

    @model_serializer
    def custom_serializer(self) -> list[Any]:
        if self.values is None:
            return []
        return list(self.values)


class Cartesian2Value(BaseCZMLObject):
    """A two-dimensional Cartesian value specified as [X, Y].

    If the values has two elements, the value is constant.
    If it has three or more elements, they are time-tagged samples
    arranged as [Time, X, Y, Time, X, Y, ...],
    where Time is an ISO 8601 date and time string or seconds since epoch.

    """

    values: None | list[Any] = Field(default=None)

    @model_validator(mode="after")
    def _check_values(self) -> Self:
        if self.values is None:
            return self
        num_coords = 2
        if not (
            len(self.values) == num_coords or len(self.values) % (num_coords + 1) == 0
        ):
            raise TypeError(
                f"Input values must have either {num_coords} or N * {num_coords + 1} values, "
                "where N is the number of time-tagged samples."
            )
        return self

    @model_serializer
    def custom_serializer(self):
        if self.values is None:
            return {}
        return {"cartesian2": list(self.values)}


class CartographicRadiansValue(BaseCZMLObject):
    """A geodetic, WGS84 position specified as [Longitude, Latitude, Height].

    Longitude and Latitude are in radians and Height is in meters.
    If the array has three elements, the value is constant.
    If it has four or more elements, they are time-tagged samples
    arranged as [Time, Longitude, Latitude, Height, Time, Longitude, Latitude, Height, ...],
    where Time is an ISO 8601 date and time string or seconds since epoch.

    """

    values: None | list[Any] = Field(default=None)

    @model_validator(mode="after")
    def _check_values(self) -> Self:
        if self.values is None:
            return self
        num_coords = 3
        if not (
            len(self.values) == num_coords or len(self.values) % (num_coords + 1) == 0
        ):
            raise TypeError(
                f"Input values must have either {num_coords} or N * {num_coords + 1} values, "
                "where N is the number of time-tagged samples."
            )
        return self

    @model_serializer
    def custom_serializer(self):
        if self.values is None:
            return []
        return list(self.values)


class CartographicDegreesValue(BaseCZMLObject):
    """A geodetic, WGS84 position specified as [Longitude, Latitude, Height].

    Longitude and Latitude are in degrees and Height is in meters.
    If the array has three elements, the value is constant.
    If it has four or more elements, they are time-tagged samples
    arranged as [Time, Longitude, Latitude, Height, Time, Longitude, Latitude, Height, ...],
    where Time is an ISO 8601 date and time string or seconds since epoch.

    """

    values: None | list[Any] = Field(default=None)

    @model_validator(mode="after")
    def _check_values(self) -> Self:
        if self.values is None:
            return self
        num_coords = 3
        if not (
            len(self.values) == num_coords or len(self.values) % (num_coords + 1) == 0
        ):
            raise TypeError(
                f"Input values must have either {num_coords} or N * {num_coords + 1} values, "
                "where N is the number of time-tagged samples."
            )
        return self

    @model_serializer
    def custom_serializer(self) -> list[Any]:
        if self.values is None:
            return []
        return self.values


class StringValue(BaseCZMLObject):
    """A string value.

    The string can optionally vary with time.
    """

    string: str

    @model_serializer
    def custom_serializer(self) -> str:
        return self.string


class CartographicRadiansListValue(BaseCZMLObject):
    """A list of geodetic, WGS84 positions specified as [Longitude, Latitude, Height, Longitude, Latitude, Height, ...],
    where Longitude and Latitude are in radians and Height is in meters."""

    values: list[float] | list[int]

    @model_validator(mode="after")
    def _check_values(self) -> Self:
        num_coords = 3
        if len(self.values) % num_coords != 0:
            raise TypeError(
                f"Invalid values. Input values should be arrays of size {num_coords} * N"
            )
        return self

    @model_serializer
    def custom_serializer(self):
        return list(self.values)


class CartographicDegreesListValue(BaseCZMLObject):
    """A list of geodetic, WGS84 positions specified as [Longitude, Latitude, Height, Longitude, Latitude, Height, ...],
    where Longitude and Latitude are in degrees and Height is in meters."""

    values: list[float] | list[int]

    @model_validator(mode="after")
    def _check_values(self) -> Self:
        num_coords = 3
        if len(self.values) % num_coords != 0:
            raise TypeError(
                f"Invalid values. Input values should be arrays of size {num_coords} * N"
            )
        return self

    @model_serializer
    def custom_serializer(self):
        return list(self.values)


class DistanceDisplayConditionValue(BaseCZMLObject):
    """A value indicating the visibility of an object based on the distance to the camera, specified as two values
    [NearDistance, FarDistance]. If the array has two elements, the value is constant. If it has three or more elements,
    they are time-tagged samples arranged as [Time, NearDistance, FarDistance, Time, NearDistance, FarDistance, ...],
    where Time is an ISO 8601 date and time string or seconds since epoch.
    """

    values: list[float] | list[int]

    @model_validator(mode="after")
    def _check_values(self) -> Self:
        num_coords = 2
        if len(self.values) != num_coords and len(self.values) % (num_coords + 1) != 0:
            raise TypeError(
                f"Invalid values. Input values should be arrays of size either {num_coords} or {num_coords + 1} * N"
            )
        return self

    @model_serializer
    def custom_serializer(self):
        return list(self.values)


class NearFarScalarValue(BaseCZMLObject):
    """A near-far scalar value specified as four values [NearDistance, NearValue, FarDistance, FarValue].

     If the array has four elements, the value is constant. If it has five or more elements, they are time-tagged
    samples arranged as [Time, NearDistance, NearValue, FarDistance, FarValue, Time, NearDistance, NearValue,
    FarDistance, FarValue, ...], where Time is an ISO 8601 date and time string or seconds since epoch.
    """

    values: list[float] | list[int]

    @model_validator(mode="after")
    def _check_values(self) -> Self:
        num_coords = 4
        if not (
            len(self.values) == num_coords or len(self.values) % (num_coords + 1) == 0
        ):
            raise TypeError(
                f"Input values must have either {num_coords} or N * {num_coords + 1} values, "
                "where N is the number of time-tagged samples."
            )
        return self

    @model_serializer
    def custom_serializer(self):
        return list(self.values)


class TimeInterval(BaseCZMLObject):
    """A time interval, specified in ISO8601 interval format."""

    start: str | dt.datetime = Field(default="0001-01-01T00:00:00Z")
    end: str | dt.datetime = Field(default="9999-12-31T23:59:59Z")

    @field_validator("start", "end")
    @classmethod
    def format_time(cls, time):
        return format_datetime_like(time)

    @model_serializer
    def custom_serializer(self) -> str:
        return f"{self.start}/{self.end}"


class IntervalValue(BaseCZMLObject):
    """Value over some interval."""

    start: str | dt.datetime
    end: str | dt.datetime
    value: Any = Field(default=None)

    @model_serializer
    def custom_serializer(self) -> dict[str, Any]:
        obj_dict = {
            "interval": TimeInterval(start=self.start, end=self.end).model_dump(
                exclude_none=True
            )
        }

        if isinstance(self.value, BaseCZMLObject):
            obj_dict.update(self.value.model_dump(exclude_none=True))
        elif isinstance(self.value, list) and all(
            isinstance(v, BaseCZMLObject) for v in self.value
        ):
            for value in self.value:
                obj_dict.update(value.model_dump())
        else:
            key = TYPE_MAPPING[type(self.value)]
            obj_dict[key] = self.value

        return obj_dict


class Sequence(BaseCZMLObject):
    """Sequence, list, array of objects."""

    values: list[Any]

    @model_serializer
    def custom_serializer(self) -> list[Any]:
        return list(self.values)


class UnitQuaternionValue(BaseCZMLObject):
    """A set of 4-dimensional coordinates used to represent rotation in 3-dimensional space.

    It's specified as [X, Y, Z, W]. If the array has four elements, the value is constant.
    If it has five or more elements, they are time-tagged samples arranged as
    [Time, X, Y, Z, W, Time, X, Y, Z, W, ...],
    where Time is an ISO 8601 date and time string or seconds since epoch.

    """

    values: list[float] | list[int]

    @model_validator(mode="after")
    def _check_values(self) -> Self:
        num_coords = 4
        if len(self.values) % num_coords != 0:
            raise TypeError(
                f"Invalid values. Input values should be arrays of size {num_coords} * N"
            )
        return self

    @model_serializer
    def custom_serializer(self):
        return list(self.values)


class EpochValue(BaseCZMLObject):
    """A value representing a time epoch."""

    value: str | dt.datetime

    @model_serializer
    def custom_serializer(self):
        return {"epoch": format_datetime_like(self.value)}


class NumberValue(BaseCZMLObject):
    """A single number, or a list of number pairs signifying the time and representative value."""

    values: int | float | list[float] | list[int]

    @model_serializer
    def custom_serializer(self):
        if isinstance(self.values, int | float):
            return {"number": self.values}
        return {"number": list(self.values)}
