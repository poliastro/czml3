from typing import Any
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
    ColorBlendModes,
    CornerTypes
)
from .types import RgbafValue, RgbaValue


# noinspection PyPep8Naming
@attr.s(str=False, frozen=True, kw_only=True)
class HasAlignment:
    """A property that can be horizontally or vertically aligned."""

    horizontalOrigin: HorizontalOrigins
    verticalOrigin: VerticalOrigins


@attr.s(str=False, frozen=True, kw_only=True)
class Material(BaseCZMLObject):
    """A definition of how a surface is colored or shaded."""

    solidColor: SolidColorMaterial
    image: ImageMaterial
    grid: GridMaterial
    stripe: StripeMaterial
    checkerboard: CheckerboardMaterial
    polylineOutline: Any  # NOTE: Not present in documentation


@attr.s(str=False, frozen=True, kw_only=True)
class PolylineOutline(BaseCZMLObject):
    """A definition of how a surface is colored or shaded."""

    color: Color
    outlineColor: Color
    outlineWidth: int | float


@attr.s(str=False, frozen=True, kw_only=True)
class PolylineOutlineMaterial(BaseCZMLObject):
    """A definition of the material wrapper for a polyline outline."""

    polylineOutline: PolylineOutline


@attr.s(str=False, frozen=True, kw_only=True)
class PolylineGlow(BaseCZMLObject):
    """A definition of how a glowing polyline appears."""

    color: Color
    glowPower: int | float
    taperPower: int | float


@attr.s(str=False, frozen=True, kw_only=True)
class PolylineGlowMaterial(BaseCZMLObject):
    """A material that fills the surface of a line with a glowing color."""

    polylineGlow: PolylineGlow


@attr.s(str=False, frozen=True, kw_only=True)
class PolylineArrow(BaseCZMLObject):
    """A definition of how a polyline arrow appears."""

    color: Color


@attr.s(str=False, frozen=True, kw_only=True)
class PolylineArrowMaterial(BaseCZMLObject):
    """A material that fills the surface of a line with an arrow."""

    polylineArrow: PolylineArrow


@attr.s(str=False, frozen=True, kw_only=True)
class PolylineDash(BaseCZMLObject):
    """A definition of how a polyline should be dashed with two colors."""

    color: Color
    gapColor: Color
    dashLength: int | float
    dashPattern: int


@attr.s(str=False, frozen=True, kw_only=True)
class PolylineDashMaterial(BaseCZMLObject):
    """A material that provides a how a polyline should be dashed."""

    polylineDash: PolylineDash


@attr.s(str=False, frozen=True, kw_only=True)
class PolylineMaterial(BaseCZMLObject):
    """A definition of how a surface is colored or shaded."""

    solidColor: SolidColorMaterial
    image: ImageMaterial
    grid: GridMaterial
    stripe: StripeMaterial
    checkerboard: CheckerboardMaterial
    polylineDash: PolylineDashMaterial


@attr.s(str=False, frozen=True, kw_only=True)
class SolidColorMaterial(BaseCZMLObject):
    """A material that fills the surface with a solid color."""

    color: Color

    @classmethod
    def from_list(cls, color):
        return cls(color=Color.from_list(color))


@attr.s(str=False, frozen=True, kw_only=True)
class GridMaterial(BaseCZMLObject):
    """A material that fills the surface with a two-dimensional grid."""

    color: Color
    cellAlpha: int | float = 0.1
    lineCount: list[int] | list[float] = [8, 8]
    lineThickness: list[int] | list[float] = 1.0, 1.0
    lineOffset: list[int] | list[float] = [0.0, 0.0]


@attr.s(str=False, frozen=True, kw_only=True)
class StripeMaterial(BaseCZMLObject):
    """A material that fills the surface with alternating colors."""

    orientation: StripeOrientations = StripeOrientations.HORIZONTAL
    evenColor: Color
    oddColor: Color
    offset: int | float = 0.0
    repeat: int | float = 1.0


@attr.s(str=False, frozen=True, kw_only=True)
class CheckerboardMaterial(BaseCZMLObject):
    """A material that fills the surface with alternating colors."""

    evenColor: Color
    oddColor: Color
    repeat: list[int] | list[float] = 1.0


@attr.s(str=False, frozen=True, kw_only=True)
class ImageMaterial(BaseCZMLObject):
    """A material that fills the surface with an image."""

    image: Uri
    repeat: list[int] | list[float] = 1.0
    color: Color
    transparent: bool = False


@attr.s(str=False, frozen=True, kw_only=True)
class Color(BaseCZMLObject, Interpolatable, Deletable):
    """A color. The color can optionally vary over time."""

    rgba: list[int] | list[float]
    rgbaf: list[int] | list[float]

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

    referenceFrame: str
    cartesian: list[int] | list[float]
    cartographicRadians: list[int] | list[float]
    cartographicDegrees: list[int] | list[float]
    cartesianVelocity: list[int] | list[float]
    reference: str

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

    cartesian: list[int] | list[float]
    reference: str

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

    image: Uri
    show: bool
    scale: int | float
    eyeOffset: EyeOffset | list[int] | list[float]
    color: Color


@attr.s(str=False, frozen=True, kw_only=True)
class EllipsoidRadii(BaseCZMLObject, Interpolatable, Deletable):
    """The radii of an ellipsoid."""

    cartesian: list[int] | list[float]
    reference: str


@attr.s(str=False, frozen=True, kw_only=True)
class Corridor(BaseCZMLObject):
    """A corridor , which is a shape defined by a centerline and width that conforms to the
    curvature of the body shape. It can can optionally be extruded into a volume."""

    positions: PositionList
    show: bool
    width: int | float
    height: int | float
    heightReference: HeightReference
    extrudedHeight: int | float
    extrudedHeightReference: HeightReference
    cornerType: CornerTypes
    granularity: int | float
    fill: bool
    material: Material
    outline: bool
    outlineColor: Color
    outlineWidth: int | float
    shadows: ShadowMode
    distanceDisplayCondition: DistanceDisplayCondition
    classificationType: ClassificationType
    zIndex: int


@attr.s(str=False, frozen=True, kw_only=True)
class Cylinder(BaseCZMLObject):
    """A cylinder, which is a special cone defined by length, top and bottom radius."""

    length: int | float
    show: bool
    topRadius: int | float
    bottomRadius: int | float
    heightReference: HeightReference
    fill: bool
    material: Material
    outline: bool
    outlineColor: Color
    outlineWidth: int | float
    numberOfVerticalLines: int
    slices: int
    shadows: ShadowMode
    distanceDisplayCondition: DistanceDisplayCondition


@attr.s(str=False, frozen=True, kw_only=True)
class Ellipse(BaseCZMLObject):
    """An ellipse, which is a close curve, on or above Earth's surface."""

    semiMajorAxis: int | float
    semiMinorAxis: int | float
    show: bool
    height: int | float
    heightReference: HeightReference
    extrudedHeight: int | float
    extrudedHeightReference: HeightReference
    rotation: int | float
    stRotation: int | float
    granularity: int | float
    fill: bool
    material: Material
    outline: bool
    outlineColor: Color
    outlineWidth: int | float
    numberOfVerticalLines: int
    shadows: ShadowMode
    distanceDisplayCondition: DistanceDisplayCondition
    classificationType: ClassificationType
    zIndex: int


@attr.s(str=False, frozen=True, kw_only=True)
class Polygon(BaseCZMLObject):
    """A polygon, which is a closed figure on the surface of the Earth."""

    positions: PositionList
    show: bool
    arcType: ArcType
    granularity: int | float
    material: Material
    shadows: ShadowMode
    distanceDisplayCondition: DistanceDisplayCondition
    classificationType: ClassificationType
    zIndex: int


@attr.s(str=False, frozen=True, kw_only=True)
class Polyline(BaseCZMLObject):
    """A polyline, which is a line in the scene composed of multiple segments."""

    positions: PositionList
    show: bool
    arcType: ArcType
    width: int | float
    granularity: int | float
    material: Material
    followSurface: bool
    shadows: ShadowMode
    depthFailMaterial: PolylineMaterial
    distanceDisplayCondition: DistanceDisplayCondition
    clampToGround: bool
    classificationType: ClassificationType
    zIndex: bool


@attr.s(str=False, frozen=True, kw_only=True)
class ArcType(BaseCZMLObject, Deletable):
    """The type of an arc."""

    arcType: ArcType
    reference: str


@attr.s(str=False, frozen=True, kw_only=True)
class ShadowMode(BaseCZMLObject, Deletable):
    """Whether or not an object casts or receives shadows from each light source when shadows are enabled."""

    shadowMode: ShadowMode
    reference: str


@attr.s(str=False, frozen=True, kw_only=True)
class ClassificationType(BaseCZMLObject, Deletable):
    """Whether a classification affects terrain, 3D Tiles, or both."""

    classificationType: ClassificationType
    reference: str


@attr.s(str=False, frozen=True, kw_only=True)
class DistanceDisplayCondition(BaseCZMLObject, Interpolatable, Deletable):
    """Indicates the visibility of an object based on the distance to the camera."""

    distanceDisplayCondition: DistanceDisplayCondition
    reference: str


@attr.s(str=False, frozen=True, kw_only=True)
class PositionList(BaseCZMLObject, Deletable):
    """A list of positions."""

    referenceFrame: str
    cartesian: list[int] | list[float]
    cartographicRadians: list[int] | list[float]
    cartographicDegrees: list[int] | list[float]
    references: str | list[str]

    @cartesian.validator
    def _check_length(self, attribute, value):
        if len(value) % 3 != 0:
            raise ValueError("Input must have a length that is a multiple of three.")

    @cartographicRadians.validator
    def _check_length(self, attribute, value):
        if len(value) % 3 != 0:
            raise ValueError("Input must have a length that is a multiple of three.")

    @cartographicDegrees.validator
    def _check_length(self, attribute, value):
        if len(value) % 3 != 0:
            raise ValueError("Input must have a length that is a multiple of three.")


@attr.s(str=False, frozen=True, kw_only=True)
class Ellipsoid(BaseCZMLObject):
    """A closed quadric surface that is a three-dimensional analogue of an ellipse."""

    radii: EllipsoidRadii
    innerRadii: EllipsoidRadii
    minimumClock: int | float
    maximumClock: int | float
    minimumCone: int | float
    maximumCone: int | float
    show: bool
    heightReference: HeightReference
    fill: bool
    material: Material
    outline: bool
    outlineColor: Color
    outlineWidth: int | float
    stackPartitions: int
    slicePartitions: int
    subdivisions: int


@attr.s(str=False, frozen=True, kw_only=True)
class Box(BaseCZMLObject):
    """A box, which is a closed rectangular cuboid."""

    show: bool
    dimensions: BoxDimensions
    heightReference: HeightReference
    fill: bool
    material: Material
    outline: bool
    outlineColor: Color
    outlineWidth: int | float
    shadows: ShadowMode
    distanceDisplayCondition: DistanceDisplayCondition


@attr.s(str=False, frozen=True, kw_only=True)
class BoxDimensions(BaseCZMLObject, Interpolatable):
    """The width, depth, and height of a box."""

    cartesian: list[int] | list[float]
    reference: str


# noinspection PyPep8Naming
@attr.s(str=False, frozen=True, kw_only=True)
class Rectangle(BaseCZMLObject, Interpolatable, Deletable):
    """A cartographic rectangle, which conforms to the curvature of the globe and
    can be placed on the surface or at altitude and can optionally be extruded into a volume."""

    coordinates: RectangleCoordinates
    fill: bool
    material: Material


# noinspection PyPep8Naming
@attr.s(str=False, frozen=True, kw_only=True)
class RectangleCoordinates(BaseCZMLObject, Interpolatable, Deletable):
    """A set of coordinates describing a cartographic rectangle on the surface of the ellipsoid."""

    reference: str
    wsen: list[int] | list[float]
    wsenDegrees: list[int] | list[float]

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

    cartesian: list[int] | list[float]
    reference: str


@attr.s(str=False, frozen=True, kw_only=True)
class HeightReference(BaseCZMLObject, Deletable):
    """The height reference of an object, which indicates if the object's position is relative to terrain or not."""

    heightReference: HeightReference
    reference: str


# noinspection PyPep8Naming
@attr.s(str=False, frozen=True, kw_only=True)
class Clock(BaseCZMLObject):
    """Initial settings for a simulated clock when a document is loaded.

    The start and stop time are configured using the interval property.

    """

    currentTime: str
    multiplier: int | float = 1.0
    range: ClockRanges = ClockRanges.LOOP_STOP
    step: ClockSteps = ClockSteps.SYSTEM_CLOCK_MULTIPLIER


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

    show: bool
    leadTime: int | float
    trailTime: int | float
    width: int | float = 1.0
    resolution: int | float = 60.0
    material: Material
    distanceDisplayCondition: DistanceDisplayCondition


@attr.s(str=False, frozen=True, kw_only=True)
class Point(BaseCZMLObject):
    """A point, or viewport-aligned circle."""

    show: bool
    pixelSize: int | float
    heightReference: HeightReference
    color: Color
    outlineColor: Color
    outlineWidth: int | float
    scaleByDistance: list[int] | list[float]
    translucencyByDistance: list[int] | list[float]
    distanceDisplayCondition: DistanceDisplayCondition
    disableDepthTestDistance: int | float


@attr.s(str=False, frozen=True, kw_only=True)
class TileSet(BaseCZMLObject):
    """A 3D Tiles tileset."""

    show: bool
    uri: Uri
    maximumScreenSpaceError: int | float


@attr.s(str=False, frozen=True, kw_only=True)
class Wall(BaseCZMLObject):
    """A two-dimensional wall defined as a line strip and optional maximum and minimum heights.
    It conforms to the curvature of the globe and can be placed along the surface or at altitude."""

    show: bool
    positions: PositionList
    minimumHeights: list[int] | list[float]
    maximumHeights: list[int] | list[float]
    granularity: int | float
    fill: bool
    material: Material
    outline: bool
    outlineColor: Color
    outlineWidth: int | float
    shadows: ShadowMode
    distanceDisplayCondition: DistanceDisplayCondition


@attr.s(str=False, frozen=True, kw_only=True)
class NearFarScalar(BaseCZMLObject, Interpolatable, Deletable):
    """A numeric value which will be linearly interpolated between two values based on an object's distance from the
     camera, in eye coordinates.

    The computed value will interpolate between the near value and the far value while the camera distance falls
    between the near distance and the far distance, and will be clamped to the near or far value while the distance is
    less than the near distance or greater than the far distance, respectively.
    """

    nearFarScalar: list[int] | list[float]
    reference: str


# noinspection PyPep8Naming
@attr.s(str=False, frozen=True, kw_only=True)
class Label(BaseCZMLObject, HasAlignment):
    """A string of text."""

    show: bool = True
    text: str
    font: str
    style: LabelStyles = LabelStyles.FILL
    scale: int | float
    showBackground: bool
    backgroundColor: Color
    fillColor: Color
    outlineColor: Color
    outlineWidth: int | float = 1.0
    pixelOffset: list[int] | list[float]


@attr.s(str=False, frozen=True, kw_only=True)
class Orientation(BaseCZMLObject, Interpolatable, Deletable):
    """Defines an orientation.

    An orientation is a rotation that takes a vector expressed in the "body" axes of the object
    and transforms it to the Earth fixed axes.

    """

    unitQuaternion: list[int] | list[float]
    reference: str
    velocityReference: str


@attr.s(str=False, frozen=True, kw_only=True)
class Model(BaseCZMLObject):
    """A 3D model."""

    show: bool
    gltf: Uri
    scale: int | float
    minimumPixelSize: int | float
    maximumScale: int | float
    incrementallyLoadTextures: bool
    runAnimations: bool
    shadows: ShadowMode
    heightReference: HeightReference
    silhouetteColor: Color
    silhouetteSize: int | float
    color: Color
    colorBlendMode: ColorBlendModes
    colorBlendAmount: int | float
    distanceDisplayCondition: DistanceDisplayCondition
    nodeTransformations: dict[str, Any]
    articulations: dict[str, Any]


@attr.s(str=False, frozen=True, kw_only=True)
class Uri(BaseCZMLObject, Deletable):
    """A URI value.

    The URI can optionally vary with time.
    """

    uri: str

    @uri.validator
    def _check_uri(self, attribute, value):
        try:
            parse_data_uri(value)
        except ValueError as e:
            if not is_url(value):
                raise ValueError("uri must be a URL or a data URI") from e

    def to_json(self):
        return self.uri
