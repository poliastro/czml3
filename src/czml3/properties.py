from __future__ import annotations

import datetime as dt
from typing import Any, List, Union

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

    horizontalOrigin: Union[None, HorizontalOrigins] = Field(default=None)
    verticalOrigin: Union[None, VerticalOrigins] = Field(default=None)


class Material(BaseCZMLObject):
    """A definition of how a surface is colored or shaded."""

    solidColor: Union[None, Color, SolidColorMaterial, str] = Field(default=None)
    image: Union[None, ImageMaterial, str, Uri] = Field(default=None)
    grid: Union[None, GridMaterial] = Field(default=None)
    stripe: Union[None, StripeMaterial] = Field(default=None)
    checkerboard: Union[None, CheckerboardMaterial] = Field(default=None)
    polylineOutline: Union[None, PolylineMaterial] = Field(
        default=None
    )  # NOTE: Not present in documentation


class PolylineOutline(BaseCZMLObject):
    """A definition of how a surface is colored or shaded."""

    color: Union[None, Color, str] = Field(default=None)
    outlineColor: Union[None, Color, str] = Field(default=None)
    outlineWidth: Union[None, int, float] = Field(default=None)


class PolylineOutlineMaterial(BaseCZMLObject):
    """A definition of the material wrapper for a polyline outline."""

    polylineOutline: Union[None, PolylineOutline] = Field(default=None)


class PolylineGlow(BaseCZMLObject):
    """A definition of how a glowing polyline appears."""

    color: Union[None, Color, str] = Field(default=None)
    glowPower: Union[None, float, int] = Field(default=None)
    taperPower: Union[None, float, int] = Field(default=None)


class PolylineGlowMaterial(BaseCZMLObject):
    """A material that fills the surface of a line with a glowing color."""

    polylineGlow: Union[None, PolylineGlow] = Field(default=None)


class PolylineArrow(BaseCZMLObject):
    """A definition of how a polyline arrow appears."""

    color: Union[None, Color, str] = Field(default=None)


class PolylineArrowMaterial(BaseCZMLObject):
    """A material that fills the surface of a line with an arrow."""

    polylineArrow: Union[None, PolylineArrow] = Field(default=None)


class PolylineDash(BaseCZMLObject):
    """A definition of how a polyline should be dashed with two colors."""

    color: Union[None, Color, str] = Field(default=None)
    gapColor: Union[None, Color, str] = Field(default=None)
    dashLength: Union[None, float, int] = Field(default=None)
    dashPattern: Union[None, int] = Field(default=None)


class PolylineDashMaterial(BaseCZMLObject):
    """A material that provides a how a polyline should be dashed."""

    polylineDash: Union[None, PolylineDash] = Field(default=None)


class PolylineMaterial(BaseCZMLObject):
    """A definition of how a surface is colored or shaded."""

    solidColor: Union[None, SolidColorMaterial, str] = Field(default=None)
    image: Union[None, ImageMaterial, str, Uri] = Field(default=None)
    grid: Union[None, GridMaterial] = Field(default=None)
    stripe: Union[None, StripeMaterial] = Field(default=None)
    checkerboard: Union[None, CheckerboardMaterial] = Field(default=None)
    polylineDash: Union[None, PolylineDashMaterial] = Field(default=None)


class SolidColorMaterial(BaseCZMLObject):
    """A material that fills the surface with a solid color."""

    color: Union[None, Color, str] = Field(default=None)


class GridMaterial(BaseCZMLObject):
    """A material that fills the surface with a two-dimensional grid."""

    color: Union[None, Color, str] = Field(default=None)
    cellAlpha: Union[None, float, int] = Field(default=None)
    lineCount: Union[None, List[int]] = Field(default=None)
    lineThickness: Union[None, List[float], List[int]] = Field(default=None)
    lineOffset: Union[None, List[float], List[int]] = Field(default=None)


class StripeMaterial(BaseCZMLObject):
    """A material that fills the surface with alternating colors."""

    orientation: Union[None, int] = Field(default=None)
    evenColor: Union[None, Color, str] = Field(default=None)
    oddColor: Union[None, Color, str] = Field(default=None)
    offset: Union[None, float, int] = Field(default=None)
    repeat: Union[None, float, int] = Field(default=None)


class CheckerboardMaterial(BaseCZMLObject):
    """A material that fills the surface with alternating colors."""

    evenColor: Union[None, Color, str] = Field(default=None)
    oddColor: Union[None, Color, str] = Field(default=None)
    repeat: Union[None, int] = Field(default=None)


class ImageMaterial(BaseCZMLObject):
    """A material that fills the surface with an image."""

    image: Union[None, ImageMaterial, str, Uri] = Field(default=None)
    repeat: Union[None, List[int]] = Field(default=None)
    color: Union[None, Color, str] = Field(default=None)
    transparent: Union[None, bool] = Field(default=None)


class Color(BaseCZMLObject, Interpolatable, Deletable):
    """A color. The color can optionally vary over time."""

    rgba: Union[None, RgbaValue, str, List[float], List[int]] = Field(default=None)
    rgbaf: Union[None, RgbafValue, str, List[float], List[int]] = Field(default=None)

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

    referenceFrame: Union[None, str] = Field(default=None)
    cartesian: Union[None, Cartesian3Value, List[float], List[int]] = Field(
        default=None
    )
    cartographicRadians: Union[None, List[float], List[int]] = Field(default=None)
    cartographicDegrees: Union[None, List[float], List[int]] = Field(default=None)
    cartesianVelocity: Union[None, List[float], List[int]] = Field(default=None)
    reference: Union[None, str] = Field(default=None)
    interval: Union[None, TimeInterval] = Field(default=None)
    epoch: Union[None, str, dt.datetime] = Field(default=None)

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

    cartesian: Union[None, Cartesian3Value, List[float], List[int]]
    reference: Union[None, str] = Field(default=None)

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

    image: Union[str, Uri]
    show: Union[None, bool] = Field(default=None)
    scale: Union[None, float, int] = Field(default=None)
    pixelOffset: Union[None, List[float], List[int]] = Field(default=None)
    eyeOffset: Union[None, List[float], List[int]] = Field(default=None)
    color: Union[None, Color, str] = Field(default=None)


class EllipsoidRadii(BaseCZMLObject, Interpolatable, Deletable):
    """The radii of an ellipsoid."""

    cartesian: Union[None, Cartesian3Value, List[float], List[int]]
    reference: Union[None, str] = Field(default=None)

    @field_validator("reference")
    @classmethod
    def check(cls, r):
        check_reference(r)
        return r


class Corridor(BaseCZMLObject):
    """A corridor , which is a shape defined by a centerline and width that conforms to the
    curvature of the body shape. It can can optionally be extruded into a volume."""

    positions: Union[PositionList, List[int], List[float]]
    show: Union[None, bool] = Field(default=None)
    width: Union[float, int]
    height: Union[None, float, int] = Field(default=None)
    heightReference: Union[None, HeightReference] = Field(default=None)
    extrudedHeight: Union[None, float, int] = Field(default=None)
    extrudedHeightReference: Union[None, HeightReference] = Field(default=None)
    cornerType: Union[None, CornerType] = Field(default=None)
    granularity: Union[None, float, int] = Field(default=None)
    fill: Union[None, bool] = Field(default=None)
    material: Union[None, Material, str] = Field(default=None)
    outline: Union[None, Color, str] = Field(default=None)
    outlineColor: Union[None, Color, str] = Field(default=None)
    outlineWidth: Union[None, int, float] = Field(default=None)
    shadows: Union[None, ShadowMode] = Field(default=None)
    distanceDisplayCondition: Union[None, DistanceDisplayCondition] = Field(
        default=None
    )
    classificationType: Union[None, ClassificationType] = Field(default=None)
    zIndex: Union[None, int] = Field(default=None)


class Cylinder(BaseCZMLObject):
    """A cylinder, which is a special cone defined by length, top and bottom radius."""

    length: Union[float, int]
    show: Union[None, bool] = Field(default=None)
    topRadius: Union[float, int]
    bottomRadius: Union[float, int]
    heightReference: Union[None, HeightReference] = Field(default=None)
    fill: Union[None, bool] = Field(default=None)
    material: Union[None, Material, str] = Field(default=None)
    outline: Union[None, bool] = Field(default=None)
    outlineColor: Union[None, Color, str] = Field(default=None)
    outlineWidth: Union[None, float, int] = Field(default=None)
    numberOfVerticalLines: Union[None, int] = Field(default=None)
    slices: Union[None, int] = Field(default=None)
    shadows: Union[None, ShadowMode] = Field(default=None)
    distanceDisplayCondition: Union[None, DistanceDisplayCondition] = Field(
        default=None
    )


class Ellipse(BaseCZMLObject):
    """An ellipse, which is a close curve, on or above Earth's surface."""

    semiMajorAxis: Union[float, int]
    semiMinorAxis: Union[float, int]
    show: Union[None, bool] = Field(default=None)
    height: Union[None, float, int] = Field(default=None)
    heightReference: Union[None, HeightReference] = Field(default=None)
    extrudedHeight: Union[None, float, int] = Field(default=None)
    extrudedHeightReference: Union[None, HeightReference] = Field(default=None)
    rotation: Union[None, float, int] = Field(default=None)
    stRotation: Union[None, float, int] = Field(default=None)
    granularity: Union[None, float, int] = Field(default=None)
    fill: Union[None, bool] = Field(default=None)
    material: Union[None, Material, str] = Field(default=None)
    outline: Union[None, bool] = Field(default=None)
    outlineColor: Union[None, Color, str] = Field(default=None)
    outlineWidth: Union[None, float, int] = Field(default=None)
    numberOfVerticalLines: Union[None, int] = Field(default=None)
    shadows: Union[None, ShadowMode] = Field(default=None)
    distanceDisplayCondition: Union[None, DistanceDisplayCondition] = Field(
        default=None
    )
    classificationType: Union[None, ClassificationType] = Field(default=None)
    zIndex: Union[None, int] = Field(default=None)


class Polygon(BaseCZMLObject):
    """A polygon, which is a closed figure on the surface of the Earth."""

    positions: Union[Position, PositionList, List[int], List[float]]
    show: Union[None, bool] = Field(default=None)
    arcType: Union[None, ArcType] = Field(default=None)
    granularity: Union[None, float, int] = Field(default=None)
    material: Union[None, Material, str] = Field(default=None)
    shadows: Union[None, ShadowMode] = Field(default=None)
    distanceDisplayCondition: Union[None, DistanceDisplayCondition] = Field(
        default=None
    )
    classificationType: Union[None, ClassificationType] = Field(default=None)
    zIndex: Union[None, int] = Field(default=None)
    holes: Union[None, PositionList, PositionListOfLists, List[int], List[float]] = (
        Field(default=None)
    )  # NOTE: not in documentation
    outlineColor: Union[None, Color, str] = Field(default=None)
    outline: Union[None, bool] = Field(default=None)
    extrudedHeight: Union[None, float, int] = Field(default=None)
    perPositionHeight: Union[None, bool] = Field(default=None)


class Polyline(BaseCZMLObject):
    """A polyline, which is a line in the scene composed of multiple segments."""

    positions: PositionList
    show: Union[None, bool] = Field(default=None)
    arcType: Union[None, ArcType] = Field(default=None)
    width: Union[None, float, int] = Field(default=None)
    granularity: Union[None, float, int] = Field(default=None)
    material: Union[
        None,
        PolylineMaterial,
        PolylineDashMaterial,
        PolylineArrowMaterial,
        PolylineGlowMaterial,
        PolylineOutlineMaterial,
        str,
    ] = Field(default=None)
    followSurface: Union[None, bool] = Field(default=None)
    shadows: Union[None, ShadowMode] = Field(default=None)
    depthFailMaterial: Union[
        None,
        PolylineMaterial,
        PolylineDashMaterial,
        PolylineArrowMaterial,
        PolylineGlowMaterial,
        PolylineOutlineMaterial,
        str,
    ] = Field(default=None)
    distanceDisplayCondition: Union[None, DistanceDisplayCondition] = Field(
        default=None
    )
    clampToGround: Union[None, bool] = Field(default=None)
    classificationType: Union[None, ClassificationType] = Field(default=None)
    zIndex: Union[None, int] = Field(default=None)


class ArcType(BaseCZMLObject, Deletable):
    """The type of an arc."""

    arcType: Union[None, ArcTypes, str] = Field(default=None)
    reference: Union[None, str] = Field(default=None)

    @field_validator("reference")
    @classmethod
    def check(cls, r):
        check_reference(r)
        return r


class ShadowMode(BaseCZMLObject, Deletable):
    """Whether or not an object casts or receives shadows from each light source when shadows are enabled."""

    shadowMode: Union[None, ShadowModes] = Field(default=None)
    reference: Union[None, str] = Field(default=None)

    @field_validator("reference")
    @classmethod
    def check(cls, r):
        check_reference(r)
        return r


class ClassificationType(BaseCZMLObject, Deletable):
    """Whether a classification affects terrain, 3D Tiles, or both."""

    classificationType: Union[None, ClassificationTypes] = Field(default=None)
    reference: Union[None, str] = Field(default=None)

    @field_validator("reference")
    @classmethod
    def check(cls, r):
        check_reference(r)
        return r


class DistanceDisplayCondition(BaseCZMLObject, Interpolatable, Deletable):
    """Indicates the visibility of an object based on the distance to the camera."""

    distanceDisplayCondition: Union[None, DistanceDisplayConditionValue] = Field(
        default=None
    )
    reference: Union[None, str] = Field(default=None)

    @field_validator("reference")
    @classmethod
    def check(cls, r):
        check_reference(r)
        return r


class PositionListOfLists(BaseCZMLObject, Deletable):
    """A list of positions."""

    referenceFrame: Union[None, str, List[str]] = Field(default=None)
    cartesian: Union[None, Cartesian3Value] = Field(default=None)
    cartographicRadians: Union[
        None, List[float], List[int], List[List[float]], List[List[int]]
    ] = Field(default=None)
    cartographicDegrees: Union[
        None, List[float], List[int], List[List[float]], List[List[int]]
    ] = Field(default=None)
    references: Union[None, str, List[str]] = Field(default=None)


class PositionList(BaseCZMLObject, Interpolatable, Deletable):
    """A list of positions."""

    referenceFrame: Union[None, str, List[str]] = Field(default=None)
    cartesian: Union[None, Cartesian3Value, List[float], List[int]] = Field(
        default=None
    )
    cartographicRadians: Union[
        None, List[float], List[int], CartographicRadiansListValue
    ] = Field(default=None)
    cartographicDegrees: Union[
        None, List[float], List[int], CartographicDegreesListValue
    ] = Field(default=None)
    references: Union[None, str, List[str]] = Field(default=None)
    interval: Union[None, TimeInterval] = Field(default=None)
    epoch: Union[None, str, dt.datetime] = Field(default=None)  # note: not documented

    @field_validator("epoch")
    @classmethod
    def check(cls, e):
        return format_datetime_like(e)


class Ellipsoid(BaseCZMLObject):
    """A closed quadric surface that is a three-dimensional analogue of an ellipse."""

    radii: EllipsoidRadii
    innerRadii: Union[None, EllipsoidRadii] = Field(default=None)
    minimumClock: Union[None, float, int] = Field(default=None)
    maximumClock: Union[None, float, int] = Field(default=None)
    minimumCone: Union[None, float, int] = Field(default=None)
    maximumCone: Union[None, float, int] = Field(default=None)
    show: Union[None, bool] = Field(default=None)
    heightReference: Union[None, HeightReference] = Field(default=None)
    fill: Union[None, bool] = Field(default=None)
    material: Union[None, Material, str] = Field(default=None)
    outline: Union[None, bool] = Field(default=None)
    outlineColor: Union[None, Color, str] = Field(default=None)
    outlineWidth: Union[None, float, int] = Field(default=None)
    stackPartitions: Union[None, int] = Field(default=None)
    slicePartitions: Union[None, int] = Field(default=None)
    subdivisions: Union[None, int] = Field(default=None)


class Box(BaseCZMLObject):
    """A box, which is a closed rectangular cuboid."""

    show: Union[None, bool] = Field(default=None)
    dimensions: Union[None, BoxDimensions] = Field(default=None)
    heightReference: Union[None, HeightReference] = Field(default=None)
    fill: Union[None, bool] = Field(default=None)
    material: Union[None, Material, str] = Field(default=None)
    outline: Union[None, bool] = Field(default=None)
    outlineColor: Union[None, Color, str] = Field(default=None)
    outlineWidth: Union[None, float, int] = Field(default=None)
    shadows: Union[None, ShadowMode] = Field(default=None)
    distanceDisplayCondition: Union[None, DistanceDisplayCondition] = Field(
        default=None
    )


class BoxDimensions(BaseCZMLObject, Interpolatable):
    """The width, depth, and height of a box."""

    cartesian: Union[None, Cartesian3Value] = Field(default=None)
    reference: Union[None, str] = Field(default=None)

    @field_validator("reference")
    @classmethod
    def check(cls, r):
        check_reference(r)
        return r


class Rectangle(BaseCZMLObject, Interpolatable, Deletable):
    """A cartographic rectangle, which conforms to the curvature of the globe and
    can be placed on the surface or at altitude and can optionally be extruded into a volume.
    """

    coordinates: Union[None, RectangleCoordinates] = Field(default=None)
    fill: Union[None, bool] = Field(default=None)
    material: Union[None, Material, str] = Field(default=None)


class RectangleCoordinates(BaseCZMLObject, Interpolatable, Deletable):
    """A set of coordinates describing a cartographic rectangle on the surface of the ellipsoid."""

    wsen: Union[None, List[float], List[int]] = Field(default=None)
    wsenDegrees: Union[None, List[float], List[int]] = Field(default=None)
    reference: Union[None, str] = Field(default=None)

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

    cartesian: Union[None, Cartesian3Value, List[float], List[int]] = Field(
        default=None
    )
    reference: Union[None, str] = Field(default=None)

    @field_validator("reference")
    @classmethod
    def check(cls, r):
        check_reference(r)
        return r


class HeightReference(BaseCZMLObject, Deletable):
    """The height reference of an object, which indicates if the object's position is relative to terrain or not."""

    heightReference: Union[None, HeightReferences] = Field(default=None)
    reference: Union[None, str] = Field(default=None)

    @field_validator("reference")
    @classmethod
    def check(cls, r):
        check_reference(r)
        return r


class ColorBlendMode(BaseCZMLObject, Deletable):
    """The height reference of an object, which indicates if the object's position is relative to terrain or not."""

    colorBlendMode: Union[None, ColorBlendModes] = Field(default=None)
    reference: Union[None, str] = Field(default=None)

    @field_validator("reference")
    @classmethod
    def check(cls, r):
        check_reference(r)
        return r


class CornerType(BaseCZMLObject, Deletable):
    """The height reference of an object, which indicates if the object's position is relative to terrain or not."""

    cornerType: Union[None, CornerTypes] = Field(default=None)
    reference: Union[None, str] = Field(default=None)

    @field_validator("reference")
    @classmethod
    def check(cls, r):
        check_reference(r)
        return r


class Clock(BaseCZMLObject):
    """Initial settings for a simulated clock when a document is loaded.

    The start and stop time are configured using the interval property.

    """

    currentTime: Union[None, str, dt.datetime] = Field(default=None)
    multiplier: Union[None, float, int] = Field(default=None)
    range: Union[None, ClockRanges] = Field(default=None)
    step: Union[None, ClockSteps] = Field(default=None)

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

    show: Union[None, bool, Sequence] = Field(default=None)
    leadTime: Union[None, float, int] = Field(default=None)
    trailTime: Union[None, float, int] = Field(default=None)
    width: Union[None, float, int] = Field(default=None)
    resolution: Union[None, float, int] = Field(default=None)
    material: Union[None, Material, str] = Field(default=None)
    distanceDisplayCondition: Union[None, DistanceDisplayCondition] = Field(
        default=None
    )


class Point(BaseCZMLObject):
    """A point, or viewport-aligned circle."""

    show: Union[None, bool] = Field(default=None)
    pixelSize: Union[None, float, int] = Field(default=None)
    heightReference: Union[None, HeightReference] = Field(default=None)
    color: Union[None, Color, str] = Field(default=None)
    outlineColor: Union[None, Color, str] = Field(default=None)
    outlineWidth: Union[None, float, int] = Field(default=None)
    scaleByDistance: Union[None, NearFarScalar] = Field(default=None)
    translucencyByDistance: Union[None, NearFarScalar] = Field(default=None)
    distanceDisplayCondition: Union[None, DistanceDisplayCondition] = Field(
        default=None
    )
    disableDepthTestDistance: Union[None, float, int] = Field(default=None)


class Tileset(BaseCZMLObject):
    """A 3D Tiles tileset."""

    uri: Union[str, Uri]
    show: Union[None, bool] = Field(default=None)
    maximumScreenSpaceError: Union[None, float, int] = Field(default=None)


class Wall(BaseCZMLObject):
    """A two-dimensional wall defined as a line strip and optional maximum and minimum heights.
    It conforms to the curvature of the globe and can be placed along the surface or at altitude.
    """

    show: Union[None, bool] = Field(default=None)
    positions: PositionList
    minimumHeights: Union[None, List[float], List[int]] = Field(default=None)
    maximumHeights: Union[None, List[float], List[int]] = Field(default=None)
    granularity: Union[None, float, int] = Field(default=None)
    fill: Union[None, bool] = Field(default=None)
    material: Union[None, Material, str] = Field(default=None)
    outline: Union[None, bool] = Field(default=None)
    outlineColor: Union[None, Color, str] = Field(default=None)
    outlineWidth: Union[None, float, int] = Field(default=None)
    shadows: Union[None, ShadowMode] = Field(default=None)
    distanceDisplayCondition: Union[None, DistanceDisplayCondition] = Field(
        default=None
    )


class NearFarScalar(BaseCZMLObject, Interpolatable, Deletable):
    """A numeric value which will be linearly interpolated between two values based on an object's distance from the
     camera, in eye coordinates.

    The computed value will interpolate between the near value and the far value while the camera distance falls
    between the near distance and the far distance, and will be clamped to the near or far value while the distance is
    less than the near distance or greater than the far distance, respectively.
    """

    nearFarScalar: Union[None, List[float], List[int], NearFarScalarValue] = Field(
        default=None
    )
    reference: Union[None, str] = Field(default=None)

    @field_validator("reference")
    @classmethod
    def check(cls, r):
        check_reference(r)
        return r


class Label(BaseCZMLObject, HasAlignment):
    """A string of text."""

    show: Union[None, bool] = Field(default=None)
    text: Union[None, str] = Field(default=None)
    font: Union[None, str] = Field(default=None)
    style: Union[None, LabelStyles] = Field(default=None)
    scale: Union[None, float, int] = Field(default=None)
    showBackground: Union[None, bool] = Field(default=None)
    backgroundColor: Union[None, Color, str] = Field(default=None)
    fillColor: Union[None, Color, str] = Field(default=None)
    outlineColor: Union[None, Color, str] = Field(default=None)
    outlineWidth: Union[None, float, int] = Field(default=None)
    pixelOffset: Union[None, float, int, Cartesian2Value] = Field(default=None)


class Orientation(BaseCZMLObject, Interpolatable, Deletable):
    """Defines an orientation.

    An orientation is a rotation that takes a vector expressed in the "body" axes of the object
    and transforms it to the Earth fixed axes.

    """

    unitQuaternion: Union[None, List[float], List[int], UnitQuaternionValue] = Field(
        default=None
    )
    reference: Union[None, str] = Field(default=None)
    velocityReference: Union[None, str] = Field(default=None)

    @field_validator("reference")
    @classmethod
    def check(cls, r):
        check_reference(r)
        return r


class Model(BaseCZMLObject):
    """A 3D model."""

    show: Union[None, bool] = Field(default=None)
    gltf: str
    scale: Union[None, float, int] = Field(default=None)
    minimumPixelSize: Union[None, float, int] = Field(default=None)
    maximumScale: Union[None, float, int] = Field(default=None)
    incrementallyLoadTextures: Union[None, bool] = Field(default=None)
    runAnimations: Union[None, bool] = Field(default=None)
    shadows: Union[None, ShadowMode] = Field(default=None)
    heightReference: Union[None, HeightReference] = Field(default=None)
    silhouetteColor: Union[None, Color, str] = Field(default=None)
    silhouetteSize: Union[None, Color, str] = Field(default=None)
    color: Union[None, Color, str] = Field(default=None)
    colorBlendMode: Union[None, ColorBlendMode] = Field(default=None)
    colorBlendAmount: Union[None, float, int] = Field(default=None)
    distanceDisplayCondition: Union[None, DistanceDisplayCondition] = Field(
        default=None
    )
    nodeTransformations: Union[None, Any] = Field(default=None)
    articulations: Union[None, Any] = Field(default=None)


class Uri(BaseCZMLObject, Deletable):
    """A URI value.

    The URI can optionally vary with time.
    """

    uri: Union[None, str] = Field(default=None)

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
    def custom_serializer(self) -> Union[None, str]:
        return self.uri
