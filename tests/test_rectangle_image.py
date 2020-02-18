import base64
import os
import tempfile

import pytest

from czml3 import Document, Packet, Preamble
from czml3.properties import (
    CartographicRectangle,
    ImageMaterial,
    Material,
    RectangleCoordinates,
)

TESTS_DIR = os.path.dirname(os.path.realpath(__file__))
DEFAULT_TEST_FILE = ("smiley.png", [20, 40, 21, 41])


def filename_content_as_base64(filename):
    data = open(filename, "br").read()
    base64_data = base64.b64encode(data)
    return base64_data.decode("utf-8")


def make_image_rectangle_packet(wsen, base64_str):
    packet = Packet(
        id="id_00",
        rectangle=CartographicRectangle(
            coordinates=RectangleCoordinates(wsenDegrees=wsen),
            fill=True,
            material=Material(
                image=ImageMaterial(
                    transparent=True,
                    repeat=None,
                    image="data:image/png;base64," + base64_str,
                ),
            ),
        ),
    )
    return packet


@pytest.mark.parametrize("filename, wsen", [DEFAULT_TEST_FILE])
def test_packet_rectangles(filename, wsen):
    filename = os.path.join(TESTS_DIR, filename)
    base64_str = filename_content_as_base64(filename)
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
}}""".format(
        *wsen, base64_str
    )

    packet = make_image_rectangle_packet(wsen, base64_str)

    assert repr(packet) == expected_result


def save_czml_to_file(packet, out_filename):
    czml_doc = Document([Preamble(), packet])
    with open(out_filename, "w") as f:
        print(czml_doc, file=f)


def get_named_temporary_filenme(suffix="", dir_name=""):
    filename = next(tempfile._get_candidate_names()) + suffix
    if dir_name is None:
        return filename
    else:
        if dir_name == "":
            dir_name = tempfile._get_default_tempdir()
        return os.path.join(dir_name, filename)


@pytest.mark.parametrize("filename, wsen, remove_output", [(*DEFAULT_TEST_FILE, True)])
def test_make_czml_png_rectangle_file(filename, wsen, remove_output):
    filename = os.path.join(TESTS_DIR, filename)
    base64_str = filename_content_as_base64(filename)
    packet = make_image_rectangle_packet(wsen, base64_str)
    out_filename = get_named_temporary_filenme(
        "_" + os.path.basename(filename) + ".czml"
    )
    save_czml_to_file(packet, out_filename)
    exists = os.path.isfile(out_filename)
    if remove_output:
        os.remove(out_filename)
    assert exists
