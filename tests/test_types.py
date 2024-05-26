import datetime as dt

import astropy.time
import pytest
from czml3.types import (
    Cartesian3Value,
    CartographicDegreesListValue,
    CartographicRadiansListValue,
    DistanceDisplayConditionValue,
    FontValue,
    NearFarScalarValue,
    ReferenceValue,
    RgbafValue,
    RgbaValue,
    TimeInterval,
    UnitQuaternionValue,
    format_datetime_like,
)
from dateutil.tz import tzoffset


def test_invalid_near_far_scalar_value():
    with pytest.raises(ValueError) as excinfo:
        NearFarScalarValue(values=[0, 3.2, 1, 4, 2, 1])

    assert "Input values must have either 4 or N * 5 values, " in excinfo.exconly()


def test_distance_display_condition():
    expected_result = """[
    0,
    150,
    15000000,
    300,
    10000,
    15000000,
    600,
    150,
    15000000
]"""
    dist = DistanceDisplayConditionValue(
        values=[0, 150, 15000000, 300, 10000, 15000000, 600, 150, 15000000]
    )
    assert str(dist) == expected_result


def test_cartographic_radian_list():
    expected_result = """[
    0,
    1,
    0
]"""
    car = CartographicRadiansListValue(values=[0, 1, 0])
    assert str(car) == expected_result


def test_invalid_cartograpic_radian_list():
    with pytest.raises(ValueError) as excinfo:
        CartographicRadiansListValue(values=[1])
    assert (
        "Invalid values. Input values should be arrays of size 3 * N"
        in excinfo.exconly()
    )


def test_cartograpic_degree_list():
    expected_result = """[
    15,
    25,
    50
]"""
    car = CartographicDegreesListValue(values=[15, 25, 50])
    assert str(car) == expected_result


def test_invalid_cartograpic_degree_list():
    with pytest.raises(ValueError) as excinfo:
        CartographicDegreesListValue(values=[15, 25, 50, 30])
    assert (
        "Invalid values. Input values should be arrays of size 3 * N"
        in excinfo.exconly()
    )


@pytest.mark.parametrize("values", [[2, 2], [5, 5, 5, 5, 5]])
def test_bad_cartesian_raises_error(values):
    with pytest.raises(ValueError) as excinfo:
        Cartesian3Value(values=values)

    assert "Input values must have either 3 or N * 4 values" in excinfo.exconly()


def test_reference_value():
    expected_result = '"id#property"'
    reference = ReferenceValue(string="id#property")

    assert str(reference) == expected_result


def test_invalid_reference_value():
    with pytest.raises(ValueError) as excinfo:
        ReferenceValue(string="id")

    assert (
        "Invalid reference string format. Input must be of the form id#property"
        in excinfo.exconly()
    )


def test_font_value():
    expected_result = '"20px sans-serif"'
    font = FontValue(font="20px sans-serif")

    assert str(font) == expected_result


def test_font_property_value():
    expected_result = "20px sans-serif"
    font = FontValue(font="20px sans-serif")

    assert font.font == expected_result


def test_bad_rgba_size_values_raises_error():
    with pytest.raises(ValueError) as excinfo:
        RgbaValue(values=[0, 0, 255])

    assert "Input values must have either 4 or N * 5 values, " in excinfo.exconly()


def test_bad_rgba_4_values_raises_error():
    with pytest.raises(ValueError) as excinfo:
        RgbaValue(values=[256, 0, 0, 255])

    assert "Color values must be integers in the range 0-255." in excinfo.exconly()


def test_bad_rgba_5_color_values_raises_error():
    with pytest.raises(ValueError) as excinfo:
        RgbaValue(values=[0, 0.1, 0.3, 0.3, 255])

    assert "Color values must be integers in the range 0-255." in excinfo.exconly()


def test_bad_rgbaf_size_values_raises_error():
    with pytest.raises(ValueError) as excinfo:
        RgbafValue(values=[0, 0, 0.1])

    assert "Input values must have either 4 or N * 5 values, " in excinfo.exconly()


def test_bad_rgbaf_4_values_raises_error():
    with pytest.raises(ValueError) as excinfo:
        RgbafValue(values=[0.3, 0, 0, 1.4])

    assert "Color values must be floats in the range 0-1." in excinfo.exconly()


def test_bad_rgbaf_5_color_values_raises_error():
    with pytest.raises(ValueError) as excinfo:
        RgbafValue(values=[0, 0.1, 0.3, 0.3, 255])

    assert "Color values must be floats in the range 0-1." in excinfo.exconly()


def test_default_time_interval():
    expected_result = '"0000-00-00T00:00:00Z/9999-12-31T24:00:00Z"'
    time_interval = TimeInterval()

    assert str(time_interval) == expected_result


def test_custom_time_interval():
    tz = tzoffset("UTC+02", dt.timedelta(hours=2))
    start = dt.datetime(2019, 1, 1, 12, 0, tzinfo=dt.timezone.utc)
    end = dt.datetime(2019, 9, 2, 23, 59, 59, tzinfo=tz)

    expected_result = '"2019-01-01T12:00:00.000000Z/2019-09-02T21:59:59.000000Z"'

    time_interval = TimeInterval(start=start, end=end)

    assert str(time_interval) == expected_result


def test_bad_time_raises_error():
    with pytest.raises(ValueError):
        format_datetime_like("2019/01/01")


@pytest.mark.xfail
def test_astropy_time_retains_input_format():
    # It would be nice to recover the input format,
    # but it's difficult without conditionally depending on Astropy
    expected_result = "2012-03-15T10:16:06.97400000000198Z"
    time = astropy.time.Time(expected_result)

    result = format_datetime_like(time)

    assert result == expected_result


def test_astropy_time_format():
    expected_result = "2012-03-15T10:16:06.974Z"
    time = astropy.time.Time("2012-03-15T10:16:06.97400000000198Z")

    result = format_datetime_like(time)

    assert result == expected_result


def test_quaternion_value():
    expected_result = """[
    0,
    0,
    0,
    1
]"""

    result = UnitQuaternionValue(values=[0, 0, 0, 1])

    assert str(result) == expected_result
