@attr.s(auto_attribs=True, repr=False, frozen=True, kw_only=True, field_transformer=enum_fields)
class {{class_name}}{% if bases %}({{ bases | join(", ") }}){% endif %}:
    """
    {{ description | wordwrap | indent }}
    """

    {% for attr_name, attr_obj in attributes.items() -%}
    {{ attr_name }}: {{ attr_obj.type | rewrite_optional | remove_typing_prefix }}{% if attr_obj._default is none %} = None{% endif %}
    {% endfor -%}
