from io import StringIO
from uuid import UUID

import pytest

from czml3 import CZML_VERSION, Packet, Preamble
from czml3.enums import InterpolationAlgorithms, ReferenceFrames
from czml3.properties import Billboard, Position
from czml3.types import StringValue


def test_preamble_has_proper_id_and_expected_version():
    preamble = Preamble()

    assert preamble.id == "document"
    assert preamble.version == CZML_VERSION


def test_preamble_has_given_name():
    expected_name = "document_00"
    preamble = Preamble(name=expected_name)

    assert preamble.name == expected_name


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


def test_packet_with_delete_has_nothing_else():
    expected_result = """{
    "id": "id_00",
    "delete": true
}"""
    packet = Packet(id="id_00", delete=True, name="No Name In Packet")

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
    packet = Packet(id="MyObject", position=Position(cartesian=[0.0, 0.0, 0.0]))

    assert repr(packet) == expected_result


def test_packet_constant_cartesian_position():
    expected_result = """{
    "id": "MyObject",
    "position": {
        "cartesian": [
            0.0,
            0.0,
            0.0
        ]
    }
}"""
    packet = Packet(id="MyObject", position=Position(cartesian=[0.0, 0.0, 0.0]))

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
            cartesian=[
                0.0,
                -6668447.2211117,
                1201886.45913705,
                146789.427467256,
                60.0,
                -6711432.84684144,
                919677.673492462,
                -214047.552431458,
            ],
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
            cartesian=[
                0.0,
                -6668447.2211117,
                1201886.45913705,
                146789.427467256,
                60.0,
                -6711432.84684144,
                919677.673492462,
                -214047.552431458,
            ],
        ),
    )

    assert repr(packet) == expected_result


def test_packet_description():
    expected_result = """{
    "id": "id_00",
    "name": "Name",
    "description": "<strong>Description</strong>"
}"""
    string = "<strong>Description</strong>"
    packet_str = Packet(id="id_00", name="Name", description=string)
    packet_val = Packet(id="id_00", name="Name", description=StringValue(string=string))

    assert repr(packet_str) == repr(packet_val) == expected_result


def test_packet_custom_properties():
    expected_result = """{
    "id": "id_00",
    "properties": {
        "a": false,
        "b": 1,
        "c": "C"
    }
}"""
    prop_dict = {"a": False, "b": 1, "c": "C"}
    packet = Packet(id="id_00", properties=prop_dict)

    assert repr(packet) == expected_result


def test_packet_billboard():
    expected_result = """{
    "id": "id_00",
    "billboard": {
        "image": "file://image.png"
    }
}"""
    packet = Packet(id="id_00", billboard=Billboard(image="file://image.png"))

    assert repr(packet) == expected_result
