# noinspection PyPep8Naming
from __future__ import annotations

import datetime as dt

import attr

from .enums import InterpolationAlgorithms


@attr.s(str=False, frozen=True, kw_only=True)
class Deletable:
    """A property whose value may be deleted."""

    delete: bool | None = attr.ib(default=None)


# noinspection PyPep8Naming
@attr.s(str=False, frozen=True, kw_only=True)
class Interpolatable:
    """A property whose value may be determined by interpolating.

    The interpolation happens over provided time-tagged samples.
    """

    epoch: dt.datetime | None = attr.ib(default=None)
    interpolationAlgorithm: InterpolationAlgorithms | None = attr.ib(default=None)
    interpolationDegree: int | None = attr.ib(default=None)
