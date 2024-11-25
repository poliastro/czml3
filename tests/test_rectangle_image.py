import base64
import os
import tempfile

import pytest

from czml3 import Document, Packet, Preamble
from czml3.properties import ImageMaterial, Material, Rectangle, RectangleCoordinates


@pytest.fixture
def image():
    filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "smiley.png")
    with open(filename, "rb") as fp:
        data = fp.read()

    base64_data = base64.b64encode(data)
    return base64_data.decode("utf-8")


def test_rectangle_coordinates_invalid_if_nothing_given():
    with pytest.raises(TypeError) as excinfo:
        RectangleCoordinates()

    assert "One of wsen or wsenDegrees must be given" in excinfo.exconly()


def test_packet_rectangles(image):
    wsen = [20, 40, 21, 41]

    expected_result = """{{
    "id": "id_00",
    "rectangle": {{
        "coordinates": {{
            "wsenDegrees": [
                {},
                {},
                {},
                {}
            ]
        }},
        "fill": true,
        "material": {{
            "image": {{
                "image": "data:image/png;base64,{}",
                "transparent": true
            }}
        }}
    }}
}}""".format(*wsen, image)

    rectangle_packet = Packet(
        id="id_00",
        rectangle=Rectangle(
            coordinates=RectangleCoordinates(wsenDegrees=wsen),
            fill=True,
            material=Material(
                image=ImageMaterial(
                    transparent=True,
                    repeat=None,
                    image="data:image/png;base64," + image,
                ),
            ),
        ),
    )

    assert str(rectangle_packet) == expected_result


def test_make_czml_png_rectangle_file(image):
    rectangle_packet = Packet(
        id="id_00",
        rectangle=Rectangle(
            coordinates=RectangleCoordinates(wsenDegrees=[20, 40, 21, 41]),
            fill=True,
            material=Material(
                image=ImageMaterial(
                    transparent=True,
                    repeat=None,
                    image="data:image/png;base64," + image,
                ),
            ),
        ),
    )

    with tempfile.NamedTemporaryFile(mode="w", suffix=".czml") as out_file:
        out_file.write(str(Document(packets=[Preamble(), rectangle_packet])))
        exists = os.path.isfile(out_file.name)

        # TODO: Should we be testing something else?
        assert exists
