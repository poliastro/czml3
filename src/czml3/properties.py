from .base import BaseCZMLObject
from .common import Deletable, HasAlignment, Interpolatable
from .enums import ClockRanges, ClockSteps, LabelStyles
from .types import Cartesian3Value, FontValue, RgbafValue, RgbaValue, Uri


class Material(BaseCZMLObject):
    """A definition of how a surface is colored or shaded."""

    KNOWN_PROPERTIES = ["solidColor", "image", "grid", "stripe", "checkerboard"]

    def __init__(
        self, *, solidColor=None, image=None, grid=None, stripe=None, checkerboard=None
    ):
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
    ):
        if isinstance(cartesian, list):
            cartesian = Cartesian3Value(values=cartesian)

        self._delete = delete
        self._epoch = epoch
        self._interpolation_algorithm = interpolationAlgorithm
        self._interpolation_degree = interpolationDegree
        self._reference_frame = referenceFrame
        self._cartesian = cartesian

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
    ):
        self._show = show
        self._lead_time = leadTime
        self._trail_time = trailTime
        self._width = width
        self._resolution = resolution
        self._material = material

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
        return self._distanceDisplayCondition

    @property
    def material(self):
        """The material to use to draw the path."""
        return self._material


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
