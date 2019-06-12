from czml3.common import DeletableProperty, InterpolatableProperty

from .base import BaseCZMLObject
from .enums import (
    ClockRanges,
    ClockSteps,
    InterpolationAlgorithms,
    ReferenceFrames,
)
from .types import Cartesian3Value, Uri


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
        delete=None,
        epoch=None,
        interpolationAlgorithm=InterpolationAlgorithms.LINEAR,
        referenceFrame=ReferenceFrames.FIXED,
        cartesian=None,
    ):
        super().__init__(
            delete=delete, epoch=epoch, interpolationAlgorithm=interpolationAlgorithm
        )
        if isinstance(cartesian, list):
            cartesian = Cartesian3Value(values=cartesian)
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


# noinspection PyPep8Naming
class Billboard(BaseCZMLObject):
    """A billboard, or viewport-aligned image.

    The billboard is positioned in the scene by the position property.
    A billboard is sometimes called a marker.
    """

    KNOWN_PROPERTIES = ["image"]

    def __init__(self, *, image):
        if isinstance(image, str):
            image = Uri(uri=image)

        self._image = image

    @property
    def image(self):
        """The URI of the image displayed on the billboard.

        For broadest client compatibility,
        the URI should be accessible via Cross-Origin Resource Sharing (CORS).
        The URI may also be a data URI.
        """
        return self._image


# noinspection PyPep8Naming
class Clock(BaseCZMLObject):
    """Initial settings for a simulated clock when a document is loaded.

    The start and stop time are configured using the interval property.

    """

    KNOWN_PROPERTIES = ["currentTime", "multiplier", "range", "step"]

    def __init__(
        self,
        *,
        currentTime=None,
        multiplier=1.0,
        range=ClockRanges.LOOP_STOP,
        step=ClockSteps.SYSTEM_CLOCK_MULTIPLIER,
    ):
        self._current_time = currentTime
        self._multiplier = multiplier
        self._range = range
        self._step = step

    @property
    def currentTime(self):
        """The current time, specified in ISO8601 format."""
        return self._current_time

    @property
    def multiplier(self):
        """The multiplier.

        When step is set to TICK_DEPENDENT,
        this is the number of seconds to advance each tick.
        When step is set to SYSTEM_CLOCK_DEPENDENT,
        this is multiplied by the elapsed system time between ticks.
        This value is ignored in SYSTEM_CLOCK mode.

        """
        return self._multiplier

    @property
    def range(self):
        """The behavior when the current time reaches its start or end times."""
        return self._range

    @property
    def step(self):
        """How the current time advances each tick."""
        return self._step
