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
