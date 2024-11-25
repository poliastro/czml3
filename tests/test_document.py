from czml3 import Document, Packet


def test_document_has_expected_packets():
    packet0 = Packet(id="id_00")
    packet1 = Packet(id="id_01")

    document = Document(packets=[packet0, packet1])

    assert document.packets == [packet0, packet1]


def test_doc_repr():
    packet = Packet(id="id_00")
    expected_result = """[
    {
        "id": "id_00"
    }
]"""

    document = Document(packets=[packet])

    assert str(document) == expected_result


def test_doc_dumps():
    packet = Packet(id="id_00")
    expected_result = """[{"id":"id_00"}]"""

    document = Document(packets=[packet])

    assert document.dumps() == expected_result
