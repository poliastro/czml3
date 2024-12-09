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
    Cartesian3ListOfListsValue,
    Cartesian3ListValue,
    Cartesian3Value,
    Cartesian3VelocityValue,
    CartographicDegreesListOfListsValue,
    CartographicDegreesListValue,
    CartographicDegreesValue,
    CartographicRadiansListOfListsValue,
    CartographicRadiansListValue,
    CartographicRadiansValue,
    DistanceDisplayConditionValue,
    NearFarScalarValue,
    ReferenceListOfListsValue,
    ReferenceListValue,
    RgbafValue,
    RgbaValue,
    TimeInterval,
    TimeIntervalCollection,
    UnitQuaternionValue,
    check_reference,
    format_datetime_like,
)


class HasAlignment(BaseModel):
    """A property that can be horizontally or vertically aligned."""

    horizontalOrigin: None | HorizontalOrigins | TimeIntervalCollection = Field(
        default=None
    )
    verticalOrigin: None | VerticalOrigins | TimeIntervalCollection = Field(
        default=None
    )


class Material(BaseCZMLObject):
    """A definition of how a surface is colored or shaded."""

    solidColor: None | SolidColorMaterial | str | TimeIntervalCollection = Field(
        default=None
    )
    image: None | ImageMaterial | str | Uri | TimeIntervalCollection = Field(
        default=None
    )
    grid: None | GridMaterial | TimeIntervalCollection = Field(default=None)
    stripe: None | StripeMaterial | TimeIntervalCollection = Field(default=None)
    checkerboard: None | CheckerboardMaterial | TimeIntervalCollection = Field(
        default=None
    )
    polylineOutline: (
        None | PolylineMaterial | PolylineOutline | TimeIntervalCollection
    ) = Field(default=None)  # NOTE: Not present in documentation


class PolylineOutline(BaseCZMLObject):
    """A definition of how a surface is colored or shaded."""

    color: None | Color | str | TimeIntervalCollection = Field(default=None)
    outlineColor: None | Color | str | TimeIntervalCollection = Field(default=None)
    outlineWidth: None | float | TimeIntervalCollection = Field(default=None)


class PolylineOutlineMaterial(BaseCZMLObject):
    """A definition of the material wrapper for a polyline outline."""

    polylineOutline: None | PolylineOutline | TimeIntervalCollection = Field(
        default=None
    )


class PolylineGlow(BaseCZMLObject):
    """A definition of how a glowing polyline appears."""

    color: None | Color | str | TimeIntervalCollection = Field(default=None)
    glowPower: None | float | TimeIntervalCollection = Field(default=None)
    taperPower: None | float | TimeIntervalCollection = Field(default=None)


class PolylineGlowMaterial(BaseCZMLObject):
    """A material that fills the surface of a line with a glowing color."""

    polylineGlow: None | PolylineGlow | TimeIntervalCollection = Field(default=None)


class PolylineArrow(BaseCZMLObject):
    """A definition of how a polyline arrow appears."""

    color: None | Color | str | TimeIntervalCollection = Field(default=None)


class PolylineArrowMaterial(BaseCZMLObject):
    """A material that fills the surface of a line with an arrow."""

    polylineArrow: None | PolylineArrow | TimeIntervalCollection = Field(default=None)


class PolylineDash(BaseCZMLObject):
    """A definition of how a polyline should be dashed with two colors."""

    color: None | Color | str | TimeIntervalCollection = Field(default=None)
    gapColor: None | Color | str | TimeIntervalCollection = Field(default=None)
    dashLength: None | float | TimeIntervalCollection = Field(default=None)
    dashPattern: None | int | TimeIntervalCollection = Field(default=None)


class PolylineDashMaterial(BaseCZMLObject):
    """A material that provides a how a polyline should be dashed."""

    polylineDash: None | PolylineDash | TimeIntervalCollection = Field(default=None)


class PolylineMaterial(BaseCZMLObject):
    """A definition of how a surface is colored or shaded."""

    solidColor: None | SolidColorMaterial | str | TimeIntervalCollection = Field(
        default=None
    )
    image: None | ImageMaterial | str | Uri | TimeIntervalCollection = Field(
        default=None
    )
    grid: None | GridMaterial | TimeIntervalCollection = Field(default=None)
    stripe: None | StripeMaterial | TimeIntervalCollection = Field(default=None)
    checkerboard: None | CheckerboardMaterial | TimeIntervalCollection = Field(
        default=None
    )
    polylineDash: None | PolylineDashMaterial | TimeIntervalCollection = Field(
        default=None
    )


class SolidColorMaterial(BaseCZMLObject):
    """A material that fills the surface with a solid color."""

    color: None | Color | str | TimeIntervalCollection = Field(default=None)


class GridMaterial(BaseCZMLObject):
    """A material that fills the surface with a two-dimensional grid."""

    color: None | Color | str | TimeIntervalCollection = Field(default=None)
    cellAlpha: None | float | TimeIntervalCollection = Field(default=None)
    lineCount: None | list[int] | TimeIntervalCollection = Field(default=None)
    lineThickness: None | list[float] | TimeIntervalCollection = Field(default=None)
    lineOffset: None | list[float] | TimeIntervalCollection = Field(default=None)


class StripeMaterial(BaseCZMLObject):
    """A material that fills the surface with alternating colors."""

    orientation: None | int | TimeIntervalCollection = Field(default=None)
    evenColor: None | Color | str | TimeIntervalCollection = Field(default=None)
    oddColor: None | Color | str | TimeIntervalCollection = Field(default=None)
    offset: None | float | TimeIntervalCollection = Field(default=None)
    repeat: None | float | TimeIntervalCollection = Field(default=None)


class CheckerboardMaterial(BaseCZMLObject):
    """A material that fills the surface with alternating colors."""

    evenColor: None | Color | str | TimeIntervalCollection = Field(default=None)
    oddColor: None | Color | str | TimeIntervalCollection = Field(default=None)
    repeat: None | int | TimeIntervalCollection = Field(default=None)


class ImageMaterial(BaseCZMLObject):
    """A material that fills the surface with an image."""

    image: None | ImageMaterial | str | Uri | TimeIntervalCollection = Field(
        default=None
    )
    repeat: None | list[int] | TimeIntervalCollection = Field(default=None)
    color: None | Color | str | TimeIntervalCollection = Field(default=None)
    transparent: None | bool | TimeIntervalCollection = Field(default=None)


class Color(BaseCZMLObject, Interpolatable, Deletable):
    """A color. The color can optionally vary over time."""

    rgba: None | RgbaValue | str | list[float] | TimeIntervalCollection = Field(
        default=None
    )
    rgbaf: None | RgbafValue | str | list[float] | TimeIntervalCollection = Field(
        default=None
    )

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

    referenceFrame: None | str | TimeIntervalCollection = Field(default=None)
    cartesian: None | Cartesian3Value | list[float] | TimeIntervalCollection = Field(
        default=None
    )
    cartographicRadians: (
        None | CartographicRadiansValue | list[float] | TimeIntervalCollection
    ) = Field(default=None)
    cartographicDegrees: (
        None | CartographicDegreesValue | list[float] | TimeIntervalCollection
    ) = Field(default=None)
    cartesianVelocity: (
        None | Cartesian3VelocityValue | list[float] | TimeIntervalCollection
    ) = Field(default=None)
    reference: None | str | TimeIntervalCollection = Field(default=None)
    interval: None | TimeInterval | TimeIntervalCollection = Field(default=None)
    epoch: None | str | dt.datetime | TimeIntervalCollection = Field(default=None)

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

    cartesian: None | Cartesian3Value | list[float] | TimeIntervalCollection
    reference: None | str | TimeIntervalCollection = Field(default=None)

    @field_validator("cartesian")
    @classmethod
    def validate_cartesian(cls, r):
        if isinstance(r, list):
            return Cartesian3Value(values=r)
        return r

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

    image: str | Uri | TimeIntervalCollection
    show: None | bool | TimeIntervalCollection = Field(default=None)
    scale: None | float | TimeIntervalCollection = Field(default=None)
    pixelOffset: None | list[float] | TimeIntervalCollection = Field(default=None)
    eyeOffset: None | list[float] | TimeIntervalCollection = Field(default=None)
    color: None | Color | str | TimeIntervalCollection = Field(default=None)


class EllipsoidRadii(BaseCZMLObject, Interpolatable, Deletable):
    """The radii of an ellipsoid."""

    cartesian: Cartesian3Value | list[float] | TimeIntervalCollection
    reference: None | str | TimeIntervalCollection = Field(default=None)

    @field_validator("cartesian")
    @classmethod
    def validate_cartesian(cls, r):
        if isinstance(r, list):
            return Cartesian3Value(values=r)
        return r

    @field_validator("reference")
    @classmethod
    def check(cls, r):
        check_reference(r)
        return r


class Corridor(BaseCZMLObject):
    """A corridor , which is a shape defined by a centerline and width that conforms to the
    curvature of the body shape. It can can optionally be extruded into a volume."""

    positions: PositionList | list[float] | TimeIntervalCollection
    show: None | bool | TimeIntervalCollection = Field(default=None)
    width: float
    height: None | float | TimeIntervalCollection = Field(default=None)
    heightReference: None | HeightReference | TimeIntervalCollection = Field(
        default=None
    )
    extrudedHeight: None | float | TimeIntervalCollection = Field(default=None)
    extrudedHeightReference: None | HeightReference | TimeIntervalCollection = Field(
        default=None
    )
    cornerType: None | CornerType | TimeIntervalCollection = Field(default=None)
    granularity: None | float | TimeIntervalCollection = Field(default=None)
    fill: None | bool | TimeIntervalCollection = Field(default=None)
    material: None | Material | str | TimeIntervalCollection = Field(default=None)
    outline: None | Color | str | TimeIntervalCollection = Field(default=None)
    outlineColor: None | Color | str | TimeIntervalCollection = Field(default=None)
    outlineWidth: None | float | TimeIntervalCollection = Field(default=None)
    shadows: None | ShadowMode | TimeIntervalCollection = Field(default=None)
    distanceDisplayCondition: (
        None | DistanceDisplayCondition | TimeIntervalCollection
    ) = Field(default=None)
    classificationType: None | ClassificationType | TimeIntervalCollection = Field(
        default=None
    )
    zIndex: None | int | TimeIntervalCollection = Field(default=None)


class Cylinder(BaseCZMLObject):
    """A cylinder, which is a special cone defined by length, top and bottom radius."""

    length: float | TimeIntervalCollection
    show: None | bool | TimeIntervalCollection = Field(default=None)
    topRadius: float | TimeIntervalCollection
    bottomRadius: float | TimeIntervalCollection
    heightReference: None | HeightReference | TimeIntervalCollection = Field(
        default=None
    )
    fill: None | bool | TimeIntervalCollection = Field(default=None)
    material: None | Material | str | TimeIntervalCollection = Field(default=None)
    outline: None | bool | TimeIntervalCollection = Field(default=None)
    outlineColor: None | Color | str | TimeIntervalCollection = Field(default=None)
    outlineWidth: None | float | TimeIntervalCollection = Field(default=None)
    numberOfVerticalLines: None | int | TimeIntervalCollection = Field(default=None)
    slices: None | int | TimeIntervalCollection = Field(default=None)
    shadows: None | ShadowMode | TimeIntervalCollection = Field(default=None)
    distanceDisplayCondition: (
        None | DistanceDisplayCondition | TimeIntervalCollection
    ) = Field(default=None)


class Ellipse(BaseCZMLObject):
    """An ellipse, which is a close curve, on or above Earth's surface."""

    semiMajorAxis: float | TimeIntervalCollection
    semiMinorAxis: float | TimeIntervalCollection
    show: None | bool | TimeIntervalCollection = Field(default=None)
    height: None | float | TimeIntervalCollection = Field(default=None)
    heightReference: None | HeightReference | TimeIntervalCollection = Field(
        default=None
    )
    extrudedHeight: None | float | TimeIntervalCollection = Field(default=None)
    extrudedHeightReference: None | HeightReference | TimeIntervalCollection = Field(
        default=None
    )
    rotation: None | float | TimeIntervalCollection = Field(default=None)
    stRotation: None | float | TimeIntervalCollection = Field(default=None)
    granularity: None | float | TimeIntervalCollection = Field(default=None)
    fill: None | bool | TimeIntervalCollection = Field(default=None)
    material: None | Material | str | TimeIntervalCollection = Field(default=None)
    outline: None | bool | TimeIntervalCollection = Field(default=None)
    outlineColor: None | Color | str | TimeIntervalCollection = Field(default=None)
    outlineWidth: None | float | TimeIntervalCollection = Field(default=None)
    numberOfVerticalLines: None | int | TimeIntervalCollection = Field(default=None)
    shadows: None | ShadowMode | TimeIntervalCollection = Field(default=None)
    distanceDisplayCondition: (
        None | DistanceDisplayCondition | TimeIntervalCollection
    ) = Field(default=None)
    classificationType: None | ClassificationType | TimeIntervalCollection = Field(
        default=None
    )
    zIndex: None | int | TimeIntervalCollection = Field(default=None)


class Polygon(BaseCZMLObject):
    """A polygon, which is a closed figure on the surface of the Earth."""

    positions: Position | PositionList | list[float] | TimeIntervalCollection
    show: None | bool | TimeIntervalCollection = Field(default=None)
    arcType: None | ArcType | TimeIntervalCollection = Field(default=None)
    granularity: None | float | TimeIntervalCollection = Field(default=None)
    material: None | Material | str | TimeIntervalCollection = Field(default=None)
    shadows: None | ShadowMode | TimeIntervalCollection = Field(default=None)
    distanceDisplayCondition: (
        None | DistanceDisplayCondition | TimeIntervalCollection
    ) = Field(default=None)
    classificationType: None | ClassificationType | TimeIntervalCollection = Field(
        default=None
    )
    zIndex: None | int | TimeIntervalCollection = Field(default=None)
    holes: (
        None | PositionList | PositionListOfLists | list[float] | TimeIntervalCollection
    ) = Field(default=None)  # NOTE: not in documentation
    outlineColor: None | Color | str | TimeIntervalCollection = Field(default=None)
    outline: None | bool | TimeIntervalCollection = Field(default=None)
    extrudedHeight: None | float | TimeIntervalCollection = Field(default=None)
    perPositionHeight: None | bool | TimeIntervalCollection = Field(default=None)


class Polyline(BaseCZMLObject):
    """A polyline, which is a line in the scene composed of multiple segments."""

    positions: PositionList | TimeIntervalCollection
    show: None | bool | TimeIntervalCollection = Field(default=None)
    arcType: None | ArcType | TimeIntervalCollection = Field(default=None)
    width: None | float | TimeIntervalCollection = Field(default=None)
    granularity: None | float | TimeIntervalCollection = Field(default=None)
    material: (
        None
        | PolylineMaterial
        | PolylineDashMaterial
        | PolylineArrowMaterial
        | PolylineGlowMaterial
        | PolylineOutlineMaterial
        | str
    ) | TimeIntervalCollection = Field(default=None)
    followSurface: None | bool | TimeIntervalCollection = Field(default=None)
    shadows: None | ShadowMode | TimeIntervalCollection = Field(default=None)
    depthFailMaterial: (
        None
        | PolylineMaterial
        | PolylineDashMaterial
        | PolylineArrowMaterial
        | PolylineGlowMaterial
        | PolylineOutlineMaterial
        | str
    ) | TimeIntervalCollection = Field(default=None)
    distanceDisplayCondition: (
        None | DistanceDisplayCondition | TimeIntervalCollection
    ) = Field(default=None)
    clampToGround: None | bool | TimeIntervalCollection = Field(default=None)
    classificationType: None | ClassificationType | TimeIntervalCollection = Field(
        default=None
    )
    zIndex: None | int | TimeIntervalCollection = Field(default=None)


class ArcType(BaseCZMLObject, Deletable):
    """The type of an arc."""

    arcType: None | ArcTypes | str | TimeIntervalCollection = Field(default=None)
    reference: None | str | TimeIntervalCollection = Field(default=None)

    @field_validator("reference")
    @classmethod
    def check(cls, r):
        check_reference(r)
        return r


class ShadowMode(BaseCZMLObject, Deletable):
    """Whether or not an object casts or receives shadows from each light source when shadows are enabled."""

    shadowMode: None | ShadowModes | TimeIntervalCollection = Field(default=None)
    reference: None | str | TimeIntervalCollection = Field(default=None)

    @field_validator("reference")
    @classmethod
    def check(cls, r):
        check_reference(r)
        return r


class ClassificationType(BaseCZMLObject, Deletable):
    """Whether a classification affects terrain, 3D Tiles, or both."""

    classificationType: None | ClassificationTypes | TimeIntervalCollection = Field(
        default=None
    )
    reference: None | str | TimeIntervalCollection = Field(default=None)

    @field_validator("reference")
    @classmethod
    def check(cls, r):
        check_reference(r)
        return r


class DistanceDisplayCondition(BaseCZMLObject, Interpolatable, Deletable):
    """Indicates the visibility of an object based on the distance to the camera."""

    distanceDisplayCondition: (
        None | DistanceDisplayConditionValue | TimeIntervalCollection
    ) = Field(default=None)
    reference: None | str | TimeIntervalCollection = Field(default=None)

    @field_validator("reference")
    @classmethod
    def check(cls, r):
        check_reference(r)
        return r


class PositionListOfLists(BaseCZMLObject, Deletable):
    """A list of positions."""

    referenceFrame: None | str | TimeIntervalCollection = Field(default=None)
    cartesian: (
        None | Cartesian3ListOfListsValue | list[list[float]] | TimeIntervalCollection
    ) = Field(default=None)
    cartographicRadians: (
        None
        | CartographicRadiansListOfListsValue
        | list[list[float]]
        | TimeIntervalCollection
    ) = Field(default=None)
    cartographicDegrees: (
        None
        | CartographicDegreesListOfListsValue
        | list[list[float]]
        | TimeIntervalCollection
    ) = Field(default=None)
    references: (
        None | ReferenceListOfListsValue | list[list[str]] | TimeIntervalCollection
    ) = Field(default=None)

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
                )
            )
            != 1
        ):
            raise TypeError(
                "One of cartesian, cartographicDegrees, cartographicRadians or reference must be given"
            )
        if isinstance(self.references, ReferenceListOfListsValue):
            if isinstance(self.cartesian, Cartesian3ListOfListsValue):
                v = self.cartesian.values
            elif isinstance(
                self.cartographicDegrees, CartographicDegreesListOfListsValue
            ):
                v = self.cartographicDegrees.values
            elif isinstance(
                self.cartographicRadians, CartographicRadiansListOfListsValue
            ):
                v = self.cartographicRadians.values
            else:
                raise TypeError
            if len(self.references.values) != len(v):
                raise TypeError("Number of references must equal number of coordinates")
            for r, v1 in zip(self.references.values, v, strict=False):
                if len(r) != len(v1) // 3:
                    raise TypeError(
                        "Number of references must equal number of coordinates in each list"
                    )

        return self

    @field_validator("references")
    @classmethod
    def validate_reference(cls, r):
        if isinstance(r, list):
            return ReferenceListOfListsValue(values=r)
        return r

    @field_validator("cartesian")
    @classmethod
    def validate_cartesian(cls, r):
        if isinstance(r, list):
            return Cartesian3ListOfListsValue(values=r)
        return r

    @field_validator("cartographicRadians")
    @classmethod
    def validate_cartographicRadians(cls, r):
        if isinstance(r, list):
            return CartographicRadiansListOfListsValue(values=r)
        return r

    @field_validator("cartographicDegrees")
    @classmethod
    def validate_cartographicDegrees(cls, r):
        if isinstance(r, list):
            return CartographicDegreesListOfListsValue(values=r)
        return r


class PositionList(BaseCZMLObject, Interpolatable, Deletable):
    """A list of positions."""

    referenceFrame: None | str | TimeIntervalCollection = Field(default=None)
    cartesian: None | Cartesian3ListValue | list[float] | TimeIntervalCollection = (
        Field(default=None)
    )
    cartographicRadians: (
        None | CartographicRadiansListValue | list[float] | TimeIntervalCollection
    ) = Field(default=None)
    cartographicDegrees: (
        None | CartographicDegreesListValue | list[float] | TimeIntervalCollection
    ) = Field(default=None)
    references: None | ReferenceListValue | list[str] | TimeIntervalCollection = Field(
        default=None
    )
    interval: None | TimeInterval | TimeIntervalCollection = Field(default=None)
    epoch: None | str | dt.datetime | TimeIntervalCollection = Field(
        default=None
    )  # note: not documented

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
                )
            )
            != 1
        ):
            raise TypeError(
                "One of cartesian, cartographicDegrees, cartographicRadians or reference must be given"
            )
        if isinstance(self.references, ReferenceListValue):
            if isinstance(self.cartesian, Cartesian3ListValue):
                v = self.cartesian.values
            elif isinstance(self.cartographicDegrees, CartographicDegreesListValue):
                v = self.cartographicDegrees.values
            elif isinstance(self.cartographicRadians, CartographicRadiansListValue):
                v = self.cartographicRadians.values
            else:
                raise TypeError
            if len(self.references.values) != len(v) // 3:
                raise TypeError("Number of references must equal number of coordinates")
        return self

    @field_validator("references")
    @classmethod
    def validate_reference(cls, r):
        if isinstance(r, list):
            return ReferenceListValue(values=r)
        return r

    @field_validator("cartesian")
    @classmethod
    def validate_cartesian(cls, r):
        if isinstance(r, list):
            return Cartesian3ListValue(values=r)
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

    radii: EllipsoidRadii | TimeIntervalCollection
    innerRadii: None | EllipsoidRadii | TimeIntervalCollection = Field(default=None)
    minimumClock: None | float | TimeIntervalCollection = Field(default=None)
    maximumClock: None | float | TimeIntervalCollection = Field(default=None)
    minimumCone: None | float | TimeIntervalCollection = Field(default=None)
    maximumCone: None | float | TimeIntervalCollection = Field(default=None)
    show: None | bool | TimeIntervalCollection = Field(default=None)
    heightReference: None | HeightReference | TimeIntervalCollection = Field(
        default=None
    )
    fill: None | bool | TimeIntervalCollection = Field(default=None)
    material: None | Material | str | TimeIntervalCollection = Field(default=None)
    outline: None | bool | TimeIntervalCollection = Field(default=None)
    outlineColor: None | Color | str | TimeIntervalCollection = Field(default=None)
    outlineWidth: None | float | TimeIntervalCollection = Field(default=None)
    stackPartitions: None | int | TimeIntervalCollection = Field(default=None)
    slicePartitions: None | int | TimeIntervalCollection = Field(default=None)
    subdivisions: None | int | TimeIntervalCollection = Field(default=None)


class Box(BaseCZMLObject):
    """A box, which is a closed rectangular cuboid."""

    show: None | bool | TimeIntervalCollection = Field(default=None)
    dimensions: None | BoxDimensions | TimeIntervalCollection = Field(default=None)
    heightReference: None | HeightReference | TimeIntervalCollection = Field(
        default=None
    )
    fill: None | bool | TimeIntervalCollection = Field(default=None)
    material: None | Material | str | TimeIntervalCollection = Field(default=None)
    outline: None | bool | TimeIntervalCollection = Field(default=None)
    outlineColor: None | Color | str | TimeIntervalCollection = Field(default=None)
    outlineWidth: None | float | TimeIntervalCollection = Field(default=None)
    shadows: None | ShadowMode | TimeIntervalCollection = Field(default=None)
    distanceDisplayCondition: (
        None | DistanceDisplayCondition | TimeIntervalCollection
    ) = Field(default=None)


class BoxDimensions(BaseCZMLObject, Interpolatable):
    """The width, depth, and height of a box."""

    cartesian: None | Cartesian3Value | list[float] | TimeIntervalCollection = Field(
        default=None
    )
    reference: None | str | TimeIntervalCollection = Field(default=None)

    @field_validator("cartesian")
    @classmethod
    def validate_cartesian(cls, r):
        if isinstance(r, list):
            return Cartesian3Value(values=r)
        return r

    @field_validator("reference")
    @classmethod
    def check(cls, r):
        check_reference(r)
        return r


class Rectangle(BaseCZMLObject, Interpolatable, Deletable):
    """A cartographic rectangle, which conforms to the curvature of the globe and
    can be placed on the surface or at altitude and can optionally be extruded into a volume.
    """

    coordinates: None | RectangleCoordinates | TimeIntervalCollection = Field(
        default=None
    )
    fill: None | bool | TimeIntervalCollection = Field(default=None)
    material: None | Material | str | TimeIntervalCollection = Field(default=None)


class RectangleCoordinates(BaseCZMLObject, Interpolatable, Deletable):
    """A set of coordinates describing a cartographic rectangle on the surface of the ellipsoid."""

    wsen: None | list[float] | TimeIntervalCollection = Field(default=None)
    wsenDegrees: None | list[float] | TimeIntervalCollection = Field(default=None)
    reference: None | str | TimeIntervalCollection = Field(default=None)

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

    cartesian: None | Cartesian3Value | list[float] | TimeIntervalCollection = Field(
        default=None
    )
    reference: None | str | TimeIntervalCollection = Field(default=None)

    @field_validator("cartesian")
    @classmethod
    def validate_cartesian(cls, r):
        if isinstance(r, list):
            return Cartesian3Value(values=r)
        return r

    @field_validator("reference")
    @classmethod
    def check(cls, r):
        check_reference(r)
        return r


class HeightReference(BaseCZMLObject, Deletable):
    """The height reference of an object, which indicates if the object's position is relative to terrain or not."""

    heightReference: None | HeightReferences | TimeIntervalCollection = Field(
        default=None
    )
    reference: None | str | TimeIntervalCollection = Field(default=None)

    @field_validator("reference")
    @classmethod
    def check(cls, r):
        check_reference(r)
        return r


class ColorBlendMode(BaseCZMLObject, Deletable):
    """The height reference of an object, which indicates if the object's position is relative to terrain or not."""

    colorBlendMode: None | ColorBlendModes | TimeIntervalCollection = Field(
        default=None
    )
    reference: None | str | TimeIntervalCollection = Field(default=None)

    @field_validator("reference")
    @classmethod
    def check(cls, r):
        check_reference(r)
        return r


class CornerType(BaseCZMLObject, Deletable):
    """The height reference of an object, which indicates if the object's position is relative to terrain or not."""

    cornerType: None | CornerTypes | TimeIntervalCollection = Field(default=None)
    reference: None | str | TimeIntervalCollection = Field(default=None)

    @field_validator("reference")
    @classmethod
    def check(cls, r):
        check_reference(r)
        return r


class Clock(BaseCZMLObject):
    """Initial settings for a simulated clock when a document is loaded.

    The start and stop time are configured using the interval property.

    """

    currentTime: None | str | dt.datetime | TimeIntervalCollection = Field(default=None)
    multiplier: None | float | TimeIntervalCollection = Field(default=None)
    range: None | ClockRanges | TimeIntervalCollection = Field(default=None)
    step: None | ClockSteps | TimeIntervalCollection = Field(default=None)

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

    show: None | bool | TimeIntervalCollection = Field(default=None)
    leadTime: None | float | TimeIntervalCollection = Field(default=None)
    trailTime: None | float | TimeIntervalCollection = Field(default=None)
    width: None | float | TimeIntervalCollection = Field(default=None)
    resolution: None | float | TimeIntervalCollection = Field(default=None)
    material: None | Material | str | TimeIntervalCollection = Field(default=None)
    distanceDisplayCondition: (
        None | DistanceDisplayCondition | TimeIntervalCollection
    ) = Field(default=None)


class Point(BaseCZMLObject):
    """A point, or viewport-aligned circle."""

    show: None | bool | TimeIntervalCollection = Field(default=None)
    pixelSize: None | float | TimeIntervalCollection = Field(default=None)
    heightReference: None | HeightReference | TimeIntervalCollection = Field(
        default=None
    )
    color: None | Color | str | TimeIntervalCollection = Field(default=None)
    outlineColor: None | Color | str | TimeIntervalCollection = Field(default=None)
    outlineWidth: None | float | TimeIntervalCollection = Field(default=None)
    scaleByDistance: None | NearFarScalar | TimeIntervalCollection = Field(default=None)
    translucencyByDistance: None | NearFarScalar | TimeIntervalCollection = Field(
        default=None
    )
    distanceDisplayCondition: (
        None | DistanceDisplayCondition | TimeIntervalCollection
    ) = Field(default=None)
    disableDepthTestDistance: None | float | TimeIntervalCollection = Field(
        default=None
    )


class Tileset(BaseCZMLObject):
    """A 3D Tiles tileset."""

    uri: str | Uri | TimeIntervalCollection
    show: None | bool | TimeIntervalCollection = Field(default=None)
    maximumScreenSpaceError: None | float | TimeIntervalCollection = Field(default=None)


class Wall(BaseCZMLObject):
    """A two-dimensional wall defined as a line strip and optional maximum and minimum heights.
    It conforms to the curvature of the globe and can be placed along the surface or at altitude.
    """

    show: None | bool | TimeIntervalCollection = Field(default=None)
    positions: PositionList | TimeIntervalCollection
    minimumHeights: None | list[float] | TimeIntervalCollection = Field(default=None)
    maximumHeights: None | list[float] | TimeIntervalCollection = Field(default=None)
    granularity: None | float | TimeIntervalCollection = Field(default=None)
    fill: None | bool | TimeIntervalCollection = Field(default=None)
    material: None | Material | str | TimeIntervalCollection = Field(default=None)
    outline: None | bool | TimeIntervalCollection = Field(default=None)
    outlineColor: None | Color | str | TimeIntervalCollection = Field(default=None)
    outlineWidth: None | float | TimeIntervalCollection = Field(default=None)
    shadows: None | ShadowMode | TimeIntervalCollection = Field(default=None)
    distanceDisplayCondition: (
        None | DistanceDisplayCondition | TimeIntervalCollection
    ) = Field(default=None)


class NearFarScalar(BaseCZMLObject, Interpolatable, Deletable):
    """A numeric value which will be linearly interpolated between two values based on an object's distance from the
     camera, in eye coordinates.

    The computed value will interpolate between the near value and the far value while the camera distance falls
    between the near distance and the far distance, and will be clamped to the near or far value while the distance is
    less than the near distance or greater than the far distance, respectively.
    """

    nearFarScalar: None | list[float] | NearFarScalarValue | TimeIntervalCollection = (
        Field(default=None)
    )
    reference: None | str | TimeIntervalCollection = Field(default=None)

    @field_validator("reference")
    @classmethod
    def check(cls, r):
        check_reference(r)
        return r


class Label(BaseCZMLObject, HasAlignment):
    """A string of text."""

    show: None | bool | TimeIntervalCollection = Field(default=None)
    text: None | str | TimeIntervalCollection = Field(default=None)
    font: None | str | TimeIntervalCollection = Field(default=None)
    style: None | LabelStyles | TimeIntervalCollection = Field(default=None)
    scale: None | float | TimeIntervalCollection = Field(default=None)
    showBackground: None | bool | TimeIntervalCollection = Field(default=None)
    backgroundColor: None | Color | str | TimeIntervalCollection = Field(default=None)
    fillColor: None | Color | str | TimeIntervalCollection = Field(default=None)
    outlineColor: None | Color | str | TimeIntervalCollection = Field(default=None)
    outlineWidth: None | float | TimeIntervalCollection = Field(default=None)
    pixelOffset: None | float | Cartesian2Value | TimeIntervalCollection = Field(
        default=None
    )


class Orientation(BaseCZMLObject, Interpolatable, Deletable):
    """Defines an orientation.

    An orientation is a rotation that takes a vector expressed in the "body" axes of the object
    and transforms it to the Earth fixed axes.

    """

    unitQuaternion: (
        None | list[float] | UnitQuaternionValue | TimeIntervalCollection
    ) = Field(default=None)
    reference: None | str | TimeIntervalCollection = Field(default=None)
    velocityReference: None | str | TimeIntervalCollection = Field(default=None)

    @field_validator("reference")
    @classmethod
    def check(cls, r):
        check_reference(r)
        return r


class Model(BaseCZMLObject):
    """A 3D model."""

    show: None | bool | TimeIntervalCollection = Field(default=None)
    gltf: str | TimeIntervalCollection
    scale: None | float | TimeIntervalCollection = Field(default=None)
    minimumPixelSize: None | float | TimeIntervalCollection = Field(default=None)
    maximumScale: None | float | TimeIntervalCollection = Field(default=None)
    incrementallyLoadTextures: None | bool | TimeIntervalCollection = Field(
        default=None
    )
    runAnimations: None | bool | TimeIntervalCollection = Field(default=None)
    shadows: None | ShadowMode | TimeIntervalCollection = Field(default=None)
    heightReference: None | HeightReference | TimeIntervalCollection = Field(
        default=None
    )
    silhouetteColor: None | Color | str | TimeIntervalCollection = Field(default=None)
    silhouetteSize: None | Color | str | TimeIntervalCollection = Field(default=None)
    color: None | Color | str | TimeIntervalCollection = Field(default=None)
    colorBlendMode: None | ColorBlendMode | TimeIntervalCollection = Field(default=None)
    colorBlendAmount: None | float | TimeIntervalCollection = Field(default=None)
    distanceDisplayCondition: (
        None | DistanceDisplayCondition | TimeIntervalCollection
    ) = Field(default=None)
    nodeTransformations: None | Any | TimeIntervalCollection = Field(default=None)
    articulations: None | Any | TimeIntervalCollection = Field(default=None)


class Uri(BaseCZMLObject, Deletable):
    """A URI value.

    The URI can optionally vary with time.
    """

    uri: None | str | TimeIntervalCollection = Field(default=None)

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
    def custom_serializer(self) -> None | str | TimeIntervalCollection:
        return self.uri
