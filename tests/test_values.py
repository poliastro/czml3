import pytest

from czml3.values import Cartesian3Value


@pytest.mark.parametrize("values", [[2, 2], [5, 5, 5, 5, 5]])
def test_bad_cartesian_raises_error(values):
    with pytest.raises(ValueError) as excinfo:
        Cartesian3Value(values)

    assert "Input values must have either 3 or N * 4 values" in excinfo.exconly()
