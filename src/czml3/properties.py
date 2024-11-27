from __future__ import annotations

import datetime as dt
from typing import Any

from pydantic import (
    BaseModel,
    Field,
    field_validator,
    model_serializer,
    model_validator,
)
from w3lib.url import is_url, parse_data_uri

from .base import BaseCZMLObject
from .common import Deletable, Interpolatable
from .enums import (
    ArcTypes,
    ClassificationTypes,
    ClockRanges,
    ClockSteps,
    ColorBlendModes,
    CornerTypes,
    HeightReferences,
    HorizontalOrigins,
    LabelStyles,
    ShadowModes,
    VerticalOrigins,
)
from .types import (
    Cartesian2Value,
    Cartesian3Value,
    CartographicDegreesListValue,
    CartographicRadiansListValue,
    DistanceDisplayConditionValue,
    NearFarScalarValue,
    RgbafValue,
    RgbaValue,
    Sequence,
    TimeInterval,
    UnitQuaternionValue,
    check_reference,
    format_datetime_like,
    get_color,
)


class HasAlignment(BaseModel):
    """A property that can be horizontally or vertically aligned."""

    horizontalOrigin: None | HorizontalOrigins = Field(default=None)
    verticalOrigin: None | VerticalOrigins = Field(default=None)


class Material(BaseCZMLObject):
    """A definition of how a surface is colored or shaded."""

    solidColor: None | Color | SolidColorMaterial | str = Field(default=None)
    image: None | ImageMaterial | str | Uri = Field(default=None)
    grid: None | GridMaterial = Field(default=None)
    stripe: None | StripeMaterial = Field(default=None)
    checkerboard: None | CheckerboardMaterial = Field(default=None)
    polylineOutline: None | PolylineMaterial = Field(
        default=None
    )  # NOTE: Not present in documentation


class PolylineOutline(BaseCZMLObject):
    """A definition of how a surface is colored or shaded."""

    color: None | Color | str = Field(default=None)
    outlineColor: None | Color | str = Field(default=None)
    outlineWidth: None | int | float = Field(default=None)


class PolylineOutlineMaterial(BaseCZMLObject):
    """A definition of the material wrapper for a polyline outline."""

    polylineOutline: None | PolylineOutline = Field(default=None)


class PolylineGlow(BaseCZMLObject):
    """A definition of how a glowing polyline appears."""

    color: None | Color | str = Field(default=None)
    glowPower: None | float | int = Field(default=None)
    taperPower: None | float | int = Field(default=None)


class PolylineGlowMaterial(BaseCZMLObject):
    """A material that fills the surface of a line with a glowing color."""

    polylineGlow: None | PolylineGlow = Field(default=None)


class PolylineArrow(BaseCZMLObject):
    """A definition of how a polyline arrow appears."""

    color: None | Color | str = Field(default=None)


class PolylineArrowMaterial(BaseCZMLObject):
    """A material that fills the surface of a line with an arrow."""

    polylineArrow: None | PolylineArrow = Field(default=None)


class PolylineDash(BaseCZMLObject):
    """A definition of how a polyline should be dashed with two colors."""

    color: None | Color | str = Field(default=None)
    gapColor: None | Color | str = Field(default=None)
    dashLength: None | float | int = Field(default=None)
    dashPattern: None | int = Field(default=None)


class PolylineDashMaterial(BaseCZMLObject):
    """A material that provides a how a polyline should be dashed."""

    polylineDash: None | PolylineDash = Field(default=None)


class PolylineMaterial(BaseCZMLObject):
    """A definition of how a surface is colored or shaded."""

    solidColor: None | SolidColorMaterial | str = Field(default=None)
    image: None | ImageMaterial | str | Uri = Field(default=None)
    grid: None | GridMaterial = Field(default=None)
    stripe: None | StripeMaterial = Field(default=None)
    checkerboard: None | CheckerboardMaterial = Field(default=None)
    polylineDash: None | PolylineDashMaterial = Field(default=None)


class SolidColorMaterial(BaseCZMLObject):
    """A material that fills the surface with a solid color."""

    color: None | Color | str = Field(default=None)


class GridMaterial(BaseCZMLObject):
    """A material that fills the surface with a two-dimensional grid."""

    color: None | Color | str = Field(default=None)
    cellAlpha: None | float | int = Field(default=None)
    lineCount: None | list[int] = Field(default=None)
    lineThickness: None | list[float] | list[int] = Field(default=None)
    lineOffset: None | list[float] | list[int] = Field(default=None)


class StripeMaterial(BaseCZMLObject):
    """A material that fills the surface with alternating colors."""

    orientation: None | int = Field(default=None)
    evenColor: None | Color | str = Field(default=None)
    oddColor: None | Color | str = Field(default=None)
    offset: None | float | int = Field(default=None)
    repeat: None | float | int = Field(default=None)


class CheckerboardMaterial(BaseCZMLObject):
    """A material that fills the surface with alternating colors."""

    evenColor: None | Color | str = Field(default=None)
    oddColor: None | Color | str = Field(default=None)
    repeat: None | int = Field(default=None)


class ImageMaterial(BaseCZMLObject):
    """A material that fills the surface with an image."""

    image: None | ImageMaterial | str | Uri = Field(default=None)
    repeat: None | list[int] = Field(default=None)
    color: None | Color | str = Field(default=None)
    transparent: None | bool = Field(default=None)


class Color(BaseCZMLObject, Interpolatable, Deletable):
    """A color. The color can optionally vary over time."""

    rgba: None | RgbaValue | str | list[float] | list[int] = Field(default=None)
    rgbaf: None | RgbafValue | str | list[float] | list[int] = Field(default=None)

    @field_validator("rgba", "rgbaf")
    @classmethod
    def is_valid(cls, color):
        return get_color(color)

    # @classmethod
    # def from_list(cls, color):
    #     if all(issubclass(type(v), int) for v in color):
    #         color = color + [255] if len(color) == 3 else color[:]
    #         return cls(rgba=RgbaValue(values=color))
    #     else:
    #         color = color + [1.0] if len(color) == 3 else color[:]
    #         return cls(rgbaf=RgbafValue(values=color))

    # @classmethod
    # def from_tuple(cls, color):
    #     return cls.from_list(list(color))

    # @classmethod
    # def from_hex(cls, color):
    #     if color > 0xFFFFFF:
    #         values = [
    #             (color & 0xFF000000) >> 24,
    #             (color & 0x00FF0000) >> 16,
    #             (color & 0x0000FF00) >> 8,
    #             (color & 0x000000FF) >> 0,
    #         ]
    #     else:
    #         values = [
    #             (color & 0xFF0000) >> 16,
    #             (color & 0x00FF00) >> 8,
    #             (color & 0x0000FF) >> 0,
    #             0xFF,
    #         ]

    #     return cls.from_list(values)

    # @classmethod
    # def from_str(cls, color):
    #     return cls.from_hex(int(color.rsplit("#")[-1], 16))


class Position(BaseCZMLObject, Interpolatable, Deletable):
    """Defines a position. The position can optionally vary over time."""

    referenceFrame: None | str = Field(default=None)
    cartesian: None | Cartesian3Value | list[float] | list[int] = Field(default=None)
    cartographicRadians: None | list[float] | list[int] = Field(default=None)
    cartographicDegrees: None | list[float] | list[int] = Field(default=None)
    cartesianVelocity: None | list[float] | list[int] = Field(default=None)
    reference: None | str = Field(default=None)
    interval: None | TimeInterval = Field(default=None)
    epoch: None | str | dt.datetime = Field(default=None)

    @model_validator(mode="after")
    def checks(self):
        if self.delete:
            return self
        if (
            sum(
                val is not None
                for val in (
                    self.cartesian,
                    self.cartographicDegrees,
                    self.cartographicRadians,
                    self.cartesianVelocity,
                )
            )
            != 1
        ):
            raise TypeError(
                "One of cartesian, cartographicDegrees, cartographicRadians or reference must be given"
            )
        return self

    @field_validator("reference")
    @classmethod
    def check_ref(cls, r):
        check_reference(r)
        return r

    @field_validator("epoch")
    @classmethod
    def check_epoch(cls, e):
        return format_datetime_like(e)


class ViewFrom(BaseCZMLObject, Interpolatable, Deletable):
    """suggested initial camera position offset when tracking this object.

    ViewFrom can optionally vary over time."""

    cartesian: None | Cartesian3Value | list[float] | list[int]
    reference: None | str = Field(default=None)

    @field_validator("reference")
    @classmethod
    def check(cls, r):
        check_reference(r)
        return r


class Billboard(BaseCZMLObject, HasAlignment):
    """A billboard, or viewport-aligned image.

    The billboard is positioned in the scene by the position property.
    A billboard is sometimes called a marker.
    """

    image: str | Uri
    show: None | bool = Field(default=None)
    scale: None | float | int = Field(default=None)
    pixelOffset: None | list[float] | list[int] = Field(default=None)
    eyeOffset: None | list[float] | list[int] = Field(default=None)
    color: None | Color | str = Field(default=None)


class EllipsoidRadii(BaseCZMLObject, Interpolatable, Deletable):
    """The radii of an ellipsoid."""

    cartesian: None | Cartesian3Value | list[float] | list[int]
    reference: None | str = Field(default=None)

    @field_validator("reference")
    @classmethod
    def check(cls, r):
        check_reference(r)
        return r


class Corridor(BaseCZMLObject):
    """A corridor , which is a shape defined by a centerline and width that conforms to the
    curvature of the body shape. It can can optionally be extruded into a volume."""

    positions: PositionList | list[int] | list[float]
    show: None | bool = Field(default=None)
    width: float | int
    height: None | float | int = Field(default=None)
    heightReference: None | HeightReference = Field(default=None)
    extrudedHeight: None | float | int = Field(default=None)
    extrudedHeightReference: None | HeightReference = Field(default=None)
    cornerType: None | CornerType = Field(default=None)
    granularity: None | float | int = Field(default=None)
    fill: None | bool = Field(default=None)
    material: None | Material | str = Field(default=None)
    outline: None | Color | str = Field(default=None)
    outlineColor: None | Color | str = Field(default=None)
    outlineWidth: None | int | float = Field(default=None)
    shadows: None | ShadowMode = Field(default=None)
    distanceDisplayCondition: None | DistanceDisplayCondition = Field(default=None)
    classificationType: None | ClassificationType = Field(default=None)
    zIndex: None | int = Field(default=None)


class Cylinder(BaseCZMLObject):
    """A cylinder, which is a special cone defined by length, top and bottom radius."""

    length: float | int
    show: None | bool = Field(default=None)
    topRadius: float | int
    bottomRadius: float | int
    heightReference: None | HeightReference = Field(default=None)
    fill: None | bool = Field(default=None)
    material: None | Material | str = Field(default=None)
    outline: None | bool = Field(default=None)
    outlineColor: None | Color | str = Field(default=None)
    outlineWidth: None | float | int = Field(default=None)
    numberOfVerticalLines: None | int = Field(default=None)
    slices: None | int = Field(default=None)
    shadows: None | ShadowMode = Field(default=None)
    distanceDisplayCondition: None | DistanceDisplayCondition = Field(default=None)


class Ellipse(BaseCZMLObject):
    """An ellipse, which is a close curve, on or above Earth's surface."""

    semiMajorAxis: float | int
    semiMinorAxis: float | int
    show: None | bool = Field(default=None)
    height: None | float | int = Field(default=None)
    heightReference: None | HeightReference = Field(default=None)
    extrudedHeight: None | float | int = Field(default=None)
    extrudedHeightReference: None | HeightReference = Field(default=None)
    rotation: None | float | int = Field(default=None)
    stRotation: None | float | int = Field(default=None)
    granularity: None | float | int = Field(default=None)
    fill: None | bool = Field(default=None)
    material: None | Material | str = Field(default=None)
    outline: None | bool = Field(default=None)
    outlineColor: None | Color | str = Field(default=None)
    outlineWidth: None | float | int = Field(default=None)
    numberOfVerticalLines: None | int = Field(default=None)
    shadows: None | ShadowMode = Field(default=None)
    distanceDisplayCondition: None | DistanceDisplayCondition = Field(default=None)
    classificationType: None | ClassificationType = Field(default=None)
    zIndex: None | int = Field(default=None)


class Polygon(BaseCZMLObject):
    """A polygon, which is a closed figure on the surface of the Earth."""

    positions: Position | PositionList | list[int] | list[float]
    show: None | bool = Field(default=None)
    arcType: None | ArcType = Field(default=None)
    granularity: None | float | int = Field(default=None)
    material: None | Material | str = Field(default=None)
    shadows: None | ShadowMode = Field(default=None)
    distanceDisplayCondition: None | DistanceDisplayCondition = Field(default=None)
    classificationType: None | ClassificationType = Field(default=None)
    zIndex: None | int = Field(default=None)
    holes: None | PositionList | PositionListOfLists | list[int] | list[float] = Field(
        default=None
    )  # NOTE: not in documentation
    outlineColor: None | Color | str = Field(default=None)
    outline: None | bool = Field(default=None)
    extrudedHeight: None | float | int = Field(default=None)
    perPositionHeight: None | bool = Field(default=None)


class Polyline(BaseCZMLObject):
    """A polyline, which is a line in the scene composed of multiple segments."""

    positions: PositionList
    show: None | bool = Field(default=None)
    arcType: None | ArcType = Field(default=None)
    width: None | float | int = Field(default=None)
    granularity: None | float | int = Field(default=None)
    material: (
        None
        | PolylineMaterial
        | PolylineDashMaterial
        | PolylineArrowMaterial
        | PolylineGlowMaterial
        | PolylineOutlineMaterial
        | str
    ) = Field(default=None)
    followSurface: None | bool = Field(default=None)
    shadows: None | ShadowMode = Field(default=None)
    depthFailMaterial: (
        None
        | PolylineMaterial
        | PolylineDashMaterial
        | PolylineArrowMaterial
        | PolylineGlowMaterial
        | PolylineOutlineMaterial
        | str
    ) = Field(default=None)
    distanceDisplayCondition: None | DistanceDisplayCondition = Field(default=None)
    clampToGround: None | bool = Field(default=None)
    classificationType: None | ClassificationType = Field(default=None)
    zIndex: None | int = Field(default=None)


class ArcType(BaseCZMLObject, Deletable):
    """The type of an arc."""

    arcType: None | ArcTypes | str = Field(default=None)
    reference: None | str = Field(default=None)

    @field_validator("reference")
    @classmethod
    def check(cls, r):
        check_reference(r)
        return r


class ShadowMode(BaseCZMLObject, Deletable):
    """Whether or not an object casts or receives shadows from each light source when shadows are enabled."""

    shadowMode: None | ShadowModes = Field(default=None)
    reference: None | str = Field(default=None)

    @field_validator("reference")
    @classmethod
    def check(cls, r):
        check_reference(r)
        return r


class ClassificationType(BaseCZMLObject, Deletable):
    """Whether a classification affects terrain, 3D Tiles, or both."""

    classificationType: None | ClassificationTypes = Field(default=None)
    reference: None | str = Field(default=None)

    @field_validator("reference")
    @classmethod
    def check(cls, r):
        check_reference(r)
        return r


class DistanceDisplayCondition(BaseCZMLObject, Interpolatable, Deletable):
    """Indicates the visibility of an object based on the distance to the camera."""

    distanceDisplayCondition: None | DistanceDisplayConditionValue = Field(default=None)
    reference: None | str = Field(default=None)

    @field_validator("reference")
    @classmethod
    def check(cls, r):
        check_reference(r)
        return r


class PositionListOfLists(BaseCZMLObject, Deletable):
    """A list of positions."""

    referenceFrame: None | str | list[str] = Field(default=None)
    cartesian: None | Cartesian3Value = Field(default=None)
    cartographicRadians: (
        None | list[float] | list[int] | list[list[float]] | list[list[int]]
    ) = Field(default=None)
    cartographicDegrees: (
        None | list[float] | list[int] | list[list[float]] | list[list[int]]
    ) = Field(default=None)
    references: None | str | list[str] = Field(default=None)


class PositionList(BaseCZMLObject, Interpolatable, Deletable):
    """A list of positions."""

    referenceFrame: None | str | list[str] = Field(default=None)
    cartesian: None | Cartesian3Value | list[float] | list[int] = Field(default=None)
    cartographicRadians: (
        None | list[float] | list[int] | CartographicRadiansListValue
    ) = Field(default=None)
    cartographicDegrees: (
        None | list[float] | list[int] | CartographicDegreesListValue
    ) = Field(default=None)
    references: None | str | list[str] = Field(default=None)
    interval: None | TimeInterval = Field(default=None)
    epoch: None | str | dt.datetime = Field(default=None)  # note: not documented

    @field_validator("epoch")
    @classmethod
    def check(cls, e):
        return format_datetime_like(e)


class Ellipsoid(BaseCZMLObject):
    """A closed quadric surface that is a three-dimensional analogue of an ellipse."""

    radii: EllipsoidRadii
    innerRadii: None | EllipsoidRadii = Field(default=None)
    minimumClock: None | float | int = Field(default=None)
    maximumClock: None | float | int = Field(default=None)
    minimumCone: None | float | int = Field(default=None)
    maximumCone: None | float | int = Field(default=None)
    show: None | bool = Field(default=None)
    heightReference: None | HeightReference = Field(default=None)
    fill: None | bool = Field(default=None)
    material: None | Material | str = Field(default=None)
    outline: None | bool = Field(default=None)
    outlineColor: None | Color | str = Field(default=None)
    outlineWidth: None | float | int = Field(default=None)
    stackPartitions: None | int = Field(default=None)
    slicePartitions: None | int = Field(default=None)
    subdivisions: None | int = Field(default=None)


class Box(BaseCZMLObject):
    """A box, which is a closed rectangular cuboid."""

    show: None | bool = Field(default=None)
    dimensions: None | BoxDimensions = Field(default=None)
    heightReference: None | HeightReference = Field(default=None)
    fill: None | bool = Field(default=None)
    material: None | Material | str = Field(default=None)
    outline: None | bool = Field(default=None)
    outlineColor: None | Color | str = Field(default=None)
    outlineWidth: None | float | int = Field(default=None)
    shadows: None | ShadowMode = Field(default=None)
    distanceDisplayCondition: None | DistanceDisplayCondition = Field(default=None)


class BoxDimensions(BaseCZMLObject, Interpolatable):
    """The width, depth, and height of a box."""

    cartesian: None | Cartesian3Value = Field(default=None)
    reference: None | str = Field(default=None)

    @field_validator("reference")
    @classmethod
    def check(cls, r):
        check_reference(r)
        return r


class Rectangle(BaseCZMLObject, Interpolatable, Deletable):
    """A cartographic rectangle, which conforms to the curvature of the globe and
    can be placed on the surface or at altitude and can optionally be extruded into a volume.
    """

    coordinates: None | RectangleCoordinates = Field(default=None)
    fill: None | bool = Field(default=None)
    material: None | Material | str = Field(default=None)


class RectangleCoordinates(BaseCZMLObject, Interpolatable, Deletable):
    """A set of coordinates describing a cartographic rectangle on the surface of the ellipsoid."""

    wsen: None | list[float] | list[int] = Field(default=None)
    wsenDegrees: None | list[float] | list[int] = Field(default=None)
    reference: None | str = Field(default=None)

    @model_validator(mode="after")
    def checks(self):
        if self.delete:
            return self
        if sum(val is not None for val in (self.wsen, self.wsenDegrees)) != 1:
            raise TypeError("One of wsen or wsenDegrees must be given")
        return self

    @field_validator("reference")
    @classmethod
    def check(cls, r):
        check_reference(r)
        return r


class EyeOffset(BaseCZMLObject, Deletable):
    """An offset in eye coordinates which can optionally vary over time.

    Eye coordinates are a left-handed coordinate system
    where the X-axis points toward the viewer's right,
    the Y-axis poitns up, and the Z-axis points into the screen.

    """

    cartesian: None | Cartesian3Value | list[float] | list[int] = Field(default=None)
    reference: None | str = Field(default=None)

    @field_validator("reference")
    @classmethod
    def check(cls, r):
        check_reference(r)
        return r


class HeightReference(BaseCZMLObject, Deletable):
    """The height reference of an object, which indicates if the object's position is relative to terrain or not."""

    heightReference: None | HeightReferences = Field(default=None)
    reference: None | str = Field(default=None)

    @field_validator("reference")
    @classmethod
    def check(cls, r):
        check_reference(r)
        return r


class ColorBlendMode(BaseCZMLObject, Deletable):
    """The height reference of an object, which indicates if the object's position is relative to terrain or not."""

    colorBlendMode: None | ColorBlendModes = Field(default=None)
    reference: None | str = Field(default=None)

    @field_validator("reference")
    @classmethod
    def check(cls, r):
        check_reference(r)
        return r


class CornerType(BaseCZMLObject, Deletable):
    """The height reference of an object, which indicates if the object's position is relative to terrain or not."""

    cornerType: None | CornerTypes = Field(default=None)
    reference: None | str = Field(default=None)

    @field_validator("reference")
    @classmethod
    def check(cls, r):
        check_reference(r)
        return r


class Clock(BaseCZMLObject):
    """Initial settings for a simulated clock when a document is loaded.

    The start and stop time are configured using the interval property.

    """

    currentTime: None | str | dt.datetime = Field(default=None)
    multiplier: None | float | int = Field(default=None)
    range: None | ClockRanges = Field(default=None)
    step: None | ClockSteps = Field(default=None)

    @field_validator("currentTime")
    @classmethod
    def format_time(cls, time):
        return format_datetime_like(time)


class Path(BaseCZMLObject):
    """A path, which is a polyline defined by the motion of an object over time.

    The possible vertices of the path are specified by the position property.
    Note that because clients cannot render a truly infinite path,
    the path must be limited,
    either by defining availability for this object,
    or by using the leadTime and trailTime properties.

    """

    show: None | bool | Sequence = Field(default=None)
    leadTime: None | float | int = Field(default=None)
    trailTime: None | float | int = Field(default=None)
    width: None | float | int = Field(default=None)
    resolution: None | float | int = Field(default=None)
    material: None | Material | str = Field(default=None)
    distanceDisplayCondition: None | DistanceDisplayCondition = Field(default=None)


class Point(BaseCZMLObject):
    """A point, or viewport-aligned circle."""

    show: None | bool = Field(default=None)
    pixelSize: None | float | int = Field(default=None)
    heightReference: None | HeightReference = Field(default=None)
    color: None | Color | str = Field(default=None)
    outlineColor: None | Color | str = Field(default=None)
    outlineWidth: None | float | int = Field(default=None)
    scaleByDistance: None | NearFarScalar = Field(default=None)
    translucencyByDistance: None | NearFarScalar = Field(default=None)
    distanceDisplayCondition: None | DistanceDisplayCondition = Field(default=None)
    disableDepthTestDistance: None | float | int = Field(default=None)


class Tileset(BaseCZMLObject):
    """A 3D Tiles tileset."""

    uri: str | Uri
    show: None | bool = Field(default=None)
    maximumScreenSpaceError: None | float | int = Field(default=None)


class Wall(BaseCZMLObject):
    """A two-dimensional wall defined as a line strip and optional maximum and minimum heights.
    It conforms to the curvature of the globe and can be placed along the surface or at altitude.
    """

    show: None | bool = Field(default=None)
    positions: PositionList
    minimumHeights: None | list[float] | list[int] = Field(default=None)
    maximumHeights: None | list[float] | list[int] = Field(default=None)
    granularity: None | float | int = Field(default=None)
    fill: None | bool = Field(default=None)
    material: None | Material | str = Field(default=None)
    outline: None | bool = Field(default=None)
    outlineColor: None | Color | str = Field(default=None)
    outlineWidth: None | float | int = Field(default=None)
    shadows: None | ShadowMode = Field(default=None)
    distanceDisplayCondition: None | DistanceDisplayCondition = Field(default=None)


class NearFarScalar(BaseCZMLObject, Interpolatable, Deletable):
    """A numeric value which will be linearly interpolated between two values based on an object's distance from the
     camera, in eye coordinates.

    The computed value will interpolate between the near value and the far value while the camera distance falls
    between the near distance and the far distance, and will be clamped to the near or far value while the distance is
    less than the near distance or greater than the far distance, respectively.
    """

    nearFarScalar: None | list[float] | list[int] | NearFarScalarValue = Field(
        default=None
    )
    reference: None | str = Field(default=None)

    @field_validator("reference")
    @classmethod
    def check(cls, r):
        check_reference(r)
        return r


class Label(BaseCZMLObject, HasAlignment):
    """A string of text."""

    show: None | bool = Field(default=None)
    text: None | str = Field(default=None)
    font: None | str = Field(default=None)
    style: None | LabelStyles = Field(default=None)
    scale: None | float | int = Field(default=None)
    showBackground: None | bool = Field(default=None)
    backgroundColor: None | Color | str = Field(default=None)
    fillColor: None | Color | str = Field(default=None)
    outlineColor: None | Color | str = Field(default=None)
    outlineWidth: None | float | int = Field(default=None)
    pixelOffset: None | float | int | Cartesian2Value = Field(default=None)


class Orientation(BaseCZMLObject, Interpolatable, Deletable):
    """Defines an orientation.

    An orientation is a rotation that takes a vector expressed in the "body" axes of the object
    and transforms it to the Earth fixed axes.

    """

    unitQuaternion: None | list[float] | list[int] | UnitQuaternionValue = Field(
        default=None
    )
    reference: None | str = Field(default=None)
    velocityReference: None | str = Field(default=None)

    @field_validator("reference")
    @classmethod
    def check(cls, r):
        check_reference(r)
        return r


class Model(BaseCZMLObject):
    """A 3D model."""

    show: None | bool = Field(default=None)
    gltf: str
    scale: None | float | int = Field(default=None)
    minimumPixelSize: None | float | int = Field(default=None)
    maximumScale: None | float | int = Field(default=None)
    incrementallyLoadTextures: None | bool = Field(default=None)
    runAnimations: None | bool = Field(default=None)
    shadows: None | ShadowMode = Field(default=None)
    heightReference: None | HeightReference = Field(default=None)
    silhouetteColor: None | Color | str = Field(default=None)
    silhouetteSize: None | Color | str = Field(default=None)
    color: None | Color | str = Field(default=None)
    colorBlendMode: None | ColorBlendMode = Field(default=None)
    colorBlendAmount: None | float | int = Field(default=None)
    distanceDisplayCondition: None | DistanceDisplayCondition = Field(default=None)
    nodeTransformations: None | Any = Field(default=None)
    articulations: None | Any = Field(default=None)


class Uri(BaseCZMLObject, Deletable):
    """A URI value.

    The URI can optionally vary with time.
    """

    uri: None | str = Field(default=None)

    @field_validator("uri")
    @classmethod
    def _check_uri(cls, value: str):
        if is_url(value):
            return value
        try:
            parse_data_uri(value)
        except ValueError:
            raise TypeError("uri must be a URL or a data URI") from None
        return value

    @model_serializer
    def custom_serializer(self) -> None | str:
        return self.uri
