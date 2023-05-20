from typing import Union
import datetime as dt
import json
import warnings
from enum import Enum, auto
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

    def _repr_svg_(self):
        try:
            svg_elements, x_min, x_max, y_min, y_max = self._svg()

            # create SVG
            dx = x_max - x_min
            dy = y_max - y_min
            width = min([max([100.0, dx]), 300])
            height = min([max([100.0, dy]), 300])
            svg_start = f'<svg xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMinYMin meet" width="{width}" height="{height}" viewBox="{x_min} {y_min} {dx} {dy}"><g transform="matrix(1,0,0,-1,0,{y_min + y_max})">'
            svg_end = "</g></svg>"
            return "".join((svg_start, svg_elements, svg_end))
        except NotImplementedError:
            return ""
