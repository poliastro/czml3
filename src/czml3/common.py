# noinspection PyPep8Naming
class Deletable:
    """A property whose value may be deleted."""

    @property
    def delete(self):
        """
        Whether the client should delete existing samples or interval data for this property.

        Data will be deleted for the containing interval,
        or if there is no containing interval,
        then all data.
        If true,
        all other properties in this property
        will be ignored.
        """
        return self._delete


# noinspection PyPep8Naming
class Interpolatable:
    """A property whose value may be determined by interpolating.

    The interpolation happens over provided time-tagged samples.
    """

    @property
    def epoch(self):
        """The epoch to use for times specified as seconds since an epoch."""
        return self._epoch

    @property
    def interpolationAlgorithm(self):
        """The interpolation algorithm to use when interpolating."""
        return self._interpolation_algorithm

    @property
    def interpolationDegree(self):
        """The degree of interpolation to use when interpolating."""
        return self._interpolation_degree


# noinspection PyPep8Naming
class HasAlignment:
    """A property that can be horizontally or vertically aligned."""

    @property
    def horizontalOrigin(self):
        """The horizontal origin of the object.

        It controls whether the object is
        left-, center-, or right-aligned with the position.

        """
        return self._horizontal_origin

    @property
    def verticalOrigin(self):
        """The vertical origin of the object.

        Determines whether the object is
        bottom-, center-, or top-aligned with the position.

        """
        return self._vertical_origin
