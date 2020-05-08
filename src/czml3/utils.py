from .properties import Color


def get_color(color):

    """
    A helper function to make color setting more versatile. What the ``color`` parameter determines depends on
    its type.

    Parameters
    ----------

    color:
        :param color str/int/list: Depending on the type, ``color`` can be either a hexadecimal rgb/rgba color value or
        a tuple in the form of [r, g, b, a] or [r, g, b]. ``color`` also accepts a list of valid colors.

    """
    # Color.from_string, Color.from_int, ...
    if isinstance(color, str) and 6 <= len(color) <= 10:
        return Color.from_str(color)
    elif issubclass(int, type(color)):
        return Color.from_hex(int(color))
    elif isinstance(color, list):
        # If it is a valid color in list form, simply return it
        if Color.is_valid(color):
            return Color.from_list(color)
        # If not, check whether this is a valid list of colors:
        elif all(Color.is_valid(v) for v in color):
            return list(map(get_color, color))
        # map
        #    return [get_color(v) for v in color]
    raise ValueError("Invalid input")
