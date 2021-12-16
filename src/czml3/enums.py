from enum import Enum


class InterpolationAlgorithms(Enum):
    """The interpolation algorithm to use when interpolating."""

    LINEAR = "LINEAR"
    LAGRANGE = "LAGRANGE"
    HERMITE = "HERMITE"


class ExtrapolationTypes(Enum):
    """The type of extrapolation to perform when a value is requested at a time after any available samples."""

    NONE = "NONE"
    HOLD = "HOLD"
    EXTRAPOLATE = "EXTRAPOLATE"


class ReferenceFrames(Enum):
    """The reference frame in which cartesian positions are specified."""

    FIXED = "FIXED"
    INERTIAL = "INERTIAL"


class LabelStyles(Enum):
    """The style of a label."""

    FILL = "FILL"
    OUTLINE = "OUTLINE"
    FILL_AND_OUTLINE = "FILL_AND_OUTLINE"


class ClockRanges(Enum):
    """The behavior of a clock when its current time reaches its start or end time."""

    UNBOUNDED = "UNBOUNDED"
    CLAMPED = "CLAMPED"
    LOOP_STOP = "LOOP_STOP"


class ClockSteps(Enum):
    TICK_DEPENDENT = "TICK_DEPENDENT"
    SYSTEM_CLOCK_MULTIPLIER = "SYSTEM_CLOCK_MULTIPLIER"
    SYSTEM_CLOCK = "SYSTEM_CLOCK"


class VerticalOrigins(Enum):
    BASELINE = "BASELINE"
    BOTTOM = "BOTTOM"
    CENTER = "CENTER"
    TOP = "TOP"


class HorizontalOrigins(Enum):
    LEFT = "LEFT"
    CENTER = "CENTER"
    RIGHT = "RIGHT"


class HeightReferences(Enum):
    NONE = "NONE"
    CLAMP_TO_GROUND = "CLAMP_TO_GROUND"
    RELATIVE_TO_GROUND = "RELATIVE_TO_GROUND"


class ColorBlendModes(Enum):
    HIGHLIGHT = "HIGHLIGHT"
    REPLACE = "REPLACE"
    MIX = "MIX"


class ShadowModes(Enum):
    DISABLED = "DISABLED"
    ENABLED = "ENABLED"
    CAST_ONLY = "CAST_ONLY"
    RECEIVE_ONLY = "RECEIVE_ONLY"


class ClassificationTypes(Enum):
    TERRAIN = "TERRAIN"
    CESIUM_3D_TILE = "CESIUM_3D_TILE"
    BOTH = "BOTH"


class ArcTypes(Enum):
    NONE = "NONE"
    GEODESIC = "GEODESIC"
    RHUMB = "RHUMB"


class StripeOrientations(Enum):
    HORIZONTAL = "HORIZONTAL"
    VERTICAL = "VERTICAL"
