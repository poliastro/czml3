import datetime as dt
import json
import re
import warnings
from enum import Enum
from json import JSONEncoder

import attr

from .constants import ISO8601_FORMAT_Z

NON_DELETE_PROPERTIES = ["id", "delete"]


class CZMLEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, BaseCZMLObject):
            return o.to_json()

        elif isinstance(o, Enum):
            return o.name

        elif isinstance(o, dt.datetime):
            return o.astimezone(dt.timezone.utc).strftime(ISO8601_FORMAT_Z)

        return super().default(o)


@attr.s(str=False, frozen=True)
class BaseCZMLObject:
    def __str__(self):
        return self.dumps(indent=4)

    def dumps(self, *args, **kwargs):
        if "cls" in kwargs:
            warnings.warn("Ignoring specified cls", UserWarning)

        kwargs["cls"] = CZMLEncoder
        return json.dumps(self, *args, **kwargs)

    def dump(self, fp, *args, **kwargs):
        for chunk in CZMLEncoder(*args, **kwargs).iterencode(self):
            fp.write(chunk)

    def to_json(self):
        if getattr(self, "delete", False):
            properties_list = NON_DELETE_PROPERTIES
        else:
            properties_list = list(attr.asdict(self).keys())

        obj_dict = {}
        for property_name in properties_list:
            if getattr(self, property_name, None) is not None:
                obj_dict[property_name] = getattr(self, property_name)

        return obj_dict

    def _svg(self):
        raise NotImplementedError

    def _repr_svg_(self, min_dim_size: float = 100.0):
        try:
            svg_elements, x_min, x_max, y_min, y_max = self._svg()

            # adjust SVG frame
            if None in (x_min, x_max, y_min, y_max):  # frame undefined
                raise ValueError("No coordinates found.")
            elif x_min == x_max and y_min == y_max:
                x_min *= 0.99
                y_min *= 0.99
                x_max *= 1.01
                y_max *= 1.01
            else:
                expand = 0.04
                widest_part = max([x_max - x_min, y_max - y_min])
                expand_amount = widest_part * expand
                x_min -= expand_amount
                y_min -= expand_amount
                x_max += expand_amount
                y_max += expand_amount

            # create SVG
            dx = x_max - x_min
            dy = y_max - y_min
            width = min([max([min_dim_size, dx]), 300.0])
            height = min([max([min_dim_size, dy]), 300.0])
            circle_radius = 0.02 * (
                max([dx - min_dim_size, dy - min_dim_size, min_dim_size])
            )
            str_svg_elements = re.sub(
                "CIRCLE_RADIUS",
                f"{circle_radius}",
                svg_elements,
            )  # scale point radius
            svg_start = f'<svg xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMinYMin meet" width="{width}" height="{height}" viewBox="{x_min} {y_min} {dx} {dy}"><g transform="matrix(1,0,0,-1,0,{y_min + y_max})">'
            svg_end = "</g></svg>"
            return "".join((svg_start, str_svg_elements, svg_end))
        except NotImplementedError:
            print(
                f"{self.__class__.__name__} class does not support the positions property."
            )
            return """<svg xmlns="http://www.w3.org/2000/svg"
xmlns:xlink="http://www.w3.org/1999/xlink"
width="50%" viewBox="0 0 1000 1000">
<path d="M512 85.333333C277.333333 85.333333 85.333333 277.333333 85.333333 512s192 426.666667 426.666667 426.666667 426.666667-192 426.666667-426.666667S746.666667 85.333333 512 85.333333z" fill="#7CB342" /><path d="M960 512c0 249.6-202.666667 448-448 448S64 761.6 64 512 262.4 64 512 64s448 198.4 448 448z m-452.266667 206.933333c0-8.533333-4.266667-12.8-12.8-17.066666-27.733333-8.533333-53.333333-8.533333-76.8-32-4.266667-8.533333-4.266667-17.066667-8.533333-27.733334-8.533333-8.533333-32-12.8-44.8-17.066666h-89.6c-12.8-4.266667-23.466667-23.466667-32-36.266667 0-4.266667 0-12.8-8.533333-12.8-8.533333-4.266667-17.066667 4.266667-27.733334 0-4.266667-4.266667-4.266667-8.533333-4.266666-12.8 0-12.8 8.533333-27.733333 17.066666-36.266667 12.8-8.533333 27.733333 4.266667 40.533334 4.266667 4.266667 0 4.266667 0 8.533333 4.266667 12.8 4.266667 17.066667 21.333333 17.066667 36.266666v8.533334c0 4.266667 4.266667 4.266667 8.533333 4.266666 4.266667-23.466667 4.266667-44.8 8.533333-68.266666 0-27.733333 27.733333-53.333333 49.066667-61.866667 8.533333-4.266667 12.8 4.266667 23.466667 0 27.733333-8.533333 93.866667-36.266667 81.066666-72.533333-8.533333-32-36.266667-61.866667-72.533333-57.6-8.533333 4.266667-12.8 8.533333-21.333333 12.8-12.8 8.533333-40.533333 36.266667-53.333334 36.266666-23.466667-4.266667-23.466667-36.266667-17.066666-49.066666 4.266667-17.066667 44.8-76.8 72.533333-66.133334l17.066667 17.066667c8.533333 4.266667 23.466667 4.266667 36.266666 4.266667 4.266667 0 8.533333 0 12.8-4.266667 4.266667-4.266667 4.266667-4.266667 4.266667-8.533333 0-12.8-12.8-27.733333-21.333333-36.266667-8.533333-8.533333-23.466667-17.066667-36.266667-23.466667-44.8-12.8-117.333333 4.266667-151.466667 36.266667s-61.866667 85.333333-81.066666 130.133333c-8.533333 27.733333-17.066667 61.866667-21.333334 93.866667-4.266667 21.333333-8.533333 40.533333 4.266667 61.866667 12.8 27.733333 40.533333 53.333333 68.266667 72.533333 17.066667 12.8 53.333333 12.8 72.533333 36.266667 12.8 17.066667 8.533333 40.533333 8.533333 61.866666 0 27.733333 17.066667 49.066667 27.733334 72.533334 4.266667 12.8 8.533333 32 12.8 44.8 0 4.266667 4.266667 32 4.266666 36.266666 27.733333 12.8 49.066667 27.733333 81.066667 36.266667 4.266667 0 21.333333-27.733333 21.333333-32 12.8-12.8 23.466667-32 36.266667-40.533333 8.533333-4.266667 17.066667-8.533333 27.733333-17.066667 8.533333-8.533333 12.8-27.733333 17.066667-40.533333 2.133333-10.666667 6.4-27.733333 2.133333-40.533334z m8.533334-413.866666c4.266667 0 8.533333-4.266667 17.066666-8.533334 12.8-8.533333 27.733333-23.466667 40.533334-32 12.8-8.533333 27.733333-23.466667 36.266666-32 12.8-8.533333 23.466667-27.733333 27.733334-40.533333 4.266667-8.533333 17.066667-27.733333 12.8-40.533333-4.266667-8.533333-27.733333-12.8-36.266667-17.066667-36.266667-8.533333-66.133333-12.8-102.4-12.8-12.8 0-32 4.266667-36.266667 17.066667-4.266667 23.466667 12.8 17.066667 32 23.466666 0 0 4.266667 36.266667 4.266667 40.533334 4.266667 21.333333-8.533333 36.266667-8.533333 57.6 0 12.8 0 36.266667 8.533333 44.8h4.266667zM891.733333 618.666667c4.266667-8.533333 4.266667-23.466667 8.533334-32 4.266667-21.333333 4.266667-44.8 4.266666-66.133334 0-44.8-4.266667-89.6-17.066666-130.133333-8.533333-12.8-12.8-27.733333-17.066667-40.533333-8.533333-23.466667-21.333333-44.8-40.533333-61.866667-17.066667-23.466667-40.533333-85.333333-81.066667-66.133333-12.8 4.266667-21.333333 21.333333-32 32-8.533333 12.8-17.066667 27.733333-27.733333 40.533333-4.266667 4.266667-8.533333 12.8-4.266667 17.066667 0 4.266667 4.266667 4.266667 8.533333 4.266666 8.533333 4.266667 12.8 4.266667 21.333334 8.533334 4.266667 0 8.533333 4.266667 4.266666 8.533333 0 0 0 4.266667-4.266666 4.266667-21.333333 23.466667-44.8 40.533333-66.133334 61.866666-4.266667 4.266667-8.533333 12.8-8.533333 17.066667 0 4.266667 4.266667 4.266667 4.266667 8.533333s-4.266667 4.266667-8.533334 8.533334c-8.533333 4.266667-17.066667 8.533333-23.466666 12.8-4.266667 8.533333 0 23.466667-4.266667 32-4.266667 23.466667-17.066667 40.533333-27.733333 61.866666-8.533333 12.8-12.8 27.733333-21.333334 40.533334 0 17.066667-4.266667 32 4.266667 44.8 21.333333 32 61.866667 12.8 93.866667 27.733333 8.533333 4.266667 17.066667 4.266667 23.466666 12.8 12.8 12.8 12.8 36.266667 17.066667 49.066667 4.266667 17.066667 8.533333 36.266667 17.066667 53.333333 4.266667 21.333333 12.8 44.8 17.066666 61.866667 40.533333-32 76.8-66.133333 102.4-110.933334 32-27.733333 44.8-64 57.6-100.266666z" fill="#0277BD" />
<text x="200" y="-790" fill="red" transform="rotate(90 0 0)" style="font-family:ariel;font-size:300">czml3</text>
<defs>
<path id="curve1" d="M 10 100 C 200 30 300 250 350 50"
stroke="black" fill="none" stroke-width="5" />
<path id="curve2" d="M 100 300 C 300 -50 600 20 800 125"
stroke="black" fill="none" stroke-width="5"  transform="translate(0,20)"/>
</defs>
<!-- <text id="T" style="font-family:ariel;font-size:16">
<textPath xlink:href="#curve1" startOffset ="10" fill="red">
<animate attributeName="startOffset" dur="7s" from="0" to="320"
repeatCount="1" />
Property has no position!
</textPath>
</text> -->
<text id="T" fill="black" style="font-family:ariel;font-size:90">
<textPath xlink:href="#curve2">
No position found.
</textPath>
</text>
</svg>"""
