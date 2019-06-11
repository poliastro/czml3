import datetime as dt

from czml3.properties import Position
from czml3.values import Cartesian3Value


def test_position_has_delete():
    pos = Position(delete=True)

    assert pos.delete


def test_position_with_delete_has_nothing_else():
    expected_result = """{
    "delete": true
}"""
    pos_list = Position(delete=True, cartesian=[1, 2, 3])
    pos_val = Position(delete=True, cartesian=Cartesian3Value(values=[1, 2, 3]))

    assert repr(pos_list) == repr(pos_val) == expected_result


def test_position_has_given_epoch():
    expected_epoch = dt.datetime(2019, 6, 11, 12, 26, 58, tzinfo=dt.timezone.utc)

    pos = Position(epoch=expected_epoch)

    assert pos.epoch == expected_epoch


def test_position_renders_epoch():
    expected_result = """{
    "epoch": "2019-03-20T12:00:00Z",
    "interpolationAlgorithm": "LINEAR",
    "referenceFrame": "FIXED"
}"""
    pos = Position(epoch=dt.datetime(2019, 3, 20, 12, tzinfo=dt.timezone.utc))

    assert repr(pos) == expected_result
