# noinspection PyPep8Naming
import datetime as dt

from czml3.enums import HorizontalOrigins, InterpolationAlgorithms, VerticalOrigins


class Deletable:
    """A property whose value may be deleted."""

    delete: bool


# noinspection PyPep8Naming
class Interpolatable:
    """A property whose value may be determined by interpolating.

    The interpolation happens over provided time-tagged samples.
    """

    epoch: dt.datetime
    interpolation_algorithm: InterpolationAlgorithms
    interpolation_degree: int


# noinspection PyPep8Naming
class HasAlignment:
    """A property that can be horizontally or vertically aligned."""

    horizontal_origin: HorizontalOrigins
    vertical_origin: VerticalOrigins
