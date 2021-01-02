import datetime as dt
from pathlib import Path
import typing
import types
from functools import lru_cache

import attr
from jinja2 import Environment, FileSystemLoader
import requests

# TODO: Should we be able to bootstrap all the code without importing it?
from czml3.enums import InterpolationAlgorithms, ExtrapolationTypes
from czml3.meta import is_optional_type

BASE_CZML_URL = "https://analyticalgraphicsinc.github.io/czml-writer/Schema"
SCHEMAS = {
    "common": {
        "Deletable": "DeletableProperty.json",
        "Interpolatable": "InterpolatableProperty.json",
    },
}
ENUM_MAPPING = {
    "interpolationAlgorithm": InterpolationAlgorithms,
    "forwardExtrapolationType": ExtrapolationTypes,
    "backwardExtrapolationType": ExtrapolationTypes,
}
BASIC_TYPES_MAPPING = {"boolean": bool, "string": str, "number": int}


# https://github.com/python/cpython/blob/v3.8.7/Lib/typing.py#L153-L169
def _type_repr(obj):
    """Return the repr() of an object, special-casing types (internal helper).

    If obj is a type, we return a shorter version than the default
    type.__repr__, based on the module and qualified name, which is
    typically enough to uniquely identify a type.  For everything
    else, we fall back on repr(obj).
    """
    if isinstance(obj, type):
        if obj.__module__ == "builtins" or obj.__module__.startswith("czml3"):
            return obj.__qualname__
        return f"{obj.__module__}.{obj.__qualname__}"
    if obj is ...:
        return "..."
    if isinstance(obj, types.FunctionType):
        return obj.__name__
    return repr(obj)


def rewrite_optional(type_spec):
    if is_optional_type(type_spec):
        return f"typing.Optional[{_type_repr(type_spec.__args__[0])}]"
    else:
        return _type_repr(type_spec)


def remove_typing_prefix(type_str):
    return type_str.split(".", 1)[-1]


@lru_cache
def get_schema(schema_name):
    r = requests.get(f"{BASE_CZML_URL}/{schema_name}")
    r.raise_for_status()

    return r.json()


def get_czml_type(property_name, property_metadata):
    if "Valid values are " in property_metadata["description"]:
        return ENUM_MAPPING[property_name]

    return BASIC_TYPES_MAPPING[property_metadata["type"]]


def get_property_metadata(property_metadata):
    if ref := property_metadata.get("$ref"):
        return get_schema(ref)
    else:
        return property_metadata


def make_field(property_name, property_metadata):
    property_metadata = get_property_metadata(property_metadata)
    field_type = get_czml_type(property_name, property_metadata)

    if property_metadata.get("czmlRequiredForDisplay", False):
        return attr.ib(type=field_type)
    else:
        return attr.ib(type=typing.Optional[field_type], default=None)


def make_spec(schema):
    return {
        name: make_field(name, metadata)
        for name, metadata in schema["properties"].items()
    }


if __name__ == "__main__":
    env = Environment(loader=FileSystemLoader("templates"))
    env.filters["rewrite_optional"] = rewrite_optional
    env.filters["remove_typing_prefix"] = remove_typing_prefix

    class_tpl = env.get_template("class.tpl")
    module_tpl = env.get_template("module.tpl")
    for module_name, schemas in SCHEMAS.items():
        classes = []
        for schema_name, schema_url in schemas.items():
            schema = get_schema(schema_url)
            classes.append(
                class_tpl.render(
                    class_name=schema_name,
                    description=schema["description"],
                    attributes=make_spec(schema),
                )
            )

        with open(Path("src") / "czml3" / f"{module_name}.py", "w") as fp:
            fp.write(
                module_tpl.render(
                    generation_date=dt.datetime.now(),
                    # TODO: Autogenerate imports somehow
                    imports=[
                        "from typing import Optional",
                        "import attr",
                        "from .enums import ExtrapolationTypes, InterpolationAlgorithms",
                        "from .meta import enum_fields",
                    ],
                    classes=classes,
                )
            )
