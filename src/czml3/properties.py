from typing import Optional

from czml3.common import DeletableProperty, InterpolatableProperty

from .base import BaseCZMLObject
from .enums import InterpolationAlgorithms, ReferenceFrames
from .values import Cartesian3Value


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
