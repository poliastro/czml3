def test_example0():
    from czml3 import Document, Packet, Preamble
    from czml3.properties import (
        Box,
        BoxDimensions,
        Color,
        Material,
        Position,
        SolidColorMaterial,
    )
    from czml3.types import Cartesian3Value

    expected_result = """[
    {
        "id": "document",
        "version": "1.0",
        "name": "box"
    },
    {
        "id": "my_id",
        "position": {
            "cartographicDegrees": [
                -114.0,
                40.0,
                300000.0
            ]
        },
        "box": {
            "dimensions": {
                "cartesian": [
                    400000.0,
                    300000.0,
                    500000.0
                ]
            },
            "material": {
                "solidColor": {
                    "color": {
                        "rgba": [
                            0.0,
                            0.0,
                            255.0,
                            255.0
                        ]
                    }
                }
            }
        }
    }
]"""

    packet_box = Packet(
        id="my_id",  # fixing id here to ensure test passes
        position=Position(cartographicDegrees=[-114.0, 40.0, 300000.0]),
        box=Box(
            dimensions=BoxDimensions(
                cartesian=Cartesian3Value(values=[400000.0, 300000.0, 500000.0])
            ),
            material=Material(
                solidColor=SolidColorMaterial(color=Color(rgba=[0, 0, 255, 255]))
            ),
        ),
    )
    doc = Document(packets=[Preamble(name="box"), packet_box])
    assert str(doc) == expected_result


def test_example1():
    import numpy as np

    from czml3.properties import Position

    expected_result = """{
    "cartographicDegrees": [
        -114.0,
        40.0,
        300000.0
    ]
}"""
    p = Position(cartographicDegrees=np.array([-114, 40, 300000], dtype=int))  # type: ignore
    assert str(p) == expected_result
