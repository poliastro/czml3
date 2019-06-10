from czml3.properties import Position


def test_position_has_delete():
    p = Position(delete=True)

    assert p.delete
