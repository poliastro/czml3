import datetime as dt

import pytest
from dateutil.tz import tzoffset

from czml3.values import Cartesian3Value, TimeInterval, Uri


@pytest.mark.parametrize("values", [[2, 2], [5, 5, 5, 5, 5]])
def test_bad_cartesian_raises_error(values):
    with pytest.raises(ValueError) as excinfo:
        Cartesian3Value(values=values)

    assert "Input values must have either 3 or N * 4 values" in excinfo.exconly()


def test_bad_uri_raises_error():
    with pytest.raises(ValueError) as excinfo:
        Uri(uri="a")

    assert "uri must be a URL or a data URI" in excinfo.exconly()


def test_default_time_interval():
    expected_result = '"0000-00-00T00:00:00Z/9999-12-31T24:00:00Z"'
    time_interval = TimeInterval()

    assert repr(time_interval) == expected_result


def test_custom_time_interval():
    tz = tzoffset("UTC+02", dt.timedelta(hours=2))
    start = dt.datetime(2019, 1, 1, 12, 0, tzinfo=dt.timezone.utc)
    end = dt.datetime(2019, 9, 2, 23, 59, 59, tzinfo=tz)

    expected_result = '"2019-01-01T12:00:00Z/2019-09-02T21:59:59Z"'

    time_interval = TimeInterval(start=start, end=end)

    assert repr(time_interval) == expected_result
