from enum import Enum


class InterpolationAlgorithms(Enum):
    """The interpolation algorithm to use when interpolating."""

    LINEAR = "LINEAR"
    LAGRANGE = "LAGRANGE"
    HERMITE = "HERMITE"


class ReferenceFrames(Enum):
    """The reference frame in which cartesian positions are specified."""

    FIXED = "FIXED"
    INERTIAL = "INERTIAL"
