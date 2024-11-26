import datetime as dt
from typing import Union

from pydantic import BaseModel, field_validator

from .enums import InterpolationAlgorithms
from .types import format_datetime_like


class Deletable(BaseModel):
    """A property whose value may be deleted."""

    delete: Union[None, bool] = None


class Interpolatable(BaseModel):
    """A property whose value may be determined by interpolating.

    The interpolation happens over provided time-tagged samples.
    """

    epoch: Union[None, str, dt.datetime] = None
    interpolationAlgorithm: Union[None, InterpolationAlgorithms] = None
    interpolationDegree: Union[None, int] = None

    @field_validator("epoch")
    @classmethod
    def check(cls, e):
        return format_datetime_like(e)
