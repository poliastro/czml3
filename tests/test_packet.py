from io import StringIO
from uuid import UUID

import pytest

from czml3 import Packet
from czml3.enums import InterpolationAlgorithms, ReferenceFrames
from czml3.properties import Position
from czml3.values import Cartesian3Value


def test_auto_generated_id():
    packet = Packet()

    assert UUID(packet.id, version=4)


def test_packet_custom_id():
    expected_id = "id_00"
    packet = Packet(id=expected_id)

    assert packet.id == expected_id


def test_packet_repr_id_only():
    expected_result = """{
    "id": "id_00"
}"""
    packet = Packet(id="id_00")

    assert repr(packet) == expected_result


def test_packet_repr_id_name():
    expected_result = """{
    "id": "id_00",
    "name": "Test Packet"
}"""
    packet = Packet(id="id_00", name="Test Packet")

    assert repr(packet) == expected_result


def test_packet_dumps():
    expected_result = """{"id": "id_00"}"""
    packet = Packet(id="id_00")

    assert packet.dumps() == expected_result


def test_packet_dump():
    expected_result = """{"id": "id_00"}"""
    packet = Packet(id="id_00")

    with StringIO() as fp:
        packet.dump(fp)
        fp.seek(0)
        result = fp.read()

    assert result == expected_result


@pytest.mark.xfail
def test_packet_constant_cartesian_position_perfect():
    # Trying to group the cartesian value by sample
    # is much more difficult than expected.
    # Pull requests welcome
    expected_result = """{
    "id": "MyObject",
    "position": {
        "interpolationAlgorithm": "LINEAR",
        "referenceFrame": "FIXED",
        "cartesian": [
            0.0, 0.0, 0.0
        ]
    }
}"""
    packet = Packet(
        id="MyObject", position=Position(cartesian=Cartesian3Value([0.0, 0.0, 0.0]))
    )

    assert repr(packet) == expected_result


def test_packet_constant_cartesian_position():
    expected_result = """{
    "id": "MyObject",
    "position": {
        "interpolationAlgorithm": "LINEAR",
        "referenceFrame": "FIXED",
        "cartesian": [
            0.0,
            0.0,
            0.0
        ]
    }
}"""
    packet = Packet(
        id="MyObject", position=Position(cartesian=Cartesian3Value([0.0, 0.0, 0.0]))
    )

    assert repr(packet) == expected_result


@pytest.mark.xfail
def test_packet_dynamic_cartesian_position_perfect():
    # Trying to group the cartesian value by sample
    # is much more difficult than expected.
    # Pull requests welcome
    expected_result = """{
    "id": "InternationalSpaceStation",
    "position": {
        "interpolationAlgorithm": "LAGRANGE",
        "referenceFrame": "INERTIAL",
        "cartesian": [
            0.0, -6668447.2211117, 1201886.45913705, 146789.427467256,
            60.0, -6711432.84684144, 919677.673492462, -214047.552431458
        ]
    }
}"""
    packet = Packet(
        id="InternationalSpaceStation",
        position=Position(
            interpolationAlgorithm=InterpolationAlgorithms.LAGRANGE,
            referenceFrame=ReferenceFrames.INERTIAL,
            cartesian=Cartesian3Value(
                [
                    0.0,
                    -6668447.2211117,
                    1201886.45913705,
                    146789.427467256,
                    60.0,
                    -6711432.84684144,
                    919677.673492462,
                    -214047.552431458,
                ]
            ),
        ),
    )

    assert repr(packet) == expected_result


def test_packet_dynamic_cartesian_position():
    expected_result = """{
    "id": "InternationalSpaceStation",
    "position": {
        "interpolationAlgorithm": "LAGRANGE",
        "referenceFrame": "INERTIAL",
        "cartesian": [
            0.0,
            -6668447.2211117,
            1201886.45913705,
            146789.427467256,
            60.0,
            -6711432.84684144,
            919677.673492462,
            -214047.552431458
        ]
    }
}"""
    packet = Packet(
        id="InternationalSpaceStation",
        position=Position(
            interpolationAlgorithm=InterpolationAlgorithms.LAGRANGE,
            referenceFrame=ReferenceFrames.INERTIAL,
            cartesian=Cartesian3Value(
                [
                    0.0,
                    -6668447.2211117,
                    1201886.45913705,
                    146789.427467256,
                    60.0,
                    -6711432.84684144,
                    919677.673492462,
                    -214047.552431458,
                ]
            ),
        ),
    )

    assert repr(packet) == expected_result
