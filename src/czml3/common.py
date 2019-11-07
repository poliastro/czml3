# noinspection PyPep8Naming
import datetime as dt

import attr

from .enums import HorizontalOrigins, InterpolationAlgorithms, VerticalOrigins


@attr.s(repr=False, frozen=True, kw_only=True)
class Deletable:
    """A property whose value may be deleted."""

    delete: bool = attr.ib(default=None)


# noinspection PyPep8Naming
@attr.s(repr=False, frozen=True, kw_only=True)
class Interpolatable:
    """A property whose value may be determined by interpolating.

    The interpolation happens over provided time-tagged samples.
    """

    epoch: dt.datetime = attr.ib(default=None)
    interpolationAlgorithm: InterpolationAlgorithms = attr.ib(default=None)
    interpolationDegree: int = attr.ib(default=None)


# noinspection PyPep8Naming
@attr.s(repr=False, frozen=True, kw_only=True)
class HasAlignment:
    """A property that can be horizontally or vertically aligned."""

    horizontalOrigin: HorizontalOrigins = attr.ib(default=None)
    verticalOrigin: VerticalOrigins = attr.ib(default=None)
