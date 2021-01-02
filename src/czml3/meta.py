from enum import EnumMeta
from typing import List

import attr


def _transform_enum_field(field):
    # Apart from making the code cleaner,
    # this function protects the scope of field
    # so it is not reused across iterations!
    return field.evolve(
        type=str,
        # default=field.type._member_names_[0],
        # converter=attr.converters.pipe(field.type, lambda v: v.value),
        converter=lambda v: v if v is None else field.type(v).value,
        validator=attr.validators.in_(field.type._member_names_ + [None]),
    )


def enum_fields(cls, fields):
    new_fields = []  # type: List[attr.Attribute]
    for field in fields:
        if isinstance(field.type, EnumMeta):
            # Transform fields whose type is enum so they:
            # - Have str as actual type
            # - Convert the value to enum member and then back to string, or use None (abuse converter as validator)
            # - Validate that the final value is part of the enum or None
            new_fields.append(_transform_enum_field(field))
        else:
            new_fields.append(field)

    return new_fields
