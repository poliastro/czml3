from io import StringIO
from uuid import UUID

from czml3 import Packet


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
