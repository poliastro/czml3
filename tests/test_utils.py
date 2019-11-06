import pytest

from czml3.properties import Color
from czml3.types import RgbafValue, RgbaValue
from czml3.utils import get_color


def test_get_color_rgba():
    expected_color = Color(rgba=RgbaValue(values=[255, 204, 0, 255]))

    assert get_color("#ffcc00") == expected_color
    assert get_color(0xFFCC00) == expected_color
    assert get_color("#ffcc00ff") == expected_color
    assert get_color(0xFFCC00FF) == expected_color
    assert get_color([255, 204, 0]) == expected_color
    assert get_color([255, 204, 0, 255]) == expected_color


def test_get_color_rgbaf():
    expected_color = Color(rgbaf=RgbafValue(values=[1.0, 0.8, 0.0, 1.0]))

    # TODO: Simplify after https://github.com/poliastro/czml3/issues/36
    assert get_color([1.0, 0.8, 0.0]) == expected_color
    assert get_color([1.0, 0.8, 0.0, 1.0]) == expected_color


@pytest.mark.parametrize("input", ["a", [0, 0, 0, 0, 0], [1.0, 1.0]])
def test_get_color_invalid_input_raises_error(input):
    with pytest.raises(ValueError):
        get_color(input)
