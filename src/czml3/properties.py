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
    Cartesian3ListValue,
    Cartesian3Value,
    Cartesian3VelocityValue,
    CartographicDegreesListValue,
    CartographicDegreesValue,
    CartographicRadiansListValue,
    CartographicRadiansValue,
    DistanceDisplayConditionValue,
    NearFarScalarValue,
    RgbafValue,
    RgbaValue,
    Sequence,
    TimeInterval,
    UnitQuaternionValue,
    check_reference,
    format_datetime_like,
)


class HasAlignment(BaseModel):
    """A property that can be horizontally or vertically aligned."""

    horizontalOrigin: None | HorizontalOrigins | Sequence = Field(default=None)
    verticalOrigin: None | VerticalOrigins | Sequence = Field(default=None)


class Material(BaseCZMLObject):
    """A definition of how a surface is colored or shaded."""

    solidColor: None | SolidColorMaterial | str | Sequence = Field(
        default=None
    )
    image: None | ImageMaterial | str | Uri | Sequence = Field(default=None)
    grid: None | GridMaterial | Sequence = Field(default=None)
    stripe: None | StripeMaterial | Sequence = Field(default=None)
    checkerboard: None | CheckerboardMaterial | Sequence = Field(default=None)
    polylineOutline: None | PolylineMaterial | PolylineOutline | Sequence = Field(
        default=None
    )  # NOTE: Not present in documentation


class PolylineOutline(BaseCZMLObject):
    """A definition of how a surface is colored or shaded."""

    color: None | Color | str | Sequence = Field(default=None)
    outlineColor: None | Color | str | Sequence = Field(default=None)
    outlineWidth: None | float | Sequence = Field(default=None)


class PolylineOutlineMaterial(BaseCZMLObject):
    """A definition of the material wrapper for a polyline outline."""

    polylineOutline: None | PolylineOutline | Sequence = Field(default=None)


class PolylineGlow(BaseCZMLObject):
    """A definition of how a glowing polyline appears."""

    color: None | Color | str | Sequence = Field(default=None)
    glowPower: None | float | Sequence = Field(default=None)
    taperPower: None | float | Sequence = Field(default=None)


class PolylineGlowMaterial(BaseCZMLObject):
    """A material that fills the surface of a line with a glowing color."""

    polylineGlow: None | PolylineGlow | Sequence = Field(default=None)


class PolylineArrow(BaseCZMLObject):
    """A definition of how a polyline arrow appears."""

    color: None | Color | str | Sequence = Field(default=None)


class PolylineArrowMaterial(BaseCZMLObject):
    """A material that fills the surface of a line with an arrow."""

    polylineArrow: None | PolylineArrow | Sequence = Field(default=None)


class PolylineDash(BaseCZMLObject):
    """A definition of how a polyline should be dashed with two colors."""

    color: None | Color | str | Sequence = Field(default=None)
    gapColor: None | Color | str | Sequence = Field(default=None)
    dashLength: None | float | Sequence = Field(default=None)
    dashPattern: None | int | Sequence = Field(default=None)


class PolylineDashMaterial(BaseCZMLObject):
    """A material that provides a how a polyline should be dashed."""

    polylineDash: None | PolylineDash | Sequence = Field(default=None)


class PolylineMaterial(BaseCZMLObject):
    """A definition of how a surface is colored or shaded."""

    solidColor: None | SolidColorMaterial | str | Sequence = Field(default=None)
    image: None | ImageMaterial | str | Uri | Sequence = Field(default=None)
    grid: None | GridMaterial | Sequence = Field(default=None)
    stripe: None | StripeMaterial | Sequence = Field(default=None)
    checkerboard: None | CheckerboardMaterial | Sequence = Field(default=None)
    polylineDash: None | PolylineDashMaterial | Sequence = Field(default=None)


class SolidColorMaterial(BaseCZMLObject):
    """A material that fills the surface with a solid color."""

    color: None | Color | str | Sequence = Field(default=None)


class GridMaterial(BaseCZMLObject):
    """A material that fills the surface with a two-dimensional grid."""

    color: None | Color | str | Sequence = Field(default=None)
    cellAlpha: None | float | Sequence = Field(default=None)
    lineCount: None | list[int] | Sequence = Field(default=None)
    lineThickness: None | list[float] | Sequence = Field(default=None)
    lineOffset: None | list[float] | Sequence = Field(default=None)


class StripeMaterial(BaseCZMLObject):
    """A material that fills the surface with alternating colors."""

    orientation: None | int | Sequence = Field(default=None)
    evenColor: None | Color | str | Sequence = Field(default=None)
    oddColor: None | Color | str | Sequence = Field(default=None)
    offset: None | float | Sequence = Field(default=None)
    repeat: None | float | Sequence = Field(default=None)


class CheckerboardMaterial(BaseCZMLObject):
    """A material that fills the surface with alternating colors."""

    evenColor: None | Color | str | Sequence = Field(default=None)
    oddColor: None | Color | str | Sequence = Field(default=None)
    repeat: None | int | Sequence = Field(default=None)


class ImageMaterial(BaseCZMLObject):
    """A material that fills the surface with an image."""

    image: None | ImageMaterial | str | Uri | Sequence = Field(default=None)
    repeat: None | list[int] | Sequence = Field(default=None)
    color: None | Color | str | Sequence = Field(default=None)
    transparent: None | bool | Sequence = Field(default=None)


class Color(BaseCZMLObject, Interpolatable, Deletable):
    """A color. The color can optionally vary over time."""

    rgba: None | RgbaValue | str | list[float] | Sequence = Field(default=None)
    rgbaf: None | RgbafValue | str | list[float] | Sequence = Field(default=None)

    @field_validator("rgba")
    @classmethod
    def validate_rgba(cls, c):
        if isinstance(c, list):
            return RgbaValue(values=c)
        return c

    @field_validator("rgbaf")
    @classmethod
    def validate_rgbaf(cls, c):
        if isinstance(c, list):
            return RgbafValue(values=c)
        return c


class Position(BaseCZMLObject, Interpolatable, Deletable):
    """Defines a position. The position can optionally vary over time."""

    referenceFrame: None | str | Sequence = Field(default=None)
    cartesian: None | Cartesian3Value | list[float] | Sequence = Field(default=None)
    cartographicRadians: None | CartographicRadiansValue | list[float] | Sequence = (
        Field(default=None)
    )
    cartographicDegrees: None | CartographicDegreesValue | list[float] | Sequence = (
        Field(default=None)
    )
    cartesianVelocity: None | Cartesian3VelocityValue | list[float] | Sequence = Field(
        default=None
    )
    reference: None | str | Sequence = Field(default=None)
    interval: None | TimeInterval | Sequence = Field(default=None)
    epoch: None | str | dt.datetime | Sequence = Field(default=None)

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
    def validate_reference(cls, r):
        check_reference(r)
        return r

    @field_validator("cartesian")
    @classmethod
    def validate_cartesian(cls, r):
        if isinstance(r, list):
            return Cartesian3Value(values=r)
        return r

    @field_validator("cartographicRadians")
    @classmethod
    def validate_cartographicRadians(cls, r):
        if isinstance(r, list):
            return CartographicRadiansValue(values=r)
        return r

    @field_validator("cartographicDegrees")
    @classmethod
    def validate_cartographicDegrees(cls, r):
        if isinstance(r, list):
            return CartographicDegreesValue(values=r)
        return r

    @field_validator("cartesianVelocity")
    @classmethod
    def validate_cartesianVelocity(cls, r):
        if isinstance(r, list):
            return Cartesian3VelocityValue(values=r)
        return r

    @field_validator("epoch")
    @classmethod
    def validate_epoch(cls, e):
        return format_datetime_like(e)


class ViewFrom(BaseCZMLObject, Interpolatable, Deletable):
    """suggested initial camera position offset when tracking this object.

    ViewFrom can optionally vary over time."""

    cartesian: None | Cartesian3Value | list[float] | Sequence
    reference: None | str | Sequence = Field(default=None)

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

    image: str | Uri | Sequence
    show: None | bool | Sequence = Field(default=None)
    scale: None | float | Sequence = Field(default=None)
    pixelOffset: None | list[float] | Sequence = Field(default=None)
    eyeOffset: None | list[float] | Sequence = Field(default=None)
    color: None | Color | str | Sequence = Field(default=None)


class EllipsoidRadii(BaseCZMLObject, Interpolatable, Deletable):
    """The radii of an ellipsoid."""

    cartesian: Cartesian3Value | list[float] | Sequence
    reference: None | str | Sequence = Field(default=None)

    @field_validator("reference")
    @classmethod
    def check(cls, r):
        check_reference(r)
        return r


class Corridor(BaseCZMLObject):
    """A corridor , which is a shape defined by a centerline and width that conforms to the
    curvature of the body shape. It can can optionally be extruded into a volume."""

    positions: PositionList | list[float] | Sequence
    show: None | bool | Sequence = Field(default=None)
    width: float
    height: None | float | Sequence = Field(default=None)
    heightReference: None | HeightReference | Sequence = Field(default=None)
    extrudedHeight: None | float | Sequence = Field(default=None)
    extrudedHeightReference: None | HeightReference | Sequence = Field(default=None)
    cornerType: None | CornerType | Sequence = Field(default=None)
    granularity: None | float | Sequence = Field(default=None)
    fill: None | bool | Sequence = Field(default=None)
    material: None | Material | str | Sequence = Field(default=None)
    outline: None | Color | str | Sequence = Field(default=None)
    outlineColor: None | Color | str | Sequence = Field(default=None)
    outlineWidth: None | float | Sequence = Field(default=None)
    shadows: None | ShadowMode | Sequence = Field(default=None)
    distanceDisplayCondition: None | DistanceDisplayCondition | Sequence = Field(
        default=None
    )
    classificationType: None | ClassificationType | Sequence = Field(default=None)
    zIndex: None | int | Sequence = Field(default=None)


class Cylinder(BaseCZMLObject):
    """A cylinder, which is a special cone defined by length, top and bottom radius."""

    length: float | Sequence
    show: None | bool | Sequence = Field(default=None)
    topRadius: float | Sequence
    bottomRadius: float | Sequence
    heightReference: None | HeightReference | Sequence = Field(default=None)
    fill: None | bool | Sequence = Field(default=None)
    material: None | Material | str | Sequence = Field(default=None)
    outline: None | bool | Sequence = Field(default=None)
    outlineColor: None | Color | str | Sequence = Field(default=None)
    outlineWidth: None | float | Sequence = Field(default=None)
    numberOfVerticalLines: None | int | Sequence = Field(default=None)
    slices: None | int | Sequence = Field(default=None)
    shadows: None | ShadowMode | Sequence = Field(default=None)
    distanceDisplayCondition: None | DistanceDisplayCondition | Sequence = Field(
        default=None
    )


class Ellipse(BaseCZMLObject):
    """An ellipse, which is a close curve, on or above Earth's surface."""

    semiMajorAxis: float | Sequence
    semiMinorAxis: float | Sequence
    show: None | bool | Sequence = Field(default=None)
    height: None | float | Sequence = Field(default=None)
    heightReference: None | HeightReference | Sequence = Field(default=None)
    extrudedHeight: None | float | Sequence = Field(default=None)
    extrudedHeightReference: None | HeightReference | Sequence = Field(default=None)
    rotation: None | float | Sequence = Field(default=None)
    stRotation: None | float | Sequence = Field(default=None)
    granularity: None | float | Sequence = Field(default=None)
    fill: None | bool | Sequence = Field(default=None)
    material: None | Material | str | Sequence = Field(default=None)
    outline: None | bool | Sequence = Field(default=None)
    outlineColor: None | Color | str | Sequence = Field(default=None)
    outlineWidth: None | float | Sequence = Field(default=None)
    numberOfVerticalLines: None | int | Sequence = Field(default=None)
    shadows: None | ShadowMode | Sequence = Field(default=None)
    distanceDisplayCondition: None | DistanceDisplayCondition | Sequence = Field(
        default=None
    )
    classificationType: None | ClassificationType | Sequence = Field(default=None)
    zIndex: None | int | Sequence = Field(default=None)


class Polygon(BaseCZMLObject):
    """A polygon, which is a closed figure on the surface of the Earth."""

    positions: Position | PositionList | list[float] | Sequence
    show: None | bool | Sequence = Field(default=None)
    arcType: None | ArcType | Sequence = Field(default=None)
    granularity: None | float | Sequence = Field(default=None)
    material: None | Material | str | Sequence = Field(default=None)
    shadows: None | ShadowMode | Sequence = Field(default=None)
    distanceDisplayCondition: None | DistanceDisplayCondition | Sequence = Field(
        default=None
    )
    classificationType: None | ClassificationType | Sequence = Field(default=None)
    zIndex: None | int | Sequence = Field(default=None)
    holes: None | PositionList | PositionListOfLists | list[float] | Sequence = Field(
        default=None
    )  # NOTE: not in documentation
    outlineColor: None | Color | str | Sequence = Field(default=None)
    outline: None | bool | Sequence = Field(default=None)
    extrudedHeight: None | float | Sequence = Field(default=None)
    perPositionHeight: None | bool | Sequence = Field(default=None)


class Polyline(BaseCZMLObject):
    """A polyline, which is a line in the scene composed of multiple segments."""

    positions: PositionList | Sequence
    show: None | bool | Sequence = Field(default=None)
    arcType: None | ArcType | Sequence = Field(default=None)
    width: None | float | Sequence = Field(default=None)
    granularity: None | float | Sequence = Field(default=None)
    material: (
        None
        | PolylineMaterial
        | PolylineDashMaterial
        | PolylineArrowMaterial
        | PolylineGlowMaterial
        | PolylineOutlineMaterial
        | str
    ) | Sequence = Field(default=None)
    followSurface: None | bool | Sequence = Field(default=None)
    shadows: None | ShadowMode | Sequence = Field(default=None)
    depthFailMaterial: (
        None
        | PolylineMaterial
        | PolylineDashMaterial
        | PolylineArrowMaterial
        | PolylineGlowMaterial
        | PolylineOutlineMaterial
        | str
    ) | Sequence = Field(default=None)
    distanceDisplayCondition: None | DistanceDisplayCondition | Sequence = Field(
        default=None
    )
    clampToGround: None | bool | Sequence = Field(default=None)
    classificationType: None | ClassificationType | Sequence = Field(default=None)
    zIndex: None | int | Sequence = Field(default=None)


class ArcType(BaseCZMLObject, Deletable):
    """The type of an arc."""

    arcType: None | ArcTypes | str | Sequence = Field(default=None)
    reference: None | str | Sequence = Field(default=None)

    @field_validator("reference")
    @classmethod
    def check(cls, r):
        check_reference(r)
        return r


class ShadowMode(BaseCZMLObject, Deletable):
    """Whether or not an object casts or receives shadows from each light source when shadows are enabled."""

    shadowMode: None | ShadowModes | Sequence = Field(default=None)
    reference: None | str | Sequence = Field(default=None)

    @field_validator("reference")
    @classmethod
    def check(cls, r):
        check_reference(r)
        return r


class ClassificationType(BaseCZMLObject, Deletable):
    """Whether a classification affects terrain, 3D Tiles, or both."""

    classificationType: None | ClassificationTypes | Sequence = Field(default=None)
    reference: None | str | Sequence = Field(default=None)

    @field_validator("reference")
    @classmethod
    def check(cls, r):
        check_reference(r)
        return r


class DistanceDisplayCondition(BaseCZMLObject, Interpolatable, Deletable):
    """Indicates the visibility of an object based on the distance to the camera."""

    distanceDisplayCondition: None | DistanceDisplayConditionValue | Sequence = Field(
        default=None
    )
    reference: None | str | Sequence = Field(default=None)

    @field_validator("reference")
    @classmethod
    def check(cls, r):
        check_reference(r)
        return r


class PositionListOfLists(BaseCZMLObject, Deletable):
    """A list of positions."""

    referenceFrame: None | str | list[str] | Sequence = Field(default=None)
    cartesian: None | Cartesian3Value | Sequence = Field(default=None)
    cartographicRadians: None | list[float] | list[list[float]] | Sequence = Field(
        default=None
    )
    cartographicDegrees: None | list[float] | list[list[float]] | Sequence = Field(
        default=None
    )
    references: None | str | list[str] | Sequence = Field(default=None)


class PositionList(BaseCZMLObject, Interpolatable, Deletable):
    """A list of positions."""

    referenceFrame: None | str | list[str] | Sequence = Field(default=None)
    cartesian: None | Cartesian3ListValue | list[float] | Sequence = Field(default=None)
    cartographicRadians: (
        None | list[float] | CartographicRadiansListValue | Sequence
    ) = Field(default=None)
    cartographicDegrees: (
        None | list[float] | CartographicDegreesListValue | Sequence
    ) = Field(default=None)
    references: None | str | list[str] | Sequence = Field(default=None)
    interval: None | TimeInterval | Sequence = Field(default=None)
    epoch: None | str | dt.datetime | Sequence = Field(
        default=None
    )  # note: not documented

    @field_validator("cartesian")
    @classmethod
    def validate_cartesian(cls, r):
        if isinstance(r, list):
            return Cartesian3Value(values=r)
        return r

    @field_validator("cartographicRadians")
    @classmethod
    def validate_cartographicRadians(cls, r):
        if isinstance(r, list):
            return CartographicRadiansListValue(values=r)
        return r

    @field_validator("cartographicDegrees")
    @classmethod
    def validate_cartographicDegrees(cls, r):
        if isinstance(r, list):
            return CartographicDegreesListValue(values=r)
        return r

    @field_validator("epoch")
    @classmethod
    def check(cls, e):
        return format_datetime_like(e)


class Ellipsoid(BaseCZMLObject):
    """A closed quadric surface that is a three-dimensional analogue of an ellipse."""

    radii: EllipsoidRadii | Sequence
    innerRadii: None | EllipsoidRadii | Sequence = Field(default=None)
    minimumClock: None | float | Sequence = Field(default=None)
    maximumClock: None | float | Sequence = Field(default=None)
    minimumCone: None | float | Sequence = Field(default=None)
    maximumCone: None | float | Sequence = Field(default=None)
    show: None | bool | Sequence = Field(default=None)
    heightReference: None | HeightReference | Sequence = Field(default=None)
    fill: None | bool | Sequence = Field(default=None)
    material: None | Material | str | Sequence = Field(default=None)
    outline: None | bool | Sequence = Field(default=None)
    outlineColor: None | Color | str | Sequence = Field(default=None)
    outlineWidth: None | float | Sequence = Field(default=None)
    stackPartitions: None | int | Sequence = Field(default=None)
    slicePartitions: None | int | Sequence = Field(default=None)
    subdivisions: None | int | Sequence = Field(default=None)


class Box(BaseCZMLObject):
    """A box, which is a closed rectangular cuboid."""

    show: None | bool | Sequence = Field(default=None)
    dimensions: None | BoxDimensions | Sequence = Field(default=None)
    heightReference: None | HeightReference | Sequence = Field(default=None)
    fill: None | bool | Sequence = Field(default=None)
    material: None | Material | str | Sequence = Field(default=None)
    outline: None | bool | Sequence = Field(default=None)
    outlineColor: None | Color | str | Sequence = Field(default=None)
    outlineWidth: None | float | Sequence = Field(default=None)
    shadows: None | ShadowMode | Sequence = Field(default=None)
    distanceDisplayCondition: None | DistanceDisplayCondition | Sequence = Field(
        default=None
    )


class BoxDimensions(BaseCZMLObject, Interpolatable):
    """The width, depth, and height of a box."""

    cartesian: None | Cartesian3Value | Sequence = Field(default=None)
    reference: None | str | Sequence = Field(default=None)

    @field_validator("reference")
    @classmethod
    def check(cls, r):
        check_reference(r)
        return r


class Rectangle(BaseCZMLObject, Interpolatable, Deletable):
    """A cartographic rectangle, which conforms to the curvature of the globe and
    can be placed on the surface or at altitude and can optionally be extruded into a volume.
    """

    coordinates: None | RectangleCoordinates | Sequence = Field(default=None)
    fill: None | bool | Sequence = Field(default=None)
    material: None | Material | str | Sequence = Field(default=None)


class RectangleCoordinates(BaseCZMLObject, Interpolatable, Deletable):
    """A set of coordinates describing a cartographic rectangle on the surface of the ellipsoid."""

    wsen: None | list[float] | Sequence = Field(default=None)
    wsenDegrees: None | list[float] | Sequence = Field(default=None)
    reference: None | str | Sequence = Field(default=None)

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

    cartesian: None | Cartesian3Value | list[float] | Sequence = Field(default=None)
    reference: None | str | Sequence = Field(default=None)

    @field_validator("reference")
    @classmethod
    def check(cls, r):
        check_reference(r)
        return r


class HeightReference(BaseCZMLObject, Deletable):
    """The height reference of an object, which indicates if the object's position is relative to terrain or not."""

    heightReference: None | HeightReferences | Sequence = Field(default=None)
    reference: None | str | Sequence = Field(default=None)

    @field_validator("reference")
    @classmethod
    def check(cls, r):
        check_reference(r)
        return r


class ColorBlendMode(BaseCZMLObject, Deletable):
    """The height reference of an object, which indicates if the object's position is relative to terrain or not."""

    colorBlendMode: None | ColorBlendModes | Sequence = Field(default=None)
    reference: None | str | Sequence = Field(default=None)

    @field_validator("reference")
    @classmethod
    def check(cls, r):
        check_reference(r)
        return r


class CornerType(BaseCZMLObject, Deletable):
    """The height reference of an object, which indicates if the object's position is relative to terrain or not."""

    cornerType: None | CornerTypes | Sequence = Field(default=None)
    reference: None | str | Sequence = Field(default=None)

    @field_validator("reference")
    @classmethod
    def check(cls, r):
        check_reference(r)
        return r


class Clock(BaseCZMLObject):
    """Initial settings for a simulated clock when a document is loaded.

    The start and stop time are configured using the interval property.

    """

    currentTime: None | str | dt.datetime | Sequence = Field(default=None)
    multiplier: None | float | Sequence = Field(default=None)
    range: None | ClockRanges | Sequence = Field(default=None)
    step: None | ClockSteps | Sequence = Field(default=None)

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
    leadTime: None | float | Sequence = Field(default=None)
    trailTime: None | float | Sequence = Field(default=None)
    width: None | float | Sequence = Field(default=None)
    resolution: None | float | Sequence = Field(default=None)
    material: None | Material | str | Sequence = Field(default=None)
    distanceDisplayCondition: None | DistanceDisplayCondition | Sequence = Field(
        default=None
    )


class Point(BaseCZMLObject):
    """A point, or viewport-aligned circle."""

    show: None | bool | Sequence = Field(default=None)
    pixelSize: None | float | Sequence = Field(default=None)
    heightReference: None | HeightReference | Sequence = Field(default=None)
    color: None | Color | str | Sequence = Field(default=None)
    outlineColor: None | Color | str | Sequence = Field(default=None)
    outlineWidth: None | float | Sequence = Field(default=None)
    scaleByDistance: None | NearFarScalar | Sequence = Field(default=None)
    translucencyByDistance: None | NearFarScalar | Sequence = Field(default=None)
    distanceDisplayCondition: None | DistanceDisplayCondition | Sequence = Field(
        default=None
    )
    disableDepthTestDistance: None | float | Sequence = Field(default=None)


class Tileset(BaseCZMLObject):
    """A 3D Tiles tileset."""

    uri: str | Uri | Sequence
    show: None | bool | Sequence = Field(default=None)
    maximumScreenSpaceError: None | float | Sequence = Field(default=None)


class Wall(BaseCZMLObject):
    """A two-dimensional wall defined as a line strip and optional maximum and minimum heights.
    It conforms to the curvature of the globe and can be placed along the surface or at altitude.
    """

    show: None | bool | Sequence = Field(default=None)
    positions: PositionList | Sequence
    minimumHeights: None | list[float] | Sequence = Field(default=None)
    maximumHeights: None | list[float] | Sequence = Field(default=None)
    granularity: None | float | Sequence = Field(default=None)
    fill: None | bool | Sequence = Field(default=None)
    material: None | Material | str | Sequence = Field(default=None)
    outline: None | bool | Sequence = Field(default=None)
    outlineColor: None | Color | str | Sequence = Field(default=None)
    outlineWidth: None | float | Sequence = Field(default=None)
    shadows: None | ShadowMode | Sequence = Field(default=None)
    distanceDisplayCondition: None | DistanceDisplayCondition | Sequence = Field(
        default=None
    )


class NearFarScalar(BaseCZMLObject, Interpolatable, Deletable):
    """A numeric value which will be linearly interpolated between two values based on an object's distance from the
     camera, in eye coordinates.

    The computed value will interpolate between the near value and the far value while the camera distance falls
    between the near distance and the far distance, and will be clamped to the near or far value while the distance is
    less than the near distance or greater than the far distance, respectively.
    """

    nearFarScalar: None | list[float] | NearFarScalarValue | Sequence = Field(
        default=None
    )
    reference: None | str | Sequence = Field(default=None)

    @field_validator("reference")
    @classmethod
    def check(cls, r):
        check_reference(r)
        return r


class Label(BaseCZMLObject, HasAlignment):
    """A string of text."""

    show: None | bool | Sequence = Field(default=None)
    text: None | str | Sequence = Field(default=None)
    font: None | str | Sequence = Field(default=None)
    style: None | LabelStyles | Sequence = Field(default=None)
    scale: None | float | Sequence = Field(default=None)
    showBackground: None | bool | Sequence = Field(default=None)
    backgroundColor: None | Color | str | Sequence = Field(default=None)
    fillColor: None | Color | str | Sequence = Field(default=None)
    outlineColor: None | Color | str | Sequence = Field(default=None)
    outlineWidth: None | float | Sequence = Field(default=None)
    pixelOffset: None | float | Cartesian2Value | Sequence = Field(default=None)


class Orientation(BaseCZMLObject, Interpolatable, Deletable):
    """Defines an orientation.

    An orientation is a rotation that takes a vector expressed in the "body" axes of the object
    and transforms it to the Earth fixed axes.

    """

    unitQuaternion: None | list[float] | UnitQuaternionValue | Sequence = Field(
        default=None
    )
    reference: None | str | Sequence = Field(default=None)
    velocityReference: None | str | Sequence = Field(default=None)

    @field_validator("reference")
    @classmethod
    def check(cls, r):
        check_reference(r)
        return r


class Model(BaseCZMLObject):
    """A 3D model."""

    show: None | bool | Sequence = Field(default=None)
    gltf: str | Sequence
    scale: None | float | Sequence = Field(default=None)
    minimumPixelSize: None | float | Sequence = Field(default=None)
    maximumScale: None | float | Sequence = Field(default=None)
    incrementallyLoadTextures: None | bool | Sequence = Field(default=None)
    runAnimations: None | bool | Sequence = Field(default=None)
    shadows: None | ShadowMode | Sequence = Field(default=None)
    heightReference: None | HeightReference | Sequence = Field(default=None)
    silhouetteColor: None | Color | str | Sequence = Field(default=None)
    silhouetteSize: None | Color | str | Sequence = Field(default=None)
    color: None | Color | str | Sequence = Field(default=None)
    colorBlendMode: None | ColorBlendMode | Sequence = Field(default=None)
    colorBlendAmount: None | float | Sequence = Field(default=None)
    distanceDisplayCondition: None | DistanceDisplayCondition | Sequence = Field(
        default=None
    )
    nodeTransformations: None | Any | Sequence = Field(default=None)
    articulations: None | Any | Sequence = Field(default=None)


class Uri(BaseCZMLObject, Deletable):
    """A URI value.

    The URI can optionally vary with time.
    """

    uri: None | str | Sequence = Field(default=None)

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
    def custom_serializer(self) -> None | str | Sequence:
        return self.uri
