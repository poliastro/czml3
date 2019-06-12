from enum import Enum, auto


class InterpolationAlgorithms(Enum):
    """The interpolation algorithm to use when interpolating."""

    LINEAR = auto()
    LAGRANGE = auto()
    HERMITE = auto()


class ReferenceFrames(Enum):
    """The reference frame in which cartesian positions are specified."""

    FIXED = auto()
    INERTIAL = auto()


class LabelStyles(Enum):
    """The style of a label."""

    FILL = auto()
    OUTLINE = auto()
    FILL_AND_OUTLINE = auto()


class ClockRanges(Enum):
    """The behavior of a clock when its current time reaches its start or end time."""

    UNBOUNDED = auto()
    CLAMPED = auto()
    LOOP_STOP = auto()


class ClockSteps(Enum):
    TICK_DEPENDENT = auto()
    SYSTEM_CLOCK_MULTIPLIER = auto()
    SYSTEM_CLOCK = auto()


class VerticalOrigins(Enum):
    BASELINE = auto()
    BOTTOM = auto()
    CENTER = auto()
    TOP = auto()


class HorizontalOrigins(Enum):
    LEFT = auto()
    CENTER = auto()
    RIGHT = auto()
