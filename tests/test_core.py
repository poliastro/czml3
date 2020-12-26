from czml3.core import Preamble


def test_empty_preamble_has_id_and_version():
    expected_result = """{
    "id": "document",
    "version": "1.0"
}"""

    packet = Preamble()

    assert str(packet) == expected_result
