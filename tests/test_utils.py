import pytest
from czml3.properties import Color
from czml3.types import RgbafValue, RgbaValue
from czml3.utils import get_color, get_color_list


def test_get_color_list_of_colors_rgba():
    expected_color = Color(
        rgba=RgbaValue(
            values=[
                "0000-00-00T00:00:00.000000Z",
                255,
                204,
                0,
                255,
                "9999-12-31T24:00:00.000000Z",
                255,
                204,
                0,
                255,
            ]
        )
    )
    assert (
        get_color_list(
            ["0000-00-00T00:00:00.000000Z", "9999-12-31T24:00:00.000000Z"],
            [[1.0, 0.8, 0.0, 1.0], 0xFFCC00FF],
        )
        == expected_color
    )
    assert (
        get_color_list(
            ["0000-00-00T00:00:00.000000Z", "9999-12-31T24:00:00.000000Z"],
            ["#ffcc00ff", 0xFFCC00],
        )
        == expected_color
    )


def test_get_color_list_of_colors_rgbaf():
    expected_color = Color(
        rgbaf=RgbafValue(
            values=[
                "0000-00-00T00:00:00.000000Z",
                1.0,
                0.8,
                0.0,
                1.0,
                "9999-12-31T24:00:00.000000Z",
                1.0,
                0.8,
                0.0,
                1.0,
            ]
        )
    )
    assert (
        get_color_list(
            ["0000-00-00T00:00:00.000000Z", "9999-12-31T24:00:00.000000Z"],
            [[1.0, 0.8, 0.0, 1.0], 0xFFCC00],
            rgbaf=True,
        )
        == expected_color
    )
    assert (
        get_color_list(
            ["0000-00-00T00:00:00.000000Z", "9999-12-31T24:00:00.000000Z"],
            [[255, 204, 0], 0xFFCC00FF],
            rgbaf=True,
        )
        == expected_color
    )


def test_get_color_list_of_colors_invalid():
    with pytest.raises(ValueError):
        get_color_list(
            ["0000-00-00T00:00:00.000000Z", "9999-12-31T24:00:00.000000Z"],
            [[300, 204, 0], -0xFFCC00FF],
            rgbaf=True,
        )


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


@pytest.mark.parametrize("input", ["a", [0, 0, 0, 0, -300], [0.3, 0.3, 0.1, 1.0, 1.0]])
def test_get_color_invalid_input_raises_error(input):
    with pytest.raises(ValueError):
        get_color(input)
