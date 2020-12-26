from io import StringIO

from czml3 import Document, Packet


def test_document_has_expected_packets():
    packet0 = Packet(id="id_00")
    packet1 = Packet(id="id_01")

    document = Document([packet0, packet1])

    assert document.packets == [packet0, packet1]


def test_doc_repr():
    packet = Packet(id="id_00")
    expected_result = """[
    {
        "id": "id_00"
    }
]"""

    document = Document([packet])

    assert str(document) == expected_result


def test_doc_dumps():
    packet = Packet(id="id_00")
    expected_result = """[{"id": "id_00"}]"""

    document = Document([packet])

    assert document.dumps() == expected_result


def test_document_dump():
    expected_result = """[{"id": "id_00"}]"""
    packet = Packet(id="id_00")

    document = Document([packet])

    with StringIO() as fp:
        document.dump(fp)
        fp.seek(0)
        result = fp.read()

    assert result == expected_result
