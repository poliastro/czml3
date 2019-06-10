from czml3.properties import Position
from czml3.values import Cartesian3Value


def test_position_has_delete():
    p = Position(delete=True)

    assert p.delete


def test_position_with_delete_has_nothing_else():
    expected_result = """{
    "delete": true
}"""
    p = Position(delete=True, cartesian=Cartesian3Value([1, 2, 3]))

    assert repr(p) == expected_result
