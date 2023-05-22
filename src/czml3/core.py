from typing import Tuple, Union
from uuid import uuid4

import attr

from .base import BaseCZMLObject
from .properties import Path, Point, Position, PositionList
from .types import Sequence

CZML_VERSION = "1.0"


@attr.s(str=False, frozen=True, kw_only=True)
class Preamble(BaseCZMLObject):
    """The preamble packet."""

    id = attr.ib(init=False, default="document")

    version = attr.ib(default=CZML_VERSION)
    name = attr.ib(default=None)
    description = attr.ib(default=None)
    clock = attr.ib(default=None)


@attr.s(str=False, frozen=True, kw_only=True)
class Packet(BaseCZMLObject):
    """A CZML Packet.

    See https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Packet
    for further information.
    """

    id = attr.ib(factory=lambda: str(uuid4()))
    delete = attr.ib(default=None)
    name = attr.ib(default=None)
    parent = attr.ib(default=None)
    description = attr.ib(default=None)
    availability = attr.ib(default=None)
    properties = attr.ib(default=None)
    position = attr.ib(default=None)
    orientation = attr.ib(default=None)
    viewFrom = attr.ib(default=None)
    billboard = attr.ib(default=None)
    box = attr.ib(default=None)
    corridor = attr.ib(default=None)
    cylinder = attr.ib(default=None)
    ellipse = attr.ib(default=None)
    ellipsoid = attr.ib(default=None)
    label = attr.ib(default=None)
    model = attr.ib(default=None)
    path = attr.ib(default=None)
    point = attr.ib(default=None)
    polygon = attr.ib(default=None)
    polyline = attr.ib(default=None)
    rectangle = attr.ib(default=None)
    tileset = attr.ib(default=None)
    wall = attr.ib(default=None)

    def _svg(
        self,
    ) -> Tuple[
        str,
        Union[None, float],
        Union[None, float],
        Union[None, float],
        Union[None, float],
    ]:
        x_min, x_max, y_min, y_max = None, None, None, None
        svg_elements = []
        for attr_name in self.__dict__.keys():
            attr = getattr(self, attr_name)
            if (
                not isinstance(attr, BaseCZMLObject)
                or isinstance(attr, Position)
                or isinstance(attr, PositionList)  # overwrite this with path or point
            ):
                continue
            if isinstance(attr, Point) and self.position is not None:
                # colour
                if attr.color is None:
                    colour = "black"
                elif attr.color.rgba is not None:
                    colour = f'rgba({",".join([str(c) for c in attr.color.rgba])})'
                elif attr.color.rgbaf is not None:
                    colour = (
                        f'rgba({",".join([str(c * 255) for c in attr.color.rgbaf])})'
                    )
                else:
                    raise AttributeError

                # get coordinates
                x_coords, y_coords = self.position._get_xy_coords()
                tmp_x_min, tmp_x_max, tmp_y_min, tmp_y_max = self.position._get_bounds(
                    x_coords, y_coords
                )

                # create SVG elements
                for x, y in zip(x_coords, y_coords):
                    svg_elements.append(
                        f'<circle fill="{colour}" cx="{x}" cy="{y}" r="CIRCLE_RADIUS" />'
                    )
            elif isinstance(attr, Path) and self.position is not None:
                # colour
                if attr.material is None:
                    colour = "black"
                elif hasattr(attr.material.solidColor.color.rgba, "values"):
                    colour = f'rgba({",".join([str(c) for c in attr.material.solidColor.color.rgba.values])})'
                elif hasattr(attr.material.solidColor.color.rgbaf, "values"):
                    colour = f'rgba({",".join([str(c * 255) for c in attr.material.solidColor.color.rgbaf.values])})'
                else:
                    raise AttributeError

                # get coordinates and bounds
                x_coords, y_coords = self.position._get_xy_coords()
                tmp_x_min, tmp_x_max, tmp_y_min, tmp_y_max = self.position._get_bounds(
                    x_coords, y_coords
                )

                # create SVG element
                points = " ".join([f"{x},{y}" for x, y in zip(x_coords, y_coords)])
                svg_elements.append(
                    f'<polyline stroke="{colour}" fill="none" points="{points}" />'
                )
            else:
                try:
                    (
                        tmp_svg_elements,
                        tmp_x_min,
                        tmp_x_max,
                        tmp_y_min,
                        tmp_y_max,
                    ) = attr._svg()
                    svg_elements.append(tmp_svg_elements)
                except NotImplementedError:
                    continue

            # bounds
            if None in (x_min, x_max, y_min, y_max):
                x_min = tmp_x_min
                x_max = tmp_x_max
                y_min = tmp_y_min
                y_max = tmp_y_max
            else:
                x_min = min(x_min, tmp_x_min)
                x_max = max(x_max, tmp_x_max)
                y_min = min(y_min, tmp_y_min)
                y_max = max(y_max, tmp_y_max)

        return "".join(svg_elements), x_min, x_max, y_min, y_max


@attr.s(str=False, frozen=True)
class Document(Sequence):
    """A CZML document, consisting on a list of packets."""

    @property
    def packets(self):
        return self._values
