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


def get_color(color: None | list[float], max_val: float) -> list[float] | None:
    """Determines if the input is a valid color"""
    if isinstance(color, list) and len(color) == 0:
        raise ValueError("Length of colours must be non-zero")
    if color is None or (
        isinstance(color, list)
        and len(color) == 4
        and all(0 <= v <= max_val for v in color)
    ):
        return color
    elif (
        isinstance(color, list)
        and len(color) == 3
        and all(0 <= v <= max_val for v in color)
    ):
        return color + [max_val]
    raise TypeError("Colour type not supported")


def check_list_of_values(num_points: int, values: list[Any]):
    """Values that support [X,Y,Z,X,Y,Z,...]"""
    if len(values) <= 0:
        raise ValueError("No values present")
    if len(values) % num_points != 0:
        raise TypeError(
            f"Input values must have either {num_points} or N * {num_points} values, where N is the number of samples."
        )


def check_values(num_points: int, values: list[Any]):
    """Values that support [X,Y,Z] or [Time,X,Y,Z,Time,X,Y,Z,...]"""
    if len(values) <= 0:
        raise ValueError("No values present")
    if not (len(values) % (num_points) == 0 or len(values) % (num_points + 1) == 0):
        raise TypeError(
            f"Input values must have either {num_points} or N * {num_points + 1} values, where N is the number of time-tagged samples."
        )


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

    values: list[float]

    @field_validator("values")
    @classmethod
    def get_color_from_values(cls, r):
        return get_color(r, 1.0)

    @model_validator(mode="after")
    def _check_values(self) -> Self:
        num_coords = 4
        check_values(num_coords, self.values)
        if (
            len(self.values) % num_coords == 0
            and not all(0 <= val <= 1 for val in self.values)
            or (
                len(self.values) % (num_coords + 1) == 0
                and not all(0 <= val <= 1 for val in self.values[1::5])
                and not all(0 <= val <= 1 for val in self.values[2::5])
                and not all(0 <= val <= 1 for val in self.values[3::5])
                and not all(0 <= val <= 1 for val in self.values[4::5])
            )
        ):
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

    values: list[float]

    @field_validator("values")
    @classmethod
    def get_color_from_values(cls, r):
        return get_color(r, 255.0)

    @model_validator(mode="after")
    def _check_values(self) -> Self:
        num_coords = 4
        check_values(num_coords, self.values)
        if (
            len(self.values) % num_coords == 0
            and not all(0 <= val <= 255 for val in self.values)
            or (
                len(self.values) % (num_coords + 1) == 0
                and not all(0 <= val <= 255 for val in self.values[1::5])
                and not all(0 <= val <= 255 for val in self.values[2::5])
                and not all(0 <= val <= 255 for val in self.values[3::5])
                and not all(0 <= val <= 255 for val in self.values[4::5])
            )
        ):
            raise TypeError("Color values must be floats in the range 0-255.")
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

    values: list[float] = Field(default=None)

    @model_validator(mode="after")
    def _check_values(self) -> Self:
        check_values(3, self.values)
        return self

    @model_serializer
    def custom_serializer(self) -> list[float]:
        return list(self.values)


class Cartesian3ListValue(BaseCZMLObject):
    """A list of three-dimensional Cartesian values specified as [X, Y, Z, X, Y, Z, ...]"""

    values: list[float] = Field(default=None)

    @model_validator(mode="after")
    def _check_values(self) -> Self:
        check_list_of_values(3, self.values)
        return self

    @model_serializer
    def custom_serializer(self) -> list[float]:
        return list(self.values)


class Cartesian2Value(BaseCZMLObject):
    """A two-dimensional Cartesian value specified as [X, Y].

    If the values has two elements, the value is constant.
    If it has three or more elements, they are time-tagged samples
    arranged as [Time, X, Y, Time, X, Y, ...],
    where Time is an ISO 8601 date and time string or seconds since epoch.

    """

    values: list[float] = Field(default=None)

    @model_validator(mode="after")
    def _check_values(self) -> Self:
        check_values(2, self.values)
        return self

    @model_serializer
    def custom_serializer(self):
        return {"cartesian2": list(self.values)}


class CartographicRadiansValue(BaseCZMLObject):
    """A geodetic, WGS84 position specified as [Longitude, Latitude, Height].

    Longitude and Latitude are in radians and Height is in meters.
    If the array has three elements, the value is constant.
    If it has four or more elements, they are time-tagged samples
    arranged as [Time, Longitude, Latitude, Height, Time, Longitude, Latitude, Height, ...],
    where Time is an ISO 8601 date and time string or seconds since epoch.

    """

    values: list[float] = Field(default=None)

    @model_validator(mode="after")
    def _check_values(self) -> Self:
        check_values(3, self.values)
        return self

    @model_serializer
    def custom_serializer(self):
        return list(self.values)


class CartographicDegreesValue(BaseCZMLObject):
    """A geodetic, WGS84 position specified as [Longitude, Latitude, Height].

    Longitude and Latitude are in degrees and Height is in meters.
    If the array has three elements, the value is constant.
    If it has four or more elements, they are time-tagged samples
    arranged as [Time, Longitude, Latitude, Height, Time, Longitude, Latitude, Height, ...],
    where Time is an ISO 8601 date and time string or seconds since epoch.

    """

    values: list[float] = Field(default=None)

    @model_validator(mode="after")
    def _check_values(self) -> Self:
        check_values(3, self.values)
        return self

    @model_serializer
    def custom_serializer(self) -> list[float]:
        return self.values


class Cartesian3VelocityValue(BaseCZMLObject):
    """A geodetic, WGS84 position specified as [Longitude, Latitude, Height].

    Longitude and Latitude are in degrees and Height is in meters.
    If the array has three elements, the value is constant.
    If it has four or more elements, they are time-tagged samples
    arranged as [Time, Longitude, Latitude, Height, Time, Longitude, Latitude, Height, ...],
    where Time is an ISO 8601 date and time string or seconds since epoch.

    """

    values: list[float] = Field(default=None)

    @model_validator(mode="after")
    def _check_values(self) -> Self:
        check_values(6, self.values)
        return self

    @model_serializer
    def custom_serializer(self) -> list[float]:
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

    values: list[float]

    @model_validator(mode="after")
    def _check_values(self) -> Self:
        check_list_of_values(3, self.values)
        return self

    @model_serializer
    def custom_serializer(self):
        return list(self.values)


class CartographicDegreesListValue(BaseCZMLObject):
    """A list of geodetic, WGS84 positions specified as [Longitude, Latitude, Height, Longitude, Latitude, Height, ...],
    where Longitude and Latitude are in degrees and Height is in meters."""

    values: list[float]

    @model_validator(mode="after")
    def _check_values(self) -> Self:
        check_list_of_values(3, self.values)
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

    values: list[float]

    @model_validator(mode="after")
    def _check_values(self) -> Self:
        check_values(2, self.values)
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

    values: list[float]

    @model_validator(mode="after")
    def _check_values(self) -> Self:
        check_values(4, self.values)
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

    values: list[float]

    @model_validator(mode="after")
    def _check_values(self) -> Self:
        check_values(4, self.values)
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

    values: int | float | list[float] | int | list[int]

    @model_serializer
    def custom_serializer(self):
        if isinstance(self.values, int | float):
            return {"number": self.values}
        return {"number": list(self.values)}
