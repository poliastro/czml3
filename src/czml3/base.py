import json
import warnings
from enum import Enum
from json import JSONEncoder
from typing import List

NON_DELETE_PROPERTIES = ["id", "delete"]


class CZMLEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, BaseCZMLObject):
            return o.to_json()

        elif isinstance(o, Enum):
            return o.value

        return super().default(o)


class BaseCZMLObject:
    KNOWN_PROPERTIES = []  # type: List[str]

    def __repr__(self):
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
            properties_list = self.KNOWN_PROPERTIES

        obj_dict = {}
        for property_name in properties_list:
            if getattr(self, property_name, None) is not None:
                obj_dict[property_name] = getattr(self, property_name)

        return obj_dict
