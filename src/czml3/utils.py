from functools import reduce

from .properties import Color
from .types import RgbafValue, RgbaValue


def get_color_list(timestamps, colors, rgbaf=False):
    """
    Given a list of valid colors (rgb/rgba tuples, shorthand hex string or integer representation) and a list of
    time-stamps, create a Color object with rgba/rgbaf values of the form: [time_0, r_0, g_0, b_0,..., time_k, r_k,
    g_k, b_k]

    Parameters
    ----------
    :param list(str) timestamps: The list of the timestamps (ISO 8601 date or seconds since epoch)
    :param str/int/list colors : A list of valid colors
    :param bool rgbaf: If set to True, returns rgbaf values, else return rgba values
    """
    # Check if colors is a valid list of colors
    if all(Color.is_valid(v) for v in colors):
        color_lst = list(map(get_color, colors))
    else:
        raise ValueError("Invalid input")

    # Quick function to convert between rgba-rgbaf easier
    if rgbaf:
        color_r = (
            lambda c: c.rgbaf.values
            if c.rgbaf
            else list(map(lambda x: float(x / 255), c.rgba.values))
        )
    else:
        color_r = (
            lambda c: c.rgba.values
            if c.rgba
            else list(map(lambda x: round(x * 255), c.rgbaf.values))
        )

    # Get combined list of timestamps and colors
    time_colr = [[time] + color_r(c) for time, c in zip(timestamps, color_lst)]
    # Flatten list
    time_colr = reduce(lambda x, y: x + y, time_colr)

    if rgbaf:
        return Color(rgbaf=RgbafValue(values=time_colr))
    else:
        return Color(rgba=RgbaValue(values=time_colr))


def get_color(color):
    """
    A helper function to make color setting more versatile. What the ``color`` parameter determines depends on
    its type.

    Parameters
    ----------

    :param  str/int/list color: Depending on the type, ``color`` can be either a hexadecimal rgb/rgba color value or
        a tuple in the form of [r, g, b, a] or [r, g, b].

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
    raise ValueError("Invalid input")
