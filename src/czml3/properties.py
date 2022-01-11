from __future__ import annotations

import attr
from w3lib.url import is_url, parse_data_uri

from .base import BaseCZMLObject
from .common import Deletable, Interpolatable
from .enums import (
    ClockRanges,
    ClockSteps,
    HorizontalOrigins,
    LabelStyles,
    StripeOrientations,
    VerticalOrigins,
)
from .types import RgbafValue, RgbaValue


# noinspection PyPep8Naming
@attr.s(str=False, frozen=True, kw_only=True)
class HasAlignment:
    """A property that can be horizontally or vertically aligned."""

    horizontalOrigin: HorizontalOrigins | None = attr.ib(default=None)
    verticalOrigin: VerticalOrigins | None = attr.ib(default=None)


@attr.s(str=False, frozen=True, kw_only=True)
class Material(BaseCZMLObject):
    """A definition of how a surface is colored or shaded."""

    solidColor = attr.ib(default=None)
    image = attr.ib(default=None)
    grid = attr.ib(default=None)
    stripe = attr.ib(default=None)
    checkerboard = attr.ib(default=None)
    polylineOutline = attr.ib(default=None)  # NOTE: Not present in documentation


@attr.s(str=False, frozen=True, kw_only=True)
class PolylineOutline(BaseCZMLObject):
    """A definition of how a surface is colored or shaded."""

    color = attr.ib(default=None)
    outlineColor = attr.ib(default=None)
    outlineWidth = attr.ib(default=None)


@attr.s(str=False, frozen=True, kw_only=True)
class PolylineOutlineMaterial(BaseCZMLObject):
    """A definition of the material wrapper for a polyline outline."""

    polylineOutline = attr.ib(default=None)


@attr.s(str=False, frozen=True, kw_only=True)
class PolylineGlow(BaseCZMLObject):
    """A definition of how a glowing polyline appears."""

    color = attr.ib(default=None)
    glowPower = attr.ib(default=None)
    taperPower = attr.ib(default=None)


@attr.s(str=False, frozen=True, kw_only=True)
class PolylineGlowMaterial(BaseCZMLObject):
    """A material that fills the surface of a line with a glowing color."""

    polylineGlow = attr.ib(default=None)


@attr.s(str=False, frozen=True, kw_only=True)
class PolylineArrow(BaseCZMLObject):
    """A definition of how a polyline arrow appears."""

    color = attr.ib(default=None)


@attr.s(str=False, frozen=True, kw_only=True)
class PolylineArrowMaterial(BaseCZMLObject):
    """A material that fills the surface of a line with an arrow."""

    polylineArrow = attr.ib(default=None)


@attr.s(str=False, frozen=True, kw_only=True)
class PolylineDash(BaseCZMLObject):
    """A definition of how a polyline should be dashed with two colors."""

    color = attr.ib(default=None)
    gapColor = attr.ib(default=None)
    dashLength = attr.ib(default=None)
    dashPattern = attr.ib(default=None)


@attr.s(str=False, frozen=True, kw_only=True)
class PolylineDashMaterial(BaseCZMLObject):
    """A material that provides a how a polyline should be dashed."""

    polylineDash = attr.ib(default=None)


@attr.s(str=False, frozen=True, kw_only=True)
class PolylineMaterial(BaseCZMLObject):
    """A definition of how a surface is colored or shaded."""

    solidColor = attr.ib(default=None)
    image = attr.ib(default=None)
    grid = attr.ib(default=None)
    stripe = attr.ib(default=None)
    checkerboard = attr.ib(default=None)
    polylineDash = attr.ib(default=None)


@attr.s(str=False, frozen=True, kw_only=True)
class SolidColorMaterial(BaseCZMLObject):
    """A material that fills the surface with a solid color."""

    color = attr.ib(default=None)

    @classmethod
    def from_list(cls, color):
        return cls(color=Color.from_list(color))


@attr.s(str=False, frozen=True, kw_only=True)
class GridMaterial(BaseCZMLObject):
    """A material that fills the surface with a two-dimensional grid."""

    color = attr.ib(default=None)
    cellAlpha = attr.ib(default=0.1)
    lineCount = attr.ib(default=[8, 8])
    lineThickness = attr.ib(default=[1.0, 1.0])
    lineOffset = attr.ib(default=[0.0, 0.0])


@attr.s(str=False, frozen=True, kw_only=True)
class StripeMaterial(BaseCZMLObject):
    """A material that fills the surface with alternating colors."""

    orientation = attr.ib(default=StripeOrientations.HORIZONTAL)
    evenColor = attr.ib(default=None)
    oddColor = attr.ib(default=None)
    offset = attr.ib(default=0.0)
    repeat = attr.ib(default=1.0)


@attr.s(str=False, frozen=True, kw_only=True)
class CheckerboardMaterial(BaseCZMLObject):
    """A material that fills the surface with alternating colors."""

    evenColor = attr.ib(default=None)
    oddColor = attr.ib(default=None)
    repeat = attr.ib(default=None)


@attr.s(str=False, frozen=True, kw_only=True)
class ImageMaterial(BaseCZMLObject):
    """A material that fills the surface with an image."""

    image = attr.ib(default=None)
    repeat = attr.ib(default=[1, 1])
    color = attr.ib(default=None)
    transparent = attr.ib(default=False)


@attr.s(str=False, frozen=True, kw_only=True)
class Color(BaseCZMLObject, Interpolatable, Deletable):
    """A color. The color can optionally vary over time."""

    rgba = attr.ib(default=None)
    rgbaf = attr.ib(default=None)

    @classmethod
    def is_valid(cls, color):
        """Determines if the input is a valid color"""
        # [R, G, B] or [R, G, B, A]
        if (
            isinstance(color, (list, tuple))
            and all([issubclass(type(v), int) for v in color])
            and (3 <= len(color) <= 4)
        ):
            return all(0 <= v <= 255 for v in color)
        # [r, g, b] or [r, g, b, a] (float)
        elif (
            isinstance(color, (list, tuple))
            and all([issubclass(type(v), float) for v in color])
            and (3 <= len(color) <= 4)
        ):
            return all(0 <= v <= 1 for v in color)
        # Hexadecimal RGBA
        elif issubclass(type(color), int):
            return 0 <= color <= 0xFFFFFFFF
        # RGBA string
        elif isinstance(color, str):
            try:
                n = int(color.rsplit("#")[-1], 16)
                return 0 <= n <= 0xFFFFFFFF
            except ValueError:
                return False
        return False

    @classmethod
    def from_list(cls, color):
        if all(issubclass(type(v), int) for v in color):
            if len(color) == 3:
                color = color + [255]
            else:
                color = color[:]

            return cls(rgba=RgbaValue(values=color))
        else:
            if len(color) == 3:
                color = color + [1.0]
            else:
                color = color[:]

            return cls(rgbaf=RgbafValue(values=color))

    @classmethod
    def from_tuple(cls, color):
        return cls.from_list(list(color))

    @classmethod
    def from_hex(cls, color):
        if color > 0xFFFFFF:
            values = [
                (color & 0xFF000000) >> 24,
                (color & 0x00FF0000) >> 16,
                (color & 0x0000FF00) >> 8,
                (color & 0x000000FF) >> 0,
            ]
        else:
            values = [
                (color & 0xFF0000) >> 16,
                (color & 0x00FF00) >> 8,
                (color & 0x0000FF) >> 0,
                0xFF,
            ]

        return cls.from_list(values)

    @classmethod
    def from_str(cls, color):
        return cls.from_hex(int(color.rsplit("#")[-1], 16))


# noinspection PyPep8Naming
@attr.s(str=False, frozen=True, kw_only=True)
class Position(BaseCZMLObject, Interpolatable, Deletable):
    """Defines a position. The position can optionally vary over time."""

    referenceFrame = attr.ib(default=None)
    cartesian = attr.ib(default=None)
    cartographicRadians = attr.ib(default=None)
    cartographicDegrees = attr.ib(default=None)
    cartesianVelocity = attr.ib(default=None)
    reference = attr.ib(default=None)

    def __attrs_post_init__(self):
        if all(
            val is None
            for val in (
                self.cartesian,
                self.cartographicDegrees,
                self.cartographicRadians,
                self.cartesianVelocity,
                self.reference,
            )
        ):
            raise ValueError(
                "One of cartesian, cartographicDegrees, cartographicRadians or reference must be given"
            )


# noinspection PyPep8Naming
@attr.s(str=False, frozen=True, kw_only=True)
class ViewFrom(BaseCZMLObject, Interpolatable, Deletable):
    """suggested initial camera position offset when tracking this object.

    ViewFrom can optionally vary over time."""

    cartesian = attr.ib(default=None)
    reference = attr.ib(default=None)

    def __attrs_post_init__(self):
        if all(val is None for val in (self.cartesian, self.reference)):
            raise ValueError("One of cartesian or reference must be given")


# noinspection PyPep8Naming
@attr.s(str=False, frozen=True, kw_only=True)
class Billboard(BaseCZMLObject, HasAlignment):
    """A billboard, or viewport-aligned image.

    The billboard is positioned in the scene by the position property.
    A billboard is sometimes called a marker.
    """

    image = attr.ib()
    show = attr.ib(default=None)
    scale = attr.ib(default=None)
    eyeOffset = attr.ib(default=None)


@attr.s(str=False, frozen=True, kw_only=True)
class EllipsoidRadii(BaseCZMLObject, Interpolatable, Deletable):
    """The radii of an ellipsoid."""

    cartesian = attr.ib(default=None)
    reference = attr.ib(default=None)


@attr.s(str=False, frozen=True, kw_only=True)
class Corridor(BaseCZMLObject):
    """A corridor , which is a shape defined by a centerline and width that conforms to the
    curvature of the body shape. It can can optionally be extruded into a volume."""

    positions = attr.ib()
    show = attr.ib(default=None)
    width = attr.ib()
    height = attr.ib(default=None)
    heightReference = attr.ib(default=None)
    extrudedHeight = attr.ib(default=None)
    extrudedHeightReference = attr.ib(default=None)
    cornerType = attr.ib(default=None)
    granularity = attr.ib(default=None)
    fill = attr.ib(default=None)
    material = attr.ib(default=None)
    outline = attr.ib(default=None)
    outlineColor = attr.ib(default=None)
    outlineWidth = attr.ib(default=None)
    shadows = attr.ib(default=None)
    distanceDisplayCondition = attr.ib(default=None)
    classificationType = attr.ib(default=None)
    zIndex = attr.ib(default=None)


@attr.s(str=False, frozen=True, kw_only=True)
class Cylinder(BaseCZMLObject):
    """A cylinder, which is a special cone defined by length, top and bottom radius."""

    length = attr.ib()
    show = attr.ib(default=None)
    topRadius = attr.ib()
    bottomRadius = attr.ib()
    heightReference = attr.ib(default=None)
    fill = attr.ib(default=None)
    material = attr.ib(default=None)
    outline = attr.ib(default=None)
    outlineColor = attr.ib(default=None)
    outlineWidth = attr.ib(default=None)
    numberOfVerticalLines = attr.ib(default=None)
    slices = attr.ib(default=None)
    shadows = attr.ib(default=None)
    distanceDisplayCondition = attr.ib(default=None)


@attr.s(str=False, frozen=True, kw_only=True)
class Ellipse(BaseCZMLObject):
    """An ellipse, which is a close curve, on or above Earth's surface."""

    semiMajorAxis = attr.ib()
    semiMinorAxis = attr.ib()
    show = attr.ib(default=None)
    height = attr.ib(default=None)
    heightReference = attr.ib(default=None)
    extrudedHeight = attr.ib(default=None)
    extrudedHeightReference = attr.ib(default=None)
    rotation = attr.ib(default=None)
    stRotation = attr.ib(default=None)
    granularity = attr.ib(default=None)
    fill = attr.ib(default=None)
    material = attr.ib(default=None)
    outline = attr.ib(default=None)
    outlineColor = attr.ib(default=None)
    outlineWidth = attr.ib(default=None)
    numberOfVerticalLines = attr.ib(default=None)
    shadows = attr.ib(default=None)
    distanceDisplayCondition = attr.ib(default=None)
    classificationType = attr.ib(default=None)
    zIndex = attr.ib(default=None)


@attr.s(str=False, frozen=True, kw_only=True)
class Polygon(BaseCZMLObject):
    """A polygon, which is a closed figure on the surface of the Earth."""

    positions = attr.ib()
    show = attr.ib(default=None)
    arcType = attr.ib(default=None)
    granularity = attr.ib(default=None)
    material = attr.ib(default=None)
    shadows = attr.ib(default=None)
    distanceDisplayCondition = attr.ib(default=None)
    classificationType = attr.ib(default=None)
    zIndex = attr.ib(default=None)


@attr.s(str=False, frozen=True, kw_only=True)
class Polyline(BaseCZMLObject):
    """A polyline, which is a line in the scene composed of multiple segments."""

    positions = attr.ib()
    show = attr.ib(default=None)
    arcType = attr.ib(default=None)
    width = attr.ib(default=None)
    granularity = attr.ib(default=None)
    material = attr.ib(default=None)
    followSurface = attr.ib(default=None)
    shadows = attr.ib(default=None)
    depthFailMaterial = attr.ib(default=None)
    distanceDisplayCondition = attr.ib(default=None)
    clampToGround = attr.ib(default=None)
    classificationType = attr.ib(default=None)
    zIndex = attr.ib(default=None)


@attr.s(str=False, frozen=True, kw_only=True)
class ArcType(BaseCZMLObject, Deletable):
    """The type of an arc."""

    arcType = attr.ib(default=None)
    reference = attr.ib(default=None)


@attr.s(str=False, frozen=True, kw_only=True)
class ShadowMode(BaseCZMLObject, Deletable):
    """Whether or not an object casts or receives shadows from each light source when shadows are enabled."""

    shadowMode = attr.ib(default=None)
    referenec = attr.ib(default=None)


@attr.s(str=False, frozen=True, kw_only=True)
class ClassificationType(BaseCZMLObject, Deletable):
    """Whether a classification affects terrain, 3D Tiles, or both."""

    classificationType = attr.ib(default=None)
    reference = attr.ib(default=None)


@attr.s(str=False, frozen=True, kw_only=True)
class DistanceDisplayCondition(BaseCZMLObject, Interpolatable, Deletable):
    """Indicates the visibility of an object based on the distance to the camera."""

    distanceDisplayCondition = attr.ib(default=None)
    reference = attr.ib(default=None)


@attr.s(str=False, frozen=True, kw_only=True)
class PositionList(BaseCZMLObject, Deletable):
    """A list of positions."""

    referenceFrame = attr.ib(default=None)
    cartesian = attr.ib(default=None)
    cartographicRadians = attr.ib(default=None)
    cartographicDegrees = attr.ib(default=None)
    references = attr.ib(default=None)


@attr.s(str=False, frozen=True, kw_only=True)
class Ellipsoid(BaseCZMLObject):
    """A closed quadric surface that is a three-dimensional analogue of an ellipse."""

    radii = attr.ib()
    innerRadii = attr.ib(default=None)
    minimumClock = attr.ib(default=None)
    maximumClock = attr.ib(default=None)
    minimumCone = attr.ib(default=None)
    maximumCone = attr.ib(default=None)
    show = attr.ib(default=None)
    heightReference = attr.ib(default=None)
    fill = attr.ib(default=None)
    material = attr.ib(default=None)
    outline = attr.ib(default=None)
    outlineColor = attr.ib(default=None)
    outlineWidth = attr.ib(default=None)
    stackPartitions = attr.ib(default=None)
    slicePartitions = attr.ib(default=None)
    subdivisions = attr.ib(default=None)


@attr.s(str=False, frozen=True, kw_only=True)
class Box(BaseCZMLObject):
    """A box, which is a closed rectangular cuboid."""

    show = attr.ib(default=None)
    dimensions = attr.ib(default=None)
    heightReference = attr.ib(default=None)
    fill = attr.ib(default=None)
    material = attr.ib(default=None)
    outline = attr.ib(default=None)
    outlineColor = attr.ib(default=None)
    outlineWidth = attr.ib(default=None)
    shadows = attr.ib(default=None)
    distanceDisplayCondition = attr.ib(default=None)


@attr.s(str=False, frozen=True, kw_only=True)
class BoxDimensions(BaseCZMLObject, Interpolatable):
    """The width, depth, and height of a box."""

    cartesian = attr.ib(default=None)
    reference = attr.ib(default=None)


# noinspection PyPep8Naming
@attr.s(str=False, frozen=True, kw_only=True)
class Rectangle(BaseCZMLObject, Interpolatable, Deletable):
    """A cartographic rectangle, which conforms to the curvature of the globe and
    can be placed on the surface or at altitude and can optionally be extruded into a volume."""

    coordinates = attr.ib(default=None)
    fill = attr.ib(default=None)
    material = attr.ib(default=None)


# noinspection PyPep8Naming
@attr.s(str=False, frozen=True, kw_only=True)
class RectangleCoordinates(BaseCZMLObject, Interpolatable, Deletable):
    """A set of coordinates describing a cartographic rectangle on the surface of the ellipsoid."""

    reference = attr.ib(default=None)
    wsen = attr.ib(default=None)
    wsenDegrees = attr.ib(default=None)

    def __attrs_post_init__(self):
        if all(val is None for val in (self.wsen, self.wsenDegrees)):
            raise ValueError(
                "One of cartesian, cartographicDegrees or cartographicRadians must be given"
            )


@attr.s(str=False, frozen=True, kw_only=True)
class EyeOffset(BaseCZMLObject, Deletable):
    """An offset in eye coordinates which can optionally vary over time.

    Eye coordinates are a left-handed coordinate system
    where the X-axis points toward the viewer's right,
    the Y-axis poitns up, and the Z-axis points into the screen.

    """

    cartesian = attr.ib(default=None)
    reference = attr.ib(default=None)


@attr.s(str=False, frozen=True, kw_only=True)
class HeightReference(BaseCZMLObject, Deletable):
    """The height reference of an object, which indicates if the object's position is relative to terrain or not."""

    heightReference = attr.ib(default=None)
    reference = attr.ib(default=None)


# noinspection PyPep8Naming
@attr.s(str=False, frozen=True, kw_only=True)
class Clock(BaseCZMLObject):
    """Initial settings for a simulated clock when a document is loaded.

    The start and stop time are configured using the interval property.

    """

    currentTime = attr.ib(default=None)
    multiplier = attr.ib(default=1.0)
    range = attr.ib(default=ClockRanges.LOOP_STOP)
    step = attr.ib(default=ClockSteps.SYSTEM_CLOCK_MULTIPLIER)


# noinspection PyPep8Naming
@attr.s(str=False, frozen=True, kw_only=True)
class Path(BaseCZMLObject):
    """A path, which is a polyline defined by the motion of an object over time.

    The possible vertices of the path are specified by the position property.
    Note that because clients cannot render a truly infinite path,
    the path must be limited,
    either by defining availability for this object,
    or by using the leadTime and trailTime properties.

    """

    show = attr.ib(default=None)
    leadTime = attr.ib(default=None)
    trailTime = attr.ib(default=None)
    width = attr.ib(default=1.0)
    resolution = attr.ib(default=60.0)
    material = attr.ib(default=None)
    distanceDisplayCondition = attr.ib(default=None)


@attr.s(str=False, frozen=True, kw_only=True)
class Point(BaseCZMLObject):
    """A point, or viewport-aligned circle."""

    show = attr.ib(default=None)
    pixelSize = attr.ib(default=None)
    heightReference = attr.ib(default=None)
    color = attr.ib(default=None)
    outlineColor = attr.ib(default=None)
    outlineWidth = attr.ib(default=None)
    scaleByDistance = attr.ib(default=None)
    translucencyByDistance = attr.ib(default=None)
    distanceDisplayCondition = attr.ib(default=None)
    disableDepthTestDistance = attr.ib(default=None)


@attr.s(str=False, frozen=True, kw_only=True)
class TileSet(BaseCZMLObject):
    """A 3D Tiles tileset."""

    show = attr.ib(default=None)
    uri = attr.ib()
    maximumScreenSpaceError = attr.ib(default=None)


@attr.s(str=False, frozen=True, kw_only=True)
class Wall(BaseCZMLObject):
    """A two-dimensional wall defined as a line strip and optional maximum and minimum heights.
    It conforms to the curvature of the globe and can be placed along the surface or at altitude."""

    show = attr.ib(default=None)
    positions = attr.ib()
    minimumHeights = attr.ib(default=None)
    maximumHeights = attr.ib(default=None)
    granularity = attr.ib(default=None)
    fill = attr.ib(default=None)
    material = attr.ib(default=None)
    outline = attr.ib(default=None)
    outlineColor = attr.ib(default=None)
    outlineWidth = attr.ib(default=None)
    shadows = attr.ib(default=None)
    distanceDisplayCondition = attr.ib(default=None)


@attr.s(str=False, frozen=True, kw_only=True)
class NearFarScalar(BaseCZMLObject, Interpolatable, Deletable):
    """A numeric value which will be linearly interpolated between two values based on an object's distance from the
     camera, in eye coordinates.

    The computed value will interpolate between the near value and the far value while the camera distance falls
    between the near distance and the far distance, and will be clamped to the near or far value while the distance is
    less than the near distance or greater than the far distance, respectively.
    """

    nearFarScalar = attr.ib(default=None)
    reference = attr.ib(default=None)


# noinspection PyPep8Naming
@attr.s(str=False, frozen=True, kw_only=True)
class Label(BaseCZMLObject, HasAlignment):
    """A string of text."""

    show = attr.ib(default=True)
    text = attr.ib(default=None)
    font = attr.ib(default=None)
    style = attr.ib(default=LabelStyles.FILL)
    scale = attr.ib(default=None)
    showBackground = attr.ib(default=None)
    backgroundColor = attr.ib(default=None)
    fillColor = attr.ib(default=None)
    outlineColor = attr.ib(default=None)
    outlineWidth = attr.ib(default=1.0)
    pixelOffset = attr.ib(default=None)


@attr.s(str=False, frozen=True, kw_only=True)
class Orientation(BaseCZMLObject, Interpolatable, Deletable):
    """Defines an orientation.

    An orientation is a rotation that takes a vector expressed in the "body" axes of the object
    and transforms it to the Earth fixed axes.

    """

    unitQuaternion = attr.ib(default=None)
    reference = attr.ib(default=None)
    velocityReference = attr.ib(default=None)


@attr.s(str=False, frozen=True, kw_only=True)
class Model(BaseCZMLObject):
    """A 3D model."""

    show = attr.ib(default=None)
    gltf = attr.ib()
    scale = attr.ib(default=None)
    minimumPixelSize = attr.ib(default=None)
    maximumScale = attr.ib(default=None)
    incrementallyLoadTextures = attr.ib(default=None)
    runAnimations = attr.ib(default=None)
    shadows = attr.ib(default=None)
    heightReference = attr.ib(default=None)
    silhouetteColor = attr.ib(default=None)
    silhouetteSize = attr.ib(default=None)
    color = attr.ib(default=None)
    colorBlendMode = attr.ib(default=None)
    colorBlendAmount = attr.ib(default=None)
    distanceDisplayCondition = attr.ib(default=None)
    nodeTransformations = attr.ib(default=None)
    articulations = attr.ib(default=None)


@attr.s(str=False, frozen=True, kw_only=True)
class Uri(BaseCZMLObject, Deletable):
    """A URI value.

    The URI can optionally vary with time.
    """

    uri = attr.ib(default=None)

    @uri.validator
    def _check_uri(self, attribute, value):
        try:
            parse_data_uri(value)
        except ValueError as e:
            if not is_url(value):
                raise ValueError("uri must be a URL or a data URI") from e

    def to_json(self):
        return self.uri
