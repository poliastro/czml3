from .properties import Color


def get_color(color):
    # Color.from_string, Color.from_int, ...
    if isinstance(color, str) and 6 <= len(color) <= 10:
        return Color.from_str(color)
    elif isinstance(color, int):
        return Color.from_hex(color)
    elif isinstance(color, list) and len(color) <= 4:
        return Color.from_list(color)
    else:
        raise ValueError("Invalid input")
