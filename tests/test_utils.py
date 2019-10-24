import pytest

from czml3.properties import Color
from czml3.utils import get_color


def test_get_color():
    expected_color = Color(rgba=[255, 204, 0, 255])

    # TODO: Simplify after https://github.com/poliastro/czml3/issues/36
    assert get_color("#ffcc00").rgba.values == expected_color.rgba.values
    assert get_color(0xFFCC00).rgba.values == expected_color.rgba.values
    assert get_color("#ffcc00ff").rgba.values == expected_color.rgba.values
    assert get_color(0xFFCC00FF).rgba.values == expected_color.rgba.values
    assert get_color([255, 204, 0]).rgba.values == expected_color.rgba.values
    assert get_color([255, 204, 0, 255]).rgba.values == expected_color.rgba.values


@pytest.mark.xfail
def test_get_color_missing():
    expected_color = Color(rgbaf=[1.0, 0.8, 0, 1.0])

    assert get_color([1.0, 0.8, 0, 1.0]).rgbaf.values == expected_color.rgbaf.values
