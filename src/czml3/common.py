import datetime as dt

from pydantic import BaseModel, field_validator

from .enums import InterpolationAlgorithms
from .types import Sequence, format_datetime_like


class Deletable(BaseModel):
    """A property whose value may be deleted."""

    delete: None | bool = None


class Interpolatable(BaseModel):
    """A property whose value may be determined by interpolating.

    The interpolation happens over provided time-tagged samples.
    """

    epoch: None | str | dt.datetime | Sequence = None
    interpolationAlgorithm: None | InterpolationAlgorithms | Sequence = None
    interpolationDegree: None | int | Sequence = None

    @field_validator("epoch")
    @classmethod
    def check(cls, e):
        return format_datetime_like(e)
