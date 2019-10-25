from .base import BaseCZMLObject
from .common import Deletable, HasAlignment, Interpolatable
from .enums import ClockRanges, ClockSteps, LabelStyles
from .types import (
    ArcTypeValue,
    Cartesian3Value,
    CartographicDegreesValue,
    CartographicRadiansValue,
    FontValue,
    RgbafValue,
    RgbaValue,
    Uri,
)


class Material(BaseCZMLObject):
    """A definition of how a surface is colored or shaded."""

    KNOWN_PROPERTIES = ["solidColor", "image", "grid", "stripe", "checkerboard"]

    def __init__(
        self, *, solidColor=None, image=None, grid=None, stripe=None, checkerboard=None
    ):
        if isinstance(solidColor, Color):
            solidColor = SolidColorMaterial(color=solidColor)

        self._solid_color = solidColor
        self._image = image
        self._grid = grid
        self._stripe = stripe
        self._checkerboard = checkerboard

    @property
    def solidColor(self):
        """A material that fills the surface with a solid color, which may be translucent."""
        return self._solid_color

    @property
    def image(self):
        """A material that fills the surface with an image."""
        return self._image

    @property
    def grid(self):
        """A material that fills the surface with a grid."""
        return self._grid

    @property
    def stripe(self):
        """A material that fills the surface with alternating colors."""
        return self._stripe

    @property
    def checkerboard(self):
        """A material that fills the surface with a checkerboard pattern."""
        return self._checkerboard


class PolylineMaterial(BaseCZMLObject):
    """"A definition of how a surface is colored or shaded."""

    KNOWN_PROPERTIES = [
        "solidColor",
        "polylineOutline",
        "polylineArrow",
        "polylineDash",
        "polylineGlow",
        "image",
        "grid",
        "stripe",
        "checkerboard",
    ]

    def __init__(
        self, *, solidColor=None, image=None, grid=None, stripe=None, checkerboard=None
    ):
        if isinstance(solidColor, Color):
            solidColor = SolidColorMaterial(color=solidColor)

        self._solid_color = solidColor
        self._image = image
        self._grid = grid
        self._stripe = stripe
        self._checkerboard = checkerboard

    @property
    def solidColor(self):
        """A material that fills the surface with a solid color, which may be translucent."""
        return self._solid_color

    @property
    def image(self):
        """A material that fills the surface with an image."""
        return self._image

    @property
    def grid(self):
        """A material that fills the surface with a grid."""
        return self._grid

    @property
    def stripe(self):
        """A material that fills the surface with alternating colors."""
        return self._stripe

    @property
    def checkerboard(self):
        """A material that fills the surface with a checkerboard pattern."""
        return self._checkerboard


class SolidColorMaterial(BaseCZMLObject):
    """A material that fills the surface with a solid color."""

    KNOWN_PROPERTIES = ["color"]

    def __init__(self, *, color=None):
        self._color = color

    @property
    def color(self):
        """The color of the surface."""
        return self._color


class GridMaterial(BaseCZMLObject):
    """A material that fills the surface with a two-dimensional grid."""

    KNOWN_PROPERTIES = [
        "color",
        "cellAlpha",
        "lineCount",
        "lineThickness",
        "lineOffset",
    ]

    def __init__(
        self,
        *,
        color=None,
        cellAlpha=0.1,
        lineCount=[8, 8],
        lineThickness=[1.0, 1.0],
        lineOffset=[0.0, 0.0],
    ):
        self._color = color
        self._cell_alpha = cellAlpha
        self._line_count = lineCount
        self._line_thickness = lineThickness
        self._line_offset = lineOffset

    @property
    def color(self):
        """The color of the surface."""
        return self._color

    @property
    def cellAlpha(self):
        """The alpha value for the space between grid lines.

        This will be combined with the color alpha.

        """
        return self._cell_alpha

    @property
    def lineCount(self):
        """The number of grid lines along each axis."""
        return self._line_count

    @property
    def lineThickness(self):
        """The thickness of grid lines along each axis, in pixels."""
        return self._line_thickness

    @property
    def lineOffset(self):
        """The offset of grid lines along each axis, as a percentage from 0 to 1."""
        return self._line_offset


class StripeMaterial(BaseCZMLObject):
    """A material that fills the surface with alternating colors."""

    KNOWN_PROPERTIES = ["orientation", "evenColor", "oddColor", "offset", "repeat"]

    def __init__(
        self,
        *,
        orientation="HORIZONTAL",
        evenColor=None,
        oddColor=None,
        offset=0.0,
        repeat=1.0,
    ):

        self._orientation = orientation
        self._even_color = evenColor
        self._odd_color = oddColor
        self._offset = offset
        self._repeat = repeat

    @property
    def orientation(self):
        """The value indicating if the stripes are horizontal or vertical."""
        return self._orientation

    @property
    def evenColor(self):
        """The even color."""
        return self._even_color

    @property
    def oddColor(self):
        """The odd color."""
        return self._odd_color

    @property
    def offset(self):
        """The value indicating where in the pattern to begin drawing, with 0.0 being the beginning of the even color,
         1.0 the beginning of the odd color, 2.0 being the even color again, and any multiple or fractional values being
         in between."""
        return self._offset

    @property
    def repeat(self):
        """The number of times the stripes repeat."""
        return self._repeat


class CheckerboardMaterial(BaseCZMLObject):
    """A material that fills the surface with alternating colors."""

    KNOWN_PROPERTIES = ["orientation", "evenColor", "oddColor", "offset", "repeat"]

    def __init__(self, *, evenColor=None, oddColor=None, repeat=[1, 2]):

        self._even_color = evenColor
        self._odd_color = oddColor
        self._repeat = repeat

    @property
    def evenColor(self):
        """The even color."""
        return self._even_color

    @property
    def oddColor(self):
        """The odd color."""
        return self._odd_color

    @property
    def repeat(self):
        """The number of times the stripes repeat."""
        return self._repeat


class ImageMaterial(BaseCZMLObject):
    """A material that fills the surface with an image."""

    KNOWN_PROPERTIES = ["image", "repeat", "color", "transparent"]

    def __init__(self, *, image=None, repeat=[1, 1], color=None, transparent=False):

        self._image = image
        self._repeat = repeat
        self._color = color
        self._transparent = transparent

    @property
    def image(self):
        """The image to display on the surface."""
        return self._image

    @property
    def repeat(self):
        """The number of times the image repeats along each axis."""
        return self._repeat

    @property
    def color(self):
        """The color of the image.

         This color value is multiplied with the image to produce the final color.

         """
        return self._color

    @property
    def transparent(self):
        """Whether or not the image has transparency."""
        return self._transparent


class Color(BaseCZMLObject, Interpolatable, Deletable):
    """A color. The color can optionally vary over time."""

    KNOWN_PROPERTIES = ["delete", "rgba", "rgbaf", "reference"]

    def __init__(self, *, delete=None, rgba=None, rgbaf=None):

        if isinstance(rgba, list):
            rgba = RgbaValue(values=rgba)
        if isinstance(rgbaf, list):
            rgbaf = RgbafValue(values=rgbaf)

        self._delete = delete
        self._rgba = rgba
        self._rgbaf = rgbaf

    @property
    def rgba(self):
        """A color specified as an array of color components [Red, Green, Blue, Alpha]
        where each component is in the range 0-255.

        If the array has four elements, the color is constant.

        If it has five or more elements, they are time-tagged samples arranged as
        [Time, Red, Green, Blue, Alpha, Time, Red, Green, Blue, Alpha, ...], where Time
        is an ISO 8601 date and time string or seconds since epoch.
        """
        return self._rgba

    @property
    def rgbaf(self):
        """A color specified as an array of color components [Red, Green, Blue, Alpha]
        where each component is in the range 0.0-1.0.

        If the array has four elements, the color is constant.

        If it has five or more elements, they are time-tagged
        samples arranged as [Time, Red, Green, Blue, Alpha, Time, Red, Green, Blue, Alpha, ...],
        where Time is an ISO 8601 date and time string or seconds since epoch.

        """
        return self._rgbaf


# noinspection PyPep8Naming
class Position(BaseCZMLObject, Interpolatable, Deletable):
    """Defines a position. The position can optionally vary over time."""

    KNOWN_PROPERTIES = [
        "delete",
        "epoch",
        "interpolationAlgorithm",
        "interpolationDegree",
        "referenceFrame",
        "cartesian",
        "cartographicRadians",
        "cartographicDegrees",
    ]

    def __init__(
        self,
        *,
        delete=None,
        epoch=None,
        interpolationAlgorithm=None,
        interpolationDegree=None,
        referenceFrame=None,
        cartesian=None,
        cartographicRadians=None,
        cartographicDegrees=None,
    ):
        if all(
            val is None for val in (cartesian, cartographicDegrees, cartographicRadians)
        ):
            raise ValueError(
                "One of cartesian, cartographicDegrees or cartographicRadians must be given"
            )

        if isinstance(cartesian, list):
            cartesian = Cartesian3Value(values=cartesian)
        if isinstance(cartographicRadians, list):
            cartographicRadians = CartographicRadiansValue(values=cartographicRadians)
        if isinstance(cartographicDegrees, list):
            cartographicDegrees = CartographicDegreesValue(values=cartographicDegrees)

        self._delete = delete
        self._epoch = epoch
        self._interpolation_algorithm = interpolationAlgorithm
        self._interpolation_degree = interpolationDegree
        self._reference_frame = referenceFrame
        self._cartesian = cartesian
        self._cartographic_radians = cartographicRadians
        self._cartographic_degrees = cartographicDegrees

    @property
    def referenceFrame(self):
        """The reference frame in which cartesian positions are specified."""
        return self._reference_frame

    @property
    def cartesian(self):
        """The position specified as a three-dimensional Cartesian value.

        The value [X, Y, Z] is specified
        in meters relative to the ReferenceFrame.
        """
        return self._cartesian

    @property
    def cartographicRadians(self):
        """The position specified in Cartographic WGS84 coordinates, [Longitude, Latitude, Height].

        Longitude and Latitude are in radians and Height is in meters.

        """
        return self._cartographic_radians

    @property
    def cartographicDegrees(self):
        """The position specified in Cartographic WGS84 coordinates, [Longitude, Latitude, Height].

        Longitude and Latitude are in degrees and Height is in meters.

        """
        return self._cartographic_degrees


# noinspection PyPep8Naming
class Billboard(BaseCZMLObject, HasAlignment):
    """A billboard, or viewport-aligned image.

    The billboard is positioned in the scene by the position property.
    A billboard is sometimes called a marker.
    """

    KNOWN_PROPERTIES = [
        "show",
        "image",
        "scale",
        "pixelOffset",
        "eyeOffset",
        "horizontalOrigin",
        "verticalOrigin",
        "heightReference",
        "color",
        "rotation",
        "alignedAxis",
        "sizeInMeters",
        "width",
        "height",
        "scaleByDistance",
        "translucencyByDistance",
        "pixelOffsetScaleByDistance",
        "imageSubRegion",
        "distanceDisplayCondition",
        "disableDepthTestDistance",
    ]

    def __init__(
        self,
        *,
        image,
        show=None,
        scale=None,
        horizontalOrigin=None,
        verticalOrigin=None,
    ):
        if isinstance(image, str):
            image = Uri(uri=image)
        self._image = image
        self._show = show
        self._scale = scale
        self._horizontal_origin = horizontalOrigin
        self._vertical_origin = verticalOrigin

    @property
    def show(self):
        """Whether or not the billboard is shown."""
        return self._show

    @property
    def image(self):
        """The URI of the image displayed on the billboard.

        For broadest client compatibility,
        the URI should be accessible via Cross-Origin Resource Sharing (CORS).
        The URI may also be a data URI.
        """
        return self._image

    @property
    def scale(self):
        """The scale of the billboard.

        The scale is multiplied with the pixel size of the billboard's image.
        For example, if the scale is 2.0,
        the billboard will be rendered with twice the number of pixels,
        in each direction, of the image.

        """
        return self._scale


class EllipsoidRadii(BaseCZMLObject, Deletable, Interpolatable):
    """The radii of an ellipsoid."""

    KNOWN_PROPERTIES = ["cartesian", "reference"]

    def __init__(self, *, cartesian=None, reference=None):
        self._cartesian = cartesian
        self._reference = reference

    @property
    def cartesian(self):
        """The radii specified as a three-dimensional Cartesian value [X, Y, Z], in world coordinates in meters."""
        return self._cartesian

    @property
    def reference(self):
        """The radii specified as a reference to another property."""
        return self._reference


class Polygon(BaseCZMLObject):
    """A polygon, which is a closed figure on the surface of the Earth."""

    KNOWN_PROPERTIES = [
        "show",
        "positions",
        "holes",
        "arcType",
        "height",
        "heightReference",
        "extrudedHeight",
        "extrudedHeightReference",
        "stRotation",
        "granularity",
        "fill",
        "material",
        "outline",
        "outlineColor",
        "outlineWidth",
        "perPositionHeight",
        "closeTop",
        "closeBottom",
        "shadows",
        "distanceDisplayCondition",
        "classificationType",
        "zIndex",
    ]

    def __init__(
        self,
        *,
        positions,
        show=None,
        arcType=None,
        granularity=None,
        material=None,
        shadows=None,
        distanceDisplayCondition=None,
        classificationType=None,
        zIndex=None,
    ):
        self._position = positions
        self._show = show
        self._arc_type = arcType
        self._granularity = granularity
        self._material = material
        self._shadows = shadows
        self._distance_display_condition = distanceDisplayCondition
        self._classification_type = classificationType
        self._z_index = zIndex

    @property
    def positions(self):
        """The array of positions defining a simple polygon."""
        return self._position

    @property
    def show(self):
        """Whether or not the polygon is shown."""
        return self._show

    @property
    def arcType(self):
        """The type of arc that should connect the positions of the polygon."""
        return self._arc_type

    @property
    def granularity(self):
        """The sampling distance, in radians."""
        return self._granularity

    @property
    def material(self):
        """The material to use to fill the polygon."""
        return self._material

    @property
    def shadows(self):
        """Whether or not the polygon casts or receives shadows."""
        return self._shadows

    @property
    def distanceDisplayCondition(self):
        """The display condition specifying the distance from the camera at which this polygon will be displayed."""
        return self._distance_display_condition

    @property
    def classificationType(self):
        """Whether a classification affects terrain, 3D Tiles, or both."""
        return self._classification_type

    @property
    def zIndex(self):
        """The z-index of the polygon, used for ordering ground geometry.

        Only has an effect if the polygon is constant,
        and height and extrudedHeight are not specified.

        """
        return self._z_index


class Polyline(BaseCZMLObject):
    """A polyline, which is a line in the scene composed of multiple segments."""

    KNOWN_PROPERTIES = [
        "show",
        "positions",
        "arcType",
        "width",
        "granularity",
        "material",
        "followSurface",
        "shadows",
        "depthFailMaterial",
        "distanceDisplayCondition",
        "clampToGround",
        "classificationType",
        "zIndex",
    ]

    def __init__(
        self,
        *,
        positions,
        show=None,
        arcType=None,
        width=None,
        granularity=None,
        material=None,
        followSurface=None,
        shadows=None,
        depthFailMaterial=None,
        distanceDisplayCondition=None,
        clampToGround=None,
        classificationType=None,
        zIndex=None,
    ):
        self._position = positions
        self._show = show
        self._arc_type = arcType
        self._width = width
        self._granularity = granularity
        self._material = material
        self._follow_surface = followSurface
        self._shadows = shadows
        self._depth_fail_material = depthFailMaterial
        self._distance_display_condition = distanceDisplayCondition
        self._clamp_to_ground = clampToGround
        self._classification_type = classificationType
        self._z_index = zIndex

    @property
    def positions(self):
        """The array of positions defining the polyline as a line strip."""
        return self._position

    @property
    def show(self):
        """Whether or not the polyline is shown."""
        return self._show

    @property
    def arcType(self):
        """The type of arc that should connect the positions of the polyline."""
        return self._arc_type

    @property
    def width(self):
        """The width of the polyline."""
        return self._width

    @property
    def granulariy(self):
        """The sampling distance, in radians."""
        return self._granularity

    @property
    def material(self):
        """The material to use to draw the polyline."""
        return self._material

    @property
    def followSurface(self):
        """ Whether or not the positions are connected as great arcs (the default) or as straight lines.
        This property has been superseded by arcType, which should be used instead.
        """
        return self._follow_surface

    @property
    def shadows(self):
        """Whether or not the polyline casts or receives shadows."""
        return self._shadows

    @property
    def depthFailMaterial(self):
        """The material to use to draw the polyline when it is below the terrain."""
        return self._depth_fail_material

    @property
    def distanceDisplayCondition(self):
        """The display condition specifying at what distance from the camera this polyline will be displayed."""
        return self._distance_display_condition

    @property
    def clampToGround(self):
        """Whether or not the polyline should be clamped to the ground."""
        return self._clamp_to_ground

    @property
    def classificationType(self):
        """Whether a classification affects terrain, 3D Tiles, or both."""
        return self._classification_type

    @property
    def zIndex(self):
        """ The z-index of the polyline, used for ordering ground geometry. Only has an effect if the polyline is
        constant, and clampToGround is true.
        """
        return self._z_index


class ArcType(BaseCZMLObject, Deletable):
    """The type of an arc."""

    KNOWN_PROPERTIES = ["arcType", "reference"]

    def __init__(self, *, arcType=None, reference=None):

        if isinstance(arcType, str):
            arcType = ArcTypeValue(string=arcType)

        self._arc_type = arcType
        self._reference = reference

    @property
    def arcType(self):
        """The arc type"""
        return self._arc_type

    @property
    def reference(self):
        """The arc type specified as a reference to another property."""
        return self._reference


class ShadowMode(BaseCZMLObject, Deletable):
    """Whether or not an object casts or receives shadows from each light source when shadows are enabled."""

    KNOWN_PROPERTIES = ["shadowMode", "reference"]

    def __init__(self, *, shadowMode=None, reference=None):
        self._shadow_mode = shadowMode
        self._reference = reference

    @property
    def shadowMode(self):
        """The shadow mode"""
        return self._shadow_mode

    @property
    def reference(self):
        """The shadow mode specified as a reference to another property."""
        return self._reference


class ClassificationType(BaseCZMLObject, Deletable):
    """Whether a classification affects terrain, 3D Tiles, or both."""

    KNOWN_PROPERTIES = ["classificationType", "reference"]

    def __init__(self, *, classificationType=None, reference=None):
        self._classification_type = classificationType
        self._reference = reference

    @property
    def classificationType(self):
        """The classification type, which indicates whether a classification affects terrain, 3D Tiles, or both."""
        return self._classification_type

    @property
    def reference(self):
        """The classification type specified as a reference to another property."""
        return self._reference


class DistanceDisplayCondition(BaseCZMLObject, Interpolatable, Deletable):
    """Indicates the visibility of an object based on the distance to the camera."""

    KNOWN_PROPERTIES = ["distanceDisplayCondition", "reference"]

    def __init__(self, *, distanceDisplayCondition=None, reference=None):
        self._distance_display_condition = distanceDisplayCondition
        self._reference = reference

    @property
    def distanceDisplayCondition(self):
        """The value specified as two values [NearDistance, FarDistance], with distances in meters."""
        return self._distance_display_condition

    @property
    def reference(self):
        """The value specified as a reference to another property."""
        return self._reference


class PositionList(BaseCZMLObject, Deletable):
    """A list of positions."""

    KNOWN_PROPERTIES = [
        "referenceFrame",
        "cartersian",
        "cartographicRadians",
        "cartographicDegrees",
        "references",
    ]

    def __init__(
        self,
        *,
        referenceFrame=None,
        cartesian=None,
        cartographicRadians=None,
        cartographicDegrees=None,
        references=None,
    ):
        self._reference_frames = referenceFrame
        self._cartesian = cartesian
        self._cartographic_radians = cartographicRadians
        self._cartographic_degrees = cartographicDegrees
        self._references = references

    @property
    def referenceFrame(self):
        """The reference frame in which cartesian positions are specified. Possible values are "FIXED" and
        "INERTIAL"."""
        return self._reference_frames

    @property
    def cartesian(self):
        """The list of positions specified as three-dimensional Cartesian values, [X, Y, Z, X, Y, Z, ...],
        in meters relative to the referenceFrame."""
        return self._cartesian

    @property
    def cartographicRadians(self):
        """The list of positions specified in Cartographic WGS84 coordinates, [Longitude, Latitude, Height, Longitude,
         Latitude, Height, ...], where Longitude and Latitude are in radians and Height is in meters."""
        return self._cartographic_radians

    @property
    def cartographicDegrees(self):
        """The list of positions specified in Cartographic WGS84 coordinates, [Longitude, Latitude, Height, Longitude,
        Latitude, Height, ...], where Longitude and Latitude are in degrees and Height is in meters."""
        return self._cartographic_degrees

    @property
    def references(self):
        """The list of positions specified as references. Each reference is to a property that defines a single
        position, which may change with time."""
        return self._references


class Ellipsoid(BaseCZMLObject):
    """A closed quadric surface that is a three-dimensional analogue of an ellipse."""

    KNOWN_PROPERTIES = [
        "radii",
        "show",
        "heightReference",
        "fill",
        "material",
        "outline",
        "outlineColor",
        "outlineWidth",
        "stackPartitions",
        "slicePartitions",
        "subdivisions",
        "shadows",
        "distanceDisplayCondition",
    ]

    def __init__(
        self,
        *,
        radii,
        show=None,
        heightReference=None,
        fill=None,
        material=None,
        outline=None,
        outlineColor=None,
        outlineWidth=None,
        stackPartitions=None,
        slicePartitions=None,
        subdivisions=None,
    ):
        self._radii = radii
        self._show = show
        self._height_reference = heightReference
        self._fill = fill
        self._material = material
        self._outline = outline
        self._outline_color = outlineColor
        self._outline_width = outlineWidth
        self._stack_partitions = stackPartitions
        self._slice_partitions = slicePartitions
        self._subdivisions = subdivisions

    @property
    def show(self):
        """Whether or not the ellipsoid is shown."""
        return self._show

    @property
    def radii(self):
        """The dimensions of the ellipsoid."""
        return self._radii

    @property
    def heightReference(self):
        """The height reference of the ellipsoid, which indicates if the position is relative to terrain or not."""
        return self._height_reference

    @property
    def fill(self):
        """Whether or not the ellipsoid is filled."""
        return self._fill

    @property
    def material(self):
        """The material to display on the surface of the ellipsoid."""
        return self._material

    @property
    def outline(self):
        """Whether or not the ellipsoid is outlined."""
        return self._outline

    @property
    def outlineColor(self):
        """The color of the ellipsoid outline."""
        return self._outline_color

    @property
    def outlineWidth(self):
        """The width of the ellipsoid outline."""
        return self._outline_width

    @property
    def stackPartitions(self):
        """The number of times to partition the ellipsoid into stacks."""
        return self._stack_partitions

    @property
    def slicePartitions(self):
        """The number of times to partition the ellipsoid into radial slices."""
        return self._slice_partitions

    @property
    def subdivisions(self):
        """The number of samples per outline ring, determining the granularity of the curvature."""
        return self._subdivisions


class Box(BaseCZMLObject):
    """A box, which is a closed rectangular cuboid."""

    KNOWN_PROPERTIES = [
        "show",
        "dimensions",
        "heightReference",
        "fill",
        "material",
        "outline",
        "outlineColor",
        "outlineWidth",
        "shadows",
        "distanceDisplayCondition",
    ]

    def __init__(
        self,
        show=None,
        dimensions=None,
        heightReference=None,
        fill=None,
        material=None,
        outline=None,
        outlineColor=None,
        outlineWidth=None,
        shadows=None,
        distanceDisplayCondition=None,
    ):
        self._show = show
        self._dimensions = dimensions
        self._heightReference = heightReference
        self._fill = fill
        self._material = material
        self._outline = outline
        self._outlineColor = outlineColor
        self._outlineWidth = outlineWidth
        self._shadows = shadows
        self._distanceDisplayCondition = distanceDisplayCondition

    @property
    def show(self):
        """Whether or not the box is shown."""
        return self._show

    @property
    def dimensions(self):
        """The dimensions of the box."""
        return self._dimensions

    @property
    def heightReference(self):
        """The height reference of the box, which indicates if the position is relative to terrain or not."""
        return self._heightReference

    @property
    def fill(self):
        """Whether or not the box is filled."""
        return self._fill

    @property
    def material(self):
        """The material to display on the surface of the box."""
        return self._material

    @property
    def outline(self):
        """Whether or not the box is outlined."""
        return self._outline

    @property
    def outlineColor(self):
        """The color of the box outline."""
        return self._outlineColor

    @property
    def outlineWidth(self):
        """The width of the box outline."""
        return self._outlineWidth

    @property
    def shadows(self):
        """Whether or not the box casts or receives shadows."""
        return self._shadows

    @property
    def distanceDisplayCondition(self):
        """The display condition specifying the distance from the camera at which this box will be displayed."""
        return self._distanceDisplayCondition


class BoxDimensions(BaseCZMLObject, Interpolatable):
    """The width, depth, and height of a box."""

    KNOWN_PROPERTIES = ["cartesian", "reference"]

    def __init__(self, *, cartesian=None, reference=None):
        self._cartesian = cartesian
        self._reference = reference

    @property
    def cartesian(self):
        """The dimensions specified as a three-dimensional Cartesian value [X, Y, Z], with X representing width, Y representing depth, and Z representing height, in world coordinates in meters."""
        return self._cartesian

    @property
    def reference(self):
        """The dimensions specified as a reference to another property."""
        return self._reference


class EyeOffset(BaseCZMLObject, Deletable):
    """An offset in eye coordinates which can optionally vary over time. Eye coordinates are a left-handed coordinate system where the X-axis points toward the viewer's right, the Y-axis poitns up, and the Z-axis points into the screen."""

    KNOWN_PROPERTIES = ["cartesian", "reference"]

    def __init__(self, *, cartesian=None, reference=None):
        self._cartesian = cartesian
        self._reference = reference

    @property
    def cartesian(self):
        """The eye offset specified as a three-dimensional Cartesian value [X, Y, Z], in eye coordinates in meters. If the array has three elements, the eye offset is constant. If it has four or more elements, they are time-tagged samples arranged as [Time, X, Y, Z, Time, X, Y, Z, ...], where Time is an ISO 8601 date and time string or seconds since epoch."""
        return self._cartesian

    @property
    def reference(self):
        """The eye offset specified as a reference to another property."""
        return self._reference


class HeightReference(BaseCZMLObject, Deletable):
    """The height reference of an object, which indicates if the object's position is relative to terrain or not."""

    KNOWN_PROPERTIES = ["heightReference", "reference"]

    def __init__(self, *, heightReference=None, reference=None):
        self._height_reference = heightReference
        self._reference = reference

    @property
    def heightReference(self):
        return self._height_reference

    @property
    def reference(self):
        return self._reference


# noinspection PyPep8Naming
class Clock(BaseCZMLObject):
    """Initial settings for a simulated clock when a document is loaded.

    The start and stop time are configured using the interval property.

    """

    KNOWN_PROPERTIES = ["currentTime", "multiplier", "range", "step"]

    def __init__(
        self,
        *,
        currentTime=None,
        multiplier=1.0,
        range=ClockRanges.LOOP_STOP,
        step=ClockSteps.SYSTEM_CLOCK_MULTIPLIER,
    ):
        self._current_time = currentTime
        self._multiplier = multiplier
        self._range = range
        self._step = step

    @property
    def currentTime(self):
        """The current time, specified in ISO8601 format."""
        return self._current_time

    @property
    def multiplier(self):
        """The multiplier.

        When step is set to TICK_DEPENDENT,
        this is the number of seconds to advance each tick.
        When step is set to SYSTEM_CLOCK_DEPENDENT,
        this is multiplied by the elapsed system time between ticks.
        This value is ignored in SYSTEM_CLOCK mode.

        """
        return self._multiplier

    @property
    def range(self):
        """The behavior when the current time reaches its start or end times."""
        return self._range

    @property
    def step(self):
        """How the current time advances each tick."""
        return self._step


# noinspection PyPep8Naming
class Path(BaseCZMLObject):
    """A path, which is a polyline defined by the motion of an object over time.

    The possible vertices of the path are specified by the position property.
    Note that because clients cannot render a truly infinite path,
    the path must be limited,
    either by defining availability for this object,
    or by using the leadTime and trailTime properties.

    """

    KNOWN_PROPERTIES = [
        "show",
        "leadTime",
        "trailTime",
        "width",
        "resolution",
        "material",
        "distanceDisplayCondition",
    ]

    def __init__(
        self,
        *,
        show=True,
        leadTime=None,
        trailTime=None,
        width=1.0,
        resolution=60.0,
        material=None,
        distanceDisplayCondition=None,
    ):
        self._show = show
        self._lead_time = leadTime
        self._trail_time = trailTime
        self._width = width
        self._resolution = resolution
        self._material = material
        self._distance_display_condition = distanceDisplayCondition

    @property
    def show(self):
        """Whether or not the path is shown."""
        return self._show

    @property
    def leadTime(self):
        """The time ahead of the animation time, in seconds, to show the path.

        The time will be limited to not exceed the object's availability.
        By default, the value is unlimited,
        which effectively results in drawing the entire available path of the object.

        """
        return self._lead_time

    @property
    def trailTime(self):
        """The time behind the animation time, in seconds, to show the path.

        The time will be limited to not exceed the object's availability.
        By default, the value is unlimited,
        which effectively results in drawing the entire available path of the object.

        """
        return self._trail_time

    @property
    def width(self):
        """The width of the path line."""
        return self._width

    @property
    def resolution(self):
        """The maximum step-size, in seconds, used to sample the path.

        If the position property has data points
        farther apart than resolution specifies,
        additional samples will be computed,
        creating a smoother path.

        """
        return self._resolution

    @property
    def distanceDisplayCondition(self):
        """The display condition specifying at what
         distance from the camera this path will be displayed.

         """
        return self._distance_display_condition

    @property
    def material(self):
        """The material to use to draw the path."""
        return self._material


class Point(BaseCZMLObject):
    """A point, or viewport-aligned circle."""

    KNOWN_PROPERTIES = [
        "show",
        "pixelSize",
        "heightReference",
        "color",
        "outlineColor",
        "outlineWidth",
        "scaleByDistance",
        "translucencyByDistance",
        "distanceDisplayCondition",
        "disableDepthTestDistance",
    ]

    def __init__(
        self,
        *,
        show=None,
        pixelSize=None,
        heightReference=None,
        color=None,
        outlineColor=None,
        outlineWidth=None,
        scaleByDistance=None,
        translucencyByDistance=None,
        distanceDisplayCondition=None,
        disableDepthTestDistance=None,
    ):
        self._show = show
        self._pixel_size = pixelSize
        self._height_reference = heightReference
        self._color = color
        self._outline_color = outlineColor
        self._outline_width = outlineWidth
        self._scale_by_distance = scaleByDistance
        self._translucency_by_distance = translucencyByDistance
        self._distance_display_condition = distanceDisplayCondition
        self._disable_depth_test_distance = disableDepthTestDistance

    @property
    def show(self):
        """Whether or not the point is shown."""
        return self._show

    @property
    def pixelSize(self):
        """The size of the point, in pixels."""
        return self._pixel_size

    @property
    def heightReference(self):
        """The height reference of the point, which indicates if the position is relative to terrain or not."""
        return self._height_reference

    @property
    def color(self):
        """The color of the point."""
        return self._color

    @property
    def outlineColor(self):
        """The color of the outline of the point."""
        return self._outline_color

    @property
    def outlineWidth(self):
        """The width of the outline of the point."""
        return self._outline_width

    @property
    def scaleByDistance(self):
        """ How the point's scale should change based on the point's distance from the camera.
        This scalar value will be multiplied by pixelSize.
        """
        return self._scale_by_distance

    @property
    def translucencyByDistance(self):
        """ How the point's translucency should change based on the point's distance from the camera.
        This scalar value should range from 0 to 1.
        """
        return self._translucency_by_distance

    @property
    def distanceDisplayCondition(self):
        """The display condition specifying the distance from the camera at which this point will be displayed."""
        return self._distance_display_condition

    @property
    def disableDepthTestDistance(self):
        """ The distance from the camera at which to disable the depth test. This can be used to prevent clipping
        against terrain, for example. When set to zero, the depth test is always applied.

        When set to Infinity, the depth test is never applied.
        """
        return self._disable_depth_test_distance


class NearFarScalar(BaseCZMLObject, Interpolatable, Deletable):
    """ A numeric value which will be linearly interpolated between two values based on an object's distance from the
     camera, in eye coordinates.

    The computed value will interpolate between the near value and the far value while the camera distance falls
    between the near distance and the far distance, and will be clamped to the near or far value while the distance is
    less than the near distance or greater than the far distance, respectively.
    """

    KNOWN_PROPERTIES = ["nearFarScalar", "reference"]

    def __init__(self, *, nearFarScalar=None, reference=None):
        self._near_far_scalar = nearFarScalar
        self._reference = reference

    @property
    def nearFarScalar(self):
        """ The value specified as four values [NearDistance, NearValue, FarDistance, FarValue], with distances in eye
        coordinates in meters.
        """
        return self._near_far_scalar

    @property
    def reference(self):
        """The value specified as a reference to another property."""
        return self._reference


# noinspection PyPep8Naming
class Label(BaseCZMLObject, HasAlignment):
    """A string of text."""

    KNOWN_PROPERTIES = [
        "show",
        "text",
        "font",
        "style",
        "scale",
        "showBackground",
        "backgroundColor",
        "backgroundPadding",
        "pixelOffset",
        "eyeOffset",
        "horizontalOrigin",
        "verticalOrigin",
        "heightReference",
        "fillColor",
        "outlineColor",
        "outlineWidth",
        "translucencyByDistance",
        "pixelOffsetScaleByDistance",
        "scaleByDistance",
        "distanceDisplayCondition",
        "disableDepthTestDistance",
    ]

    def __init__(
        self,
        *,
        show=True,
        text=None,
        font=None,
        style=LabelStyles.FILL,
        scale=None,
        showBackground=None,
        backgroundColor=None,
        horizontalOrigin=None,
        verticalOrigin=None,
        fillColor=None,
        outlineColor=None,
        outlineWidth=1.0,
    ):

        if isinstance(font, str):
            font = FontValue(font=font)

        self._show = show
        self._text = text
        self._font = font
        self._style = style
        self._scale = scale
        self._show_background = showBackground
        self._background_color = backgroundColor
        self._horizontal_origin = horizontalOrigin
        self._vertical_origin = verticalOrigin
        self._fill_color = fillColor
        self._outline_color = outlineColor
        self._outline_width = outlineWidth

    @property
    def show(self):
        """Whether or not the label is shown."""
        return self._show

    @property
    def text(self):
        """The text displayed by the label.

        The newline character (\n) indicates line breaks.

        """
        return self._text

    @property
    def font(self):
        """The font to use for the label."""
        return self._font

    @property
    def style(self):
        """The style of the label."""
        return self._style

    @property
    def scale(self):
        """The scale of the label.

        The scale is multiplied with the pixel size of the label's text.
        For example, if the scale is 2.0,
        the label will be rendered with twice the number of pixels,
        in each direction, of the text.

        """
        return self._scale

    @property
    def showBackground(self):
        """Whether or not a background behind the label is shown."""
        return self._show_background

    @property
    def backgroundColor(self):
        """The color of the background behind the label."""
        return self._background_color

    @property
    def fillColor(self):
        """The fill color of the label."""
        return self._fill_color

    @property
    def outlineColor(self):
        """The outline color of the label."""
        return self._outline_color

    @property
    def outlineWidth(self):
        """The outline width of the label."""
        return self._outline_width
