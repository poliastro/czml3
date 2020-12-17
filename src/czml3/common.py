# noinspection PyPep8Naming
import datetime as dt
from typing import Optional

import attr

from .enums import HorizontalOrigins, InterpolationAlgorithms, VerticalOrigins


@attr.s(auto_attribs=True, repr=False, frozen=True, kw_only=True)
class Deletable:
    """A property whose value may be deleted."""

    delete: Optional[bool] = None


# noinspection PyPep8Naming
@attr.s(auto_attribs=True, repr=False, frozen=True, kw_only=True)
class Interpolatable:
    """A property whose value may be determined by interpolating.

    The interpolation happens over provided time-tagged samples.
    """

    epoch: Optional[dt.datetime] = None
    interpolationAlgorithm: Optional[InterpolationAlgorithms] = None
    interpolationDegree: Optional[int] = None


# noinspection PyPep8Naming
@attr.s(auto_attribs=True, repr=False, frozen=True, kw_only=True)
class HasAlignment:
    """A property that can be horizontally or vertically aligned."""

    horizontalOrigin: Optional[HorizontalOrigins] = None
    verticalOrigin: Optional[VerticalOrigins] = None
