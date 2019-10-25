from .properties import Color


def get_color(color):
    # TODO: Turn this into individual classmethods on Color?
    # Color.from_string, Color.from_int, ...
    if isinstance(color, str) and 6 <= len(color) <= 10:
        return get_color(int(color.rsplit("#")[-1], 16))
    elif isinstance(color, int):
        if color > 0xFFFFFF:
            values = {
                "rgba": [
                    (color & 0xFF000000) >> 24,
                    (color & 0x00FF0000) >> 16,
                    (color & 0x0000FF00) >> 8,
                    (color & 0x000000FF) >> 0,
                ]
            }
        else:
            values = {
                "rgba": [
                    (color & 0xFF0000) >> 16,
                    (color & 0x00FF00) >> 8,
                    (color & 0x0000FF) >> 0,
                    0xFF,
                ]
            }
    elif isinstance(color, list) and all(isinstance(v, int) for v in color):
        if len(color) == 3:
            values = {"rgba": color + [255]}
        elif len(color) == 4:
            values = {"rgba": color[:]}
        else:
            raise ValueError("Invalid number of values")
    elif isinstance(color, list) and all(isinstance(v, float) for v in color):
        if len(color) == 3:
            values = {"rgbaf": color + [1.0]}
        elif len(color) == 4:
            values = {"rgbaf": color[:]}
        else:
            raise ValueError("Invalid number of values")
    else:
        raise ValueError("Invalid input")

    return Color(**values)
