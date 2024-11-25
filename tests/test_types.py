import datetime as dt

import astropy.time
import pytest
from pydantic import ValidationError

from czml3.types import (
    Cartesian2Value,
    Cartesian3Value,
    CartographicDegreesListValue,
    CartographicDegreesValue,
    CartographicRadiansListValue,
    CartographicRadiansValue,
    DistanceDisplayConditionValue,
    EpochValue,
    FontValue,
    IntervalValue,
    NearFarScalarValue,
    NumberValue,
    ReferenceValue,
    RgbafValue,
    RgbaValue,
    TimeInterval,
    UnitQuaternionValue,
    check_reference,
    format_datetime_like,
)


def test_invalid_near_far_scalar_value():
    with pytest.raises(TypeError) as excinfo:
        NearFarScalarValue(values=[0, 3.2, 1, 4, 2, 1])

    assert "Input values must have either 4 or N * 5 values, " in excinfo.exconly()


def test_distance_display_condition_is_invalid():
    with pytest.raises(TypeError):
        DistanceDisplayConditionValue(
            values=[0, 150, 15000000, 300, 10000, 15000000, 600]
        )


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
    with pytest.raises(TypeError) as excinfo:
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
    with pytest.raises(TypeError) as excinfo:
        CartographicDegreesListValue(values=[15, 25, 50, 30])
    assert (
        "Invalid values. Input values should be arrays of size 3 * N"
        in excinfo.exconly()
    )


@pytest.mark.parametrize("values", [[2, 2], [5, 5, 5, 5, 5]])
def test_bad_cartesian3_raises_error(values):
    with pytest.raises(TypeError) as excinfo:
        Cartesian3Value(values=values)

    assert "Input values must have either 3 or N * 4 values" in excinfo.exconly()
    assert str(Cartesian3Value()) == "[]"


@pytest.mark.parametrize("values", [[2, 2, 2, 2, 2], [5, 5, 5, 5, 5]])
def test_bad_cartesian2_raises_error(values):
    with pytest.raises(TypeError) as excinfo:
        Cartesian2Value(values=values)

    assert "Input values must have either 2 or N * 3 values" in excinfo.exconly()
    assert str(Cartesian2Value()) == "{}"


def test_reference_value():
    expected_result = '"id#property"'
    reference = ReferenceValue(string="id#property")

    assert str(reference) == expected_result


def test_invalid_reference_value():
    with pytest.raises(TypeError) as excinfo:
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
    with pytest.raises(TypeError) as excinfo:
        RgbaValue(values=[0, 0, 255])

    assert "Input values must have either 4 or N * 5 values, " in excinfo.exconly()


def test_bad_rgba_4_values_raises_error():
    with pytest.raises(TypeError) as excinfo:
        RgbaValue(values=[256, 0, 0, 255])

    assert "Color values must be integers in the range 0-255." in excinfo.exconly()


def test_bad_rgba_5_color_values_raises_error():
    with pytest.raises(TypeError) as excinfo:
        RgbaValue(values=[0, 0.1, 0.3, 0.3, 255])

    assert "Color values must be integers in the range 0-255." in excinfo.exconly()


def test_bad_rgbaf_size_values_raises_error():
    with pytest.raises(TypeError) as excinfo:
        RgbafValue(values=[0, 0, 0.1])

    assert "Input values must have either 4 or N * 5 values, " in excinfo.exconly()


def test_bad_rgbaf_4_values_raises_error():
    with pytest.raises(TypeError) as excinfo:
        RgbafValue(values=[0.3, 0, 0, 1.4])

    assert "Color values must be floats in the range 0-1." in excinfo.exconly()


def test_bad_rgbaf_5_color_values_raises_error():
    with pytest.raises(TypeError) as excinfo:
        RgbafValue(values=[0, 0.1, 0.3, 0.3, 255])

    assert "Color values must be floats in the range 0-1." in excinfo.exconly()


def test_default_time_interval():
    expected_result = '"0001-01-01T00:00:00Z/9999-12-31T23:59:59Z"'
    time_interval = TimeInterval()

    assert str(time_interval) == expected_result


def test_bad_time_raises_error():
    with pytest.raises(ValueError):
        format_datetime_like("2019/01/01")


def test_interval_value():
    start = "2019-01-01T12:00:00.000000Z"
    end = "2019-09-02T21:59:59.000000Z"

    # value is a boolean
    assert (
        str(IntervalValue(start=start, end=end, value=True))
        == """{
    "interval": "2019-01-01T12:00:00.000000Z/2019-09-02T21:59:59.000000Z",
    "boolean": true
}"""
    )

    assert (
        str(
            IntervalValue(
                start=start,
                end=end,
                value=[
                    EpochValue(value=start),
                    NumberValue(values=[1, 2, 3, 4]),
                ],
            )
        )
        == """{
    "interval": "2019-01-01T12:00:00.000000Z/2019-09-02T21:59:59.000000Z",
    "epoch": "2019-01-01T12:00:00.000000Z",
    "number": [
        1,
        2,
        3,
        4
    ]
}"""
    )


def test_epoch_value():
    epoch: str = "2019-01-01T12:00:00.000000Z"

    assert (
        str(EpochValue(value=epoch))
        == """{
    "epoch": "2019-01-01T12:00:00.000000Z"
}"""
    )

    assert (
        str(EpochValue(value=dt.datetime(2019, 1, 1, 12)))
        == """{
    "epoch": "2019-01-01T12:00:00.000000Z"
}"""
    )

    with pytest.raises(ValueError):
        str(EpochValue(value="test"))


@pytest.mark.xfail(reason="NumberValue class requires further explanaition")
def test_numbers_value():
    expected_result = """{
    "number": [
        1,
        2,
        3,
        4
    ]
}"""
    numbers = NumberValue(values=[1, 2, 3, 4])

    assert str(numbers) == expected_result

    expected_result = """{
    "number": 1.0
}"""
    numbers = NumberValue(values=1.0)

    assert str(numbers) == expected_result

    with pytest.raises(ValidationError):
        NumberValue(values="test")  # type: ignore

    with pytest.raises(ValidationError):
        NumberValue(values=[1, "test"])  # type: ignore

    with pytest.raises(ValidationError):
        NumberValue(values=[1, 2, 3, 4, 5])


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


def test_quaternion_value_is_invalid():
    with pytest.raises(TypeError):
        UnitQuaternionValue(values=[0, 0, 0, 1, 0])


def test_quaternion_value():
    expected_result = """[
    0,
    0,
    0,
    1
]"""

    result = UnitQuaternionValue(values=[0, 0, 0, 1])

    assert str(result) == expected_result


def test_cartographic_radians_value():
    result = CartographicRadiansValue(values=[0, 0, 0, 1])
    assert (
        str(result)
        == """[
    0,
    0,
    0,
    1
]"""
    )
    result = CartographicRadiansValue(values=[0, 0, 1])
    assert (
        str(result)
        == """[
    0,
    0,
    1
]"""
    )
    result = CartographicRadiansValue()
    assert str(result) == """[]"""
    with pytest.raises(TypeError):
        CartographicRadiansValue(values=[0, 0, 1, 1, 1, 1])


def test_cartographic_degrees_value():
    result = CartographicDegreesValue(values=[0, 0, 0, 1])
    assert (
        str(result)
        == """[
    0,
    0,
    0,
    1
]"""
    )
    result = CartographicDegreesValue(values=[0, 0, 1])
    assert (
        str(result)
        == """[
    0,
    0,
    1
]"""
    )
    result = CartographicDegreesValue()
    assert str(result) == """[]"""
    with pytest.raises(TypeError):
        CartographicDegreesValue(values=[0, 0, 1, 1, 1, 1])


def test_rgba_value():
    assert (
        str(RgbaValue(values=[30, 30, 30, 30]))
        == """[
    30,
    30,
    30,
    30
]"""
    )
    assert (
        str(RgbaValue(values=[30, 30, 30, 30, 1]))
        == """[
    30,
    30,
    30,
    30,
    1
]"""
    )


def test_rgbaf_value():
    assert (
        str(RgbafValue(values=[0.5, 0.5, 0.5, 0.5]))
        == """[
    0.5,
    0.5,
    0.5,
    0.5
]"""
    )
    assert (
        str(RgbafValue(values=[0.5, 0.5, 0.5, 0.5, 1]))
        == """[
    0.5,
    0.5,
    0.5,
    0.5,
    1.0
]"""
    )


def test_check_reference():
    with pytest.raises(TypeError):
        check_reference("thisthat")
    assert check_reference("this#that") is None


def test_format_datetime_like():
    assert format_datetime_like(None) is None
