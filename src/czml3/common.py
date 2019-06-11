from czml3.enums import InterpolationAlgorithms


# noinspection PyPep8Naming
class DeletableProperty:
    """A property whose value may be deleted."""

    KNOWN_PROPERTIES = ["delete"]

    def __init__(self, *, delete=None, **kwargs):
        super().__init__(**kwargs)  # type: ignore
        self._delete = delete

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
class InterpolatableProperty:
    """A property whose value may be determined by interpolating.

    The interpolation happens over provided time-tagged samples.
    """

    KNOWN_PROPERTIES = ["epoch", "interpolationAlgorithm"]

    def __init__(
        self,
        *,
        epoch=None,
        interpolationAlgorithm=InterpolationAlgorithms.LINEAR,
        **kwargs,
    ):
        super().__init__(**kwargs)  # type: ignore
        self._epoch = epoch
        self._interpolation_algorithm = interpolationAlgorithm

    @property
    def epoch(self):
        """The epoch to use for times specified as seconds since an epoch."""
        return self._epoch

    @property
    def interpolationAlgorithm(self):
        """The interpolation algorithm to use when interpolating."""
        return self._interpolation_algorithm
