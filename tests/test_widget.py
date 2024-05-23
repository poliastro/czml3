import pytest
from czml3.widget import CZMLWidget


def test_no_input_makes_empty_document():
    widget = CZMLWidget()

    assert len(widget.document.packets) == 1


@pytest.mark.parametrize("cesium_version", ["1.62", "1.99"])
def test_version(cesium_version):
    widget = CZMLWidget(cesium_version=cesium_version)

    assert cesium_version in widget.build_script()


def test_to_html_contains_script():
    widget = CZMLWidget()

    assert widget.build_script() in widget.to_html()
