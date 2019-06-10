from typing import Optional, Union

from czml3.common import DeletableProperty, InterpolatableProperty

from .base import BaseCZMLObject
from .enums import InterpolationAlgorithms, ReferenceFrames
from .values import Cartesian3Value, Uri


# noinspection PyPep8Naming
class Position(BaseCZMLObject, InterpolatableProperty, DeletableProperty):
    """Defines a position. The position can optionally vary over time."""

    KNOWN_PROPERTIES = (
        InterpolatableProperty.KNOWN_PROPERTIES
        + DeletableProperty.KNOWN_PROPERTIES
        + ["referenceFrame", "cartesian"]
    )

    def __init__(
        self,
        *,
        delete: Optional[bool] = None,
        epoch: Optional[str] = None,
        interpolationAlgorithm: InterpolationAlgorithms = InterpolationAlgorithms.LINEAR,
        referenceFrame: ReferenceFrames = ReferenceFrames.FIXED,
        cartesian: Union[list, Cartesian3Value, None] = None,
    ):
        super().__init__(
            delete=delete, epoch=epoch, interpolationAlgorithm=interpolationAlgorithm
        )
        if isinstance(cartesian, list):
            cartesian = Cartesian3Value(values=cartesian)
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
class Billboard(BaseCZMLObject):
    """A billboard, or viewport-aligned image.

    The billboard is positioned in the scene by the position property.
    A billboard is sometimes called a marker.
    """

    KNOWN_PROPERTIES = ["image"]

    def __init__(self, *, image: Union[str, Uri]):
        if isinstance(image, str):
            image = Uri(uri=image)

        self._image = image

    @property
    def image(self):
        """The URI of the image displayed on the billboard.

        For broadest client compatibility,
        the URI should be accessible via Cross-Origin Resource Sharing (CORS).
        The URI may also be a data URI.
        """
        return self._image
