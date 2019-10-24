from .properties import Color


def get_color(color):
    if isinstance(color, str):
        return get_color(int(color.rsplit("#")[-1], 16))
    elif isinstance(color, int):
        if color > 0xFFFFFF:
            values = [
                (color & 0xFF000000) >> 24,
                (color & 0x00FF0000) >> 16,
                (color & 0x0000FF00) >> 8,
                (color & 0x000000FF) >> 0,
            ]
        else:
            values = [
                (color & 0xFF0000) >> 16,
                (color & 0x00FF00) >> 8,
                (color & 0x0000FF) >> 0,
                0xFF,
            ]
    elif isinstance(color, list):
        if len(color) == 3:
            values = color + [255]
        elif len(color) == 4:
            values = color[:]
        else:
            raise ValueError("Invalid number of values")
    else:
        raise NotImplementedError

    return Color(rgba=values)
