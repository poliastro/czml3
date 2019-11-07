# noinspection PyPep8Naming
import attr


@attr.s(repr=False, frozen=True, kw_only=True)
class Deletable:
    """A property whose value may be deleted."""

    delete = attr.ib(default=None)


# noinspection PyPep8Naming
@attr.s(repr=False, frozen=True, kw_only=True)
class Interpolatable:
    """A property whose value may be determined by interpolating.

    The interpolation happens over provided time-tagged samples.
    """

    epoch = attr.ib(default=None)
    interpolationAlgorithm = attr.ib(default=None)
    interpolationDegree = attr.ib(default=None)


# noinspection PyPep8Naming
@attr.s(repr=False, frozen=True, kw_only=True)
class HasAlignment:
    """A property that can be horizontally or vertically aligned."""

    horizontalOrigin = attr.ib(default=None)
    verticalOrigin = attr.ib(default=None)
