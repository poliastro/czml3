import datetime as dt
import json
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
