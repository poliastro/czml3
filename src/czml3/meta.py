from enum import EnumMeta
from typing import Any, List, Optional, Union

import attr


def _transform_enum_field(field):
    # Apart from making the code cleaner,
    # this function protects the scope of field
    # so it is not reused across iterations!
    if field.type and is_optional_type(field.type):
        enum_type = field.type.__args__[0]
        return field.evolve(
            type=Optional[str],
            converter=lambda v: v if v is None else enum_type(v).value,
            validator=attr.validators.in_(enum_type._member_names_ + [None]),
        )
    else:
        enum_type = field.type
        return field.evolve(
            type=str,
            default=field.type._member_names_[0],  # TODO: Check this
            converter=attr.converters.pipe(enum_type, lambda v: v.value),
            validator=attr.validators.in_(enum_type._member_names_),
        )


def is_optional_type(t):
    return (
        t.__module__ == "typing"
        and t.__origin__ is Union
        and len(t.__args__) == 2
        and isinstance(None, t.__args__[1])
    )


def enum_fields(cls, fields):
    new_fields = []  # type: List[attr.Attribute[Any]]
    for field in fields:
        if field.type and is_optional_type(field.type):
            field_type = field.type.__args__[0]
        else:
            field_type = field.type

        if isinstance(field_type, EnumMeta):
            # Transform fields whose type is enum so they:
            # - Have str or Optional[str] as actual type
            # - Convert the value to enum member and then back to string, or use None (abuse converter as validator)
            # - Validate that the final value is part of the enum or None
            new_fields.append(_transform_enum_field(field))
        else:
            new_fields.append(field)

    return new_fields
