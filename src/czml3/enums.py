try:
    from enum import Enum, auto  # type: ignore
except ImportError:
    # We are in Python 3.5
    # https://docs.python.org/3.5/library/enum.html#autonumber
    from enum import Enum as _BaseEnum

    class Enum(_BaseEnum):  # type: ignore
        def __new__(cls, *args):
            value = len(cls.__members__) + 1
            obj = object.__new__(cls)
            obj._value_ = value
            return obj

    def auto():
        pass


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
