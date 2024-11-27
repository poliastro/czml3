import sys
from enum import auto
from typing import Any

if sys.version_info[1] >= 11:
    from enum import StrEnum

    class OCaseStrEnum(StrEnum):
        """
        StrEnum where enum.auto() returns the original member name, not lower-cased name.
        """

        @staticmethod
        def _generate_next_value_(
            name: str, start: int, count: int, last_values: list[Any]
        ) -> str:
            return name
else:
    from strenum import StrEnum as OCaseStrEnum


class InterpolationAlgorithms(OCaseStrEnum):
    """The interpolation algorithm to use when interpolating."""

    LINEAR = auto()
    LAGRANGE = auto()
    HERMITE = auto()


class ExtrapolationTypes(OCaseStrEnum):
    """The type of extrapolation to perform when a value is requested at a time after any available samples."""

    NONE = auto()
    HOLD = auto()
    EXTRAPOLATE = auto()


class ReferenceFrames(OCaseStrEnum):
    """The reference frame in which cartesian positions are specified."""

    FIXED = auto()
    INERTIAL = auto()


class LabelStyles(OCaseStrEnum):
    """The style of a label."""

    FILL = auto()
    OUTLINE = auto()
    FILL_AND_OUTLINE = auto()


class ClockRanges(OCaseStrEnum):
    """The behavior of a clock when its current time reaches its start or end time."""

    UNBOUNDED = auto()
    CLAMPED = auto()
    LOOP_STOP = auto()


class ClockSteps(OCaseStrEnum):
    TICK_DEPENDENT = auto()
    SYSTEM_CLOCK_MULTIPLIER = auto()
    SYSTEM_CLOCK = auto()


class VerticalOrigins(OCaseStrEnum):
    BASELINE = auto()
    BOTTOM = auto()
    CENTER = auto()
    TOP = auto()


class HorizontalOrigins(OCaseStrEnum):
    LEFT = auto()
    CENTER = auto()
    RIGHT = auto()


class HeightReferences(OCaseStrEnum):
    NONE = auto()
    CLAMP_TO_GROUND = auto()
    RELATIVE_TO_GROUND = auto()


class ColorBlendModes(OCaseStrEnum):
    HIGHLIGHT = auto()
    REPLACE = auto()
    MIX = auto()


class ShadowModes(OCaseStrEnum):
    DISABLED = auto()
    ENABLED = auto()
    CAST_ONLY = auto()
    RECEIVE_ONLY = auto()


class ClassificationTypes(OCaseStrEnum):
    TERRAIN = auto()
    CESIUM_3D_TILE = auto()
    BOTH = auto()


class ArcTypes(OCaseStrEnum):
    NONE = auto()
    GEODESIC = auto()
    RHUMB = auto()


class StripeOrientations(OCaseStrEnum):
    HORIZONTAL = auto()
    VERTICAL = auto()


class CornerTypes(OCaseStrEnum):
    ROUNDED = auto()
    MITERED = auto()
    BEVELED = auto()
