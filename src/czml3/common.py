# noinspection PyPep8Naming
import datetime as dt

import attr

from .enums import InterpolationAlgorithms
from .meta import enum_fields


@attr.s(str=False, frozen=True, kw_only=True, field_transformer=enum_fields)
class Deletable:
    """A property whose value may be deleted."""

    delete: bool = attr.ib(default=None)


# noinspection PyPep8Naming
@attr.s(str=False, frozen=True, kw_only=True, field_transformer=enum_fields)
class Interpolatable:
    """A property whose value may be determined by interpolating.

    The interpolation happens over provided time-tagged samples.
    """

    epoch: dt.datetime = attr.ib(default=None)
    interpolationAlgorithm: InterpolationAlgorithms = attr.ib(default=None)
    interpolationDegree: int = attr.ib(default=None)
