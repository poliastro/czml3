from io import StringIO
from uuid import UUID

import pytest
from czml3 import CZML_VERSION, Packet, Preamble
from czml3.enums import InterpolationAlgorithms, ReferenceFrames
from czml3.properties import (
    Billboard,
    Color,
    Ellipsoid,
    EllipsoidRadii,
    Label,
    Material,
    Point,
    Polygon,
    Polyline,
    PolylineArrow,
    PolylineArrowMaterial,
    PolylineDash,
    PolylineDashMaterial,
    PolylineGlow,
    PolylineGlowMaterial,
    PolylineMaterial,
    PolylineOutline,
    PolylineOutlineMaterial,
    Position,
    PositionList,
    SolidColorMaterial,
)
from czml3.types import Cartesian3Value, StringValue


def test_preamble_has_proper_id_and_expected_version():
    preamble = Preamble()

    assert preamble.id == "document"
    assert preamble.version == CZML_VERSION


def test_preamble_has_given_name():
    expected_name = "document_00"
    preamble = Preamble(name=expected_name)

    assert preamble.name == expected_name


def test_preamble_has_given_description():
    expected_description = "czml document description"
    preamble = Preamble(description=expected_description)

    assert preamble.description == expected_description


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

    assert str(packet) == expected_result


def test_packet_label():
    expected_result = """{
    "id": "0",
    "label": {
        "show": true,
        "font": "20px sans-serif",
        "style": "FILL",
        "fillColor": {
            "rgbaf": [
                0.2,
                0.3,
                0.4,
                1.0
            ]
        },
        "outlineColor": {
            "rgba": [
                0,
                233,
                255,
                2
            ]
        },
        "outlineWidth": 2.0
    }
}"""
    packet = Packet(
        id="0",
        label=Label(
            font="20px sans-serif",
            fillColor=Color.from_list([0.2, 0.3, 0.4]),
            outlineColor=Color.from_list([0, 233, 255, 2]),
            outlineWidth=2.0,
        ),
    )

    assert str(packet) == expected_result


def test_packet_repr_id_name():
    expected_result = """{
    "id": "id_00",
    "name": "Test Packet"
}"""
    packet = Packet(id="id_00", name="Test Packet")

    assert str(packet) == expected_result


def test_packet_with_delete_has_nothing_else():
    expected_result = """{
    "id": "id_00",
    "delete": true
}"""
    packet = Packet(id="id_00", delete=True, name="No Name In Packet")

    assert str(packet) == expected_result


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

    assert str(packet) == expected_result


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

    assert str(packet) == expected_result


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

    assert str(packet) == expected_result


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

    assert str(packet) == expected_result


def test_packet_description():
    expected_result = """{
    "id": "id_00",
    "name": "Name",
    "description": "<strong>Description</strong>"
}"""
    string = "<strong>Description</strong>"
    packet_str = Packet(id="id_00", name="Name", description=string)
    packet_val = Packet(id="id_00", name="Name", description=StringValue(string=string))

    assert str(packet_str) == str(packet_val) == expected_result


def test_packet_custom_properties():
    expected_result = """{
    "id": "id_00",
    "properties": {
        "a": false,
        "b": 1,
        "c": "C",
        "ellipsoid": {
            "radii": {
                "cartesian": [
                    6378137,
                    6378137,
                    6356752.31414
                ]
            }
        }
    }
}"""
    prop_dict = {
        "a": False,
        "b": 1,
        "c": "C",
        "ellipsoid": Ellipsoid(
            radii=EllipsoidRadii(
                cartesian=Cartesian3Value(values=[6378137, 6378137, 6356752.314140])
            )
        ),
    }

    packet = Packet(id="id_00", properties=prop_dict)

    assert str(packet) == expected_result


def test_packet_billboard():
    expected_result = """{
    "id": "id_00",
    "billboard": {
        "image": "file://image.png"
    }
}"""
    packet = Packet(id="id_00", billboard=Billboard(image="file://image.png"))

    assert str(packet) == expected_result


def test_packet_point():
    expected_result = """{
    "id": "id_00",
    "point": {
        "color": {
            "rgba": [
                255,
                0,
                0,
                255
            ]
        }
    }
}"""
    packet = Packet(id="id_00", point=Point(color=Color.from_list([255, 0, 0, 255])))

    assert str(packet) == expected_result


def test_packet_polyline():
    expected_result = """{
    "id": "id_00",
    "polyline": {
        "positions": {
            "cartographicDegrees": [
                -75,
                43,
                500000,
                -125,
                43,
                500000
            ]
        },
        "material": {
            "solidColor": {
                "color": {
                    "rgba": [
                        255,
                        0,
                        0,
                        255
                    ]
                }
            }
        }
    }
}"""
    packet = Packet(
        id="id_00",
        polyline=Polyline(
            positions=PositionList(
                cartographicDegrees=[-75, 43, 500000, -125, 43, 500000]
            ),
            material=PolylineMaterial(
                solidColor=SolidColorMaterial.from_list([255, 0, 0, 255])
            ),
        ),
    )

    assert str(packet) == expected_result


def test_packet_polyline_outline():
    expected_result = """{
    "id": "id_00",
    "polyline": {
        "positions": {
            "cartographicDegrees": [
                -75,
                43,
                500000,
                -125,
                43,
                500000
            ]
        },
        "material": {
            "polylineOutline": {
                "color": {
                    "rgba": [
                        255,
                        0,
                        0,
                        255
                    ]
                },
                "outlineColor": {
                    "rgba": [
                        255,
                        0,
                        0,
                        255
                    ]
                },
                "outlineWidth": 2
            }
        }
    }
}"""
    packet = Packet(
        id="id_00",
        polyline=Polyline(
            positions=PositionList(
                cartographicDegrees=[-75, 43, 500000, -125, 43, 500000]
            ),
            material=PolylineOutlineMaterial(
                polylineOutline=PolylineOutline(
                    color=Color.from_list([255, 0, 0, 255]),
                    outlineColor=Color.from_list([255, 0, 0, 255]),
                    outlineWidth=2,
                )
            ),
        ),
    )

    assert str(packet) == expected_result


# TODO:
def test_packet_polyline_glow():
    expected_result = """{
    "id": "id_00",
    "polyline": {
        "positions": {
            "cartographicDegrees": [
                -75,
                43,
                500000,
                -125,
                43,
                500000
            ]
        },
        "material": {
            "polylineGlow": {
                "color": {
                    "rgba": [
                        255,
                        0,
                        0,
                        255
                    ]
                },
                "glowPower": 0.2,
                "taperPower": 0.5
            }
        }
    }
}"""
    packet = Packet(
        id="id_00",
        polyline=Polyline(
            positions=PositionList(
                cartographicDegrees=[-75, 43, 500000, -125, 43, 500000]
            ),
            material=PolylineGlowMaterial(
                polylineGlow=PolylineGlow(
                    color=Color.from_list([255, 0, 0, 255]),
                    glowPower=0.2,
                    taperPower=0.5,
                )
            ),
        ),
    )

    assert str(packet) == expected_result


def test_packet_polyline_arrow():
    expected_result = """{
    "id": "id_00",
    "polyline": {
        "positions": {
            "cartographicDegrees": [
                -75,
                43,
                500000,
                -125,
                43,
                500000
            ]
        },
        "material": {
            "polylineArrow": {
                "color": {
                    "rgba": [
                        255,
                        0,
                        0,
                        255
                    ]
                }
            }
        }
    }
}"""
    packet = Packet(
        id="id_00",
        polyline=Polyline(
            positions=PositionList(
                cartographicDegrees=[-75, 43, 500000, -125, 43, 500000]
            ),
            material=PolylineArrowMaterial(
                polylineArrow=PolylineArrow(color=Color.from_list([255, 0, 0, 255]))
            ),
        ),
    )

    assert str(packet) == expected_result


def test_packet_polyline_dashed():
    expected_result = """{
    "id": "id_00",
    "polyline": {
        "positions": {
            "cartographicDegrees": [
                -75,
                43,
                500000,
                -125,
                43,
                500000
            ]
        },
        "material": {
            "polylineDash": {
                "color": {
                    "rgba": [
                        255,
                        0,
                        0,
                        255
                    ]
                }
            }
        }
    }
}"""
    packet = Packet(
        id="id_00",
        polyline=Polyline(
            positions=PositionList(
                cartographicDegrees=[-75, 43, 500000, -125, 43, 500000]
            ),
            material=PolylineDashMaterial(
                polylineDash=PolylineDash(color=Color.from_list([255, 0, 0, 255]))
            ),
        ),
    )

    assert str(packet) == expected_result


def test_packet_polygon():
    expected_result = """{
    "id": "id_00",
    "polygon": {
        "positions": {
            "cartographicDegrees": [
                -115.0,
                37.0,
                0,
                -115.0,
                32.0,
                0,
                -107.0,
                33.0,
                0,
                -102.0,
                31.0,
                0,
                -102.0,
                35.0,
                0
            ]
        },
        "granularity": 1.0,
        "material": {
            "solidColor": {
                "color": {
                    "rgba": [
                        255,
                        0,
                        0,
                        255
                    ]
                }
            }
        }
    }
}"""
    packet = Packet(
        id="id_00",
        polygon=Polygon(
            positions=PositionList(
                cartographicDegrees=[
                    -115.0,
                    37.0,
                    0,
                    -115.0,
                    32.0,
                    0,
                    -107.0,
                    33.0,
                    0,
                    -102.0,
                    31.0,
                    0,
                    -102.0,
                    35.0,
                    0,
                ]
            ),
            granularity=1.0,
            material=Material(solidColor=SolidColorMaterial.from_list([255, 0, 0])),
        ),
    )

    assert str(packet) == expected_result
