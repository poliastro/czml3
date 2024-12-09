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
    ReferenceListOfListsValue,
    ReferenceListValue,
    ReferenceValue,
    RgbafValue,
    RgbaValue,
    TimeInterval,
    UnitQuaternionValue,
    check_reference,
    format_datetime_like,
)


def test_invalid_near_far_scalar_value():
    with pytest.raises(TypeError):
        NearFarScalarValue(values=[0, 3.2, 1, 4, 2, 1, 0])


def test_distance_display_condition_is_invalid():
    with pytest.raises(TypeError):
        DistanceDisplayConditionValue(
            values=[0, 150, 15000000, 300, 10000, 15000000, 600]
        )


def test_distance_display_condition():
    expected_result = """[
    0.0,
    150.0,
    15000000.0,
    300.0,
    10000.0,
    15000000.0,
    600.0,
    150.0,
    15000000.0
]"""
    dist = DistanceDisplayConditionValue(
        values=[0, 150, 15000000, 300, 10000, 15000000, 600, 150, 15000000]
    )
    assert str(dist) == expected_result


def test_cartographic_radian_list():
    expected_result = """[
    0.0,
    1.0,
    0.0
]"""
    car = CartographicRadiansListValue(values=[0, 1, 0])
    assert str(car) == expected_result


def test_invalid_cartograpic_radian_list():
    with pytest.raises(TypeError):
        CartographicRadiansListValue(values=[1])


def test_cartograpic_degree_list():
    expected_result = """[
    15.0,
    25.0,
    50.0
]"""
    car = CartographicDegreesListValue(values=[15, 25, 50])
    assert str(car) == expected_result


def test_invalid_cartograpic_degree_list():
    with pytest.raises(TypeError):
        CartographicDegreesListValue(values=[15, 25, 50, 30])


@pytest.mark.parametrize("values", [[2, 2], [5, 5, 5, 5, 5]])
def test_bad_cartesian3_raises_error(values):
    with pytest.raises(TypeError):
        Cartesian3Value(values=values)


@pytest.mark.parametrize("values", [[2, 2, 2, 2, 2], [5, 5, 5, 5, 5]])
def test_bad_cartesian2_raises_error(values):
    with pytest.raises(TypeError):
        Cartesian2Value(values=values)


def test_reference_value():
    expected_result = '"id#property"'
    reference = ReferenceValue(value="id#property")

    assert str(reference) == expected_result


def test_invalid_reference_value():
    with pytest.raises(TypeError) as excinfo:
        ReferenceValue(value="id")

    assert (
        "Invalid reference string format. Input must be of the form id#property"
        in excinfo.exconly()
    )


def test_invalid_reference_list_value():
    with pytest.raises(TypeError) as excinfo:
        ReferenceListValue(values=["id"])

    assert (
        "Invalid reference string format. Input must be of the form id#property"
        in excinfo.exconly()
    )


def test_invalid_reference_list_of_lists_value():
    with pytest.raises(TypeError) as excinfo:
        ReferenceListOfListsValue(values=[["id"]])

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


def test_bad_rgba_4_values_raises_error():
    with pytest.raises(TypeError):
        RgbaValue(values=[256, 0, 0, 255])


def test_bad_rgba_5_color_values_raises_error():
    with pytest.raises(TypeError):
        RgbaValue(values=[0, 0.1, 0.3, 0.3, 256])


def test_bad_rgbaf_4_values_raises_error():
    with pytest.raises(TypeError):
        RgbafValue(values=[0.3, 0, 0, 1.4])


def test_bad_rgbaf_5_color_values_raises_error():
    with pytest.raises(TypeError):
        RgbafValue(values=[0, 0.1, 0.3, 0.3, 255])


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
        UnitQuaternionValue(values=[0, 0, 0, 1, 0, 0])


def test_quaternion_value():
    expected_result = """[
    0.0,
    0.0,
    0.0,
    1.0
]"""

    result = UnitQuaternionValue(values=[0, 0, 0, 1])

    assert str(result) == expected_result


def test_cartographic_radians_value():
    result = CartographicRadiansValue(values=[0, 0, 0, 1])
    assert (
        str(result)
        == """[
    0.0,
    0.0,
    0.0,
    1.0
]"""
    )
    result = CartographicRadiansValue(values=[0, 0, 1])
    assert (
        str(result)
        == """[
    0.0,
    0.0,
    1.0
]"""
    )
    with pytest.raises(TypeError):
        CartographicRadiansValue(values=[0, 0, 1, 1, 1, 1, 1])


def test_cartographic_degrees_value():
    result = CartographicDegreesValue(values=[0, 0, 0, 1])
    assert (
        str(result)
        == """[
    0.0,
    0.0,
    0.0,
    1.0
]"""
    )
    result = CartographicDegreesValue(values=[0, 0, 1])
    assert (
        str(result)
        == """[
    0.0,
    0.0,
    1.0
]"""
    )
    with pytest.raises(TypeError):
        CartographicDegreesValue(values=[0, 0, 1, 1, 1, 1, 1])


def test_rgba_value():
    assert (
        str(RgbaValue(values=[30, 30, 30, 30]))
        == """[
    30.0,
    30.0,
    30.0,
    30.0
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


def test_check_reference():
    with pytest.raises(TypeError):
        check_reference("thisthat")
    assert check_reference("this#that") is None


def test_format_datetime_like():
    assert format_datetime_like(None) is None


def test_reference_list():
    expected_result = """[
    "1#this",
    "1#that"
]"""
    r = ReferenceListValue(values=["1#this", "1#that"])
    assert expected_result == str(r)


def test_reference_list_of_lists():
    expected_result = """[
    [
        "1#this"
    ],
    [
        "1#that"
    ]
]"""
    r = ReferenceListOfListsValue(values=[["1#this"], ["1#that"]])
    assert expected_result == str(r)


def test_rgbaf_with_time():
    assert (
        str(RgbafValue(values=[1, 0.5, 0.5, 0.5, 0.5]))
        == """[
    1.0,
    0.5,
    0.5,
    0.5,
    0.5
]"""
    )
    assert (
        str(
            RgbafValue(
                values=[
                    1,
                    0.5,
                    0.5,
                    0.5,
                    0.5,
                    2,
                    0.8,
                    0.8,
                    0.8,
                    0.8,
                    3,
                    0.5,
                    0.5,
                    0.5,
                    0.5,
                ]
            )
        )
        == """[
    1.0,
    0.5,
    0.5,
    0.5,
    0.5,
    2.0,
    0.8,
    0.8,
    0.8,
    0.8,
    3.0,
    0.5,
    0.5,
    0.5,
    0.5
]"""
    )


def test_rgba_with_time():
    assert (
        str(RgbaValue(values=[1, 0.5, 0.5, 0.5, 0.5]))
        == """[
    1.0,
    0.5,
    0.5,
    0.5,
    0.5
]"""
    )
    assert (
        str(
            RgbaValue(
                values=[
                    1,
                    0.5,
                    0.5,
                    0.5,
                    0.5,
                    2,
                    0.8,
                    0.8,
                    0.8,
                    0.8,
                    3,
                    0.5,
                    0.5,
                    0.5,
                    0.5,
                ]
            )
        )
        == """[
    1.0,
    0.5,
    0.5,
    0.5,
    0.5,
    2.0,
    0.8,
    0.8,
    0.8,
    0.8,
    3.0,
    0.5,
    0.5,
    0.5,
    0.5
]"""
    )
