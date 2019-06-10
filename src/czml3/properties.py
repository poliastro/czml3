from typing import Optional

from .base import BaseCZMLObject
from .enums import InterpolationAlgorithms, ReferenceFrames
from .values import Cartesian3Value


# noinspection PyPep8Naming
class DeletableProperty:
    """A property whose value may be deleted."""

    KNOWN_PROPERTIES = ["delete"]

    def __init__(self, *, delete: Optional[bool] = None, **kwargs):
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
        epoch: Optional[str] = None,
        interpolationAlgorithm: InterpolationAlgorithms = InterpolationAlgorithms.LINEAR,
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


# noinspection PyPep8Naming
class Position(BaseCZMLObject, InterpolatableProperty, DeletableProperty):
    """Defines a position. The position can optionally vary over time."""

    KNOWN_PROPERTIES = (
        InterpolatableProperty.KNOWN_PROPERTIES
        + DeletableProperty.KNOWN_PROPERTIES
        + ["referenceFrame", "cartesian"]
    )

    def __init__(
        self,
        *,
        delete: Optional[bool] = None,
        epoch: Optional[str] = None,
        interpolationAlgorithm: InterpolationAlgorithms = InterpolationAlgorithms.LINEAR,
        referenceFrame: ReferenceFrames = ReferenceFrames.FIXED,
        cartesian: Cartesian3Value = None,
    ):
        super().__init__(
            delete=delete, epoch=epoch, interpolationAlgorithm=interpolationAlgorithm
        )
        self._reference_frame = referenceFrame
        self._cartesian = cartesian

    @property
    def referenceFrame(self):
        """The reference frame in which cartesian positions are specified."""
        return self._reference_frame

    @property
    def cartesian(self):
        """The position specified as a three-dimensional Cartesian value.

        The value [X, Y, Z] is specified
        in meters relative to the ReferenceFrame.
        """
        return self._cartesian
