import pytest

from czml3.values import Cartesian3Value, Uri


@pytest.mark.parametrize("values", [[2, 2], [5, 5, 5, 5, 5]])
def test_bad_cartesian_raises_error(values):
    with pytest.raises(ValueError) as excinfo:
        Cartesian3Value(values=values)

    assert "Input values must have either 3 or N * 4 values" in excinfo.exconly()


def test_bad_uri_raises_error():
    with pytest.raises(ValueError) as excinfo:
        Uri(uri="a")

    assert "uri must be a URL or a data URI" in excinfo.exconly()
