import datetime as dt
import json
import os

from czml3 import Document, Packet, Preamble
from czml3.enums import (
    HorizontalOrigins,
    InterpolationAlgorithms,
    LabelStyles,
    ReferenceFrames,
    VerticalOrigins,
)
from czml3.properties import Billboard, Clock, Label, Path, Position
from czml3.types import IntervalValue, Sequence, TimeInterval

TESTS_DIR = os.path.dirname(os.path.realpath(__file__))


def test_simple():
    with open(os.path.join(TESTS_DIR, "simple.czml"), "r") as fp:
        expected_result = json.load(fp)

    accesses_id = "9927edc4-e87a-4e1f-9b8b-0bfb3b05b227"
    start = dt.datetime(2012, 3, 15, 10, tzinfo=dt.timezone.utc)
    end = dt.datetime(2012, 3, 16, 10, tzinfo=dt.timezone.utc)

    simple = Document(
        [
            Preamble(
                name="simple",
                clock=IntervalValue(
                    start=start, end=end, value=Clock(currentTime=start, multiplier=60)
                ),
            ),
            Packet(id=accesses_id, name="Accesses", description="List of Accesses"),
            Packet(
                id="Satellite/Geoeye1-to-Satellite/ISS",
                name="Geoeye1 to ISS",
                parent=accesses_id,
            ),
            Packet(
                id="Facility/AGI-to-Satellite/ISS",
                name="AGI to ISS",
                parent=accesses_id,
            ),
            Packet(
                id="Facility/AGI-to-Satellite/Geoeye1/Sensor/Sensor",
                name="AGI to Sensor",
                parent=accesses_id,
                description="<h2>No accesses</h2>",
            ),
            Packet(
                id="AreaTarget/Pennsylvania",
                name="Pennsylvania",
                label=Label(
                    horizontalOrigin=HorizontalOrigins.LEFT,
                    show=True,
                    style=LabelStyles.FILL_AND_OUTLINE,
                    outlineWidth=2,
                    text="Pennsylvania",
                    verticalOrigin=VerticalOrigins.CENTER,
                ),
                position=Position(
                    cartesian=[1152255.80150063, -4694317.951340558, 4147335.9067563135]
                ),
            ),
            Packet(
                id="Facility/AGI",
                name="AGI",
                availability=TimeInterval(start=start, end=end),
                billboard=Billboard(
                    horizontalOrigin=HorizontalOrigins.CENTER,
                    image=(
                        "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/"
                        "9hAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAc"
                        "dvqGQAAACvSURBVDhPrZDRDcMgDAU9GqN0lIzijw6SUbJJygUeNQgSqepJTyHG91"
                        "LVVpwDdfxM3T9TSl1EXZvDwii471fivK73cBFFQNTT/d2KoGpfGOpSIkhUpgUMxq"
                        "9DFEsWv4IXhlyCnhBFnZcFEEuYqbiUlNwWgMTdrZ3JbQFoEVG53rd8ztG9aPJMnB"
                        "UQf/VFraBJeWnLS0RfjbKyLJA8FkT5seDYS1Qwyv8t0B/5C2ZmH2/eTGNNBgMmAA"
                        "AAAElFTkSuQmCC"
                    ),
                    scale=1.5,
                    show=True,
                    verticalOrigin=VerticalOrigins.CENTER,
                ),
                label=Label(
                    horizontalOrigin=HorizontalOrigins.LEFT,
                    outlineWidth=2,
                    show=True,
                    style=LabelStyles.FILL_AND_OUTLINE,
                    text="AGI",
                    verticalOrigin=VerticalOrigins.CENTER,
                ),
                position=Position(
                    cartesian=[
                        1216469.9357990976,
                        -4736121.71856379,
                        4081386.8856866374,
                    ]
                ),
            ),
            Packet(
                id="Satellite/Geoeye1",
                name="Geoeye1",
                availability=TimeInterval(start=start, end=end),
                billboard=Billboard(
                    horizontalOrigin=HorizontalOrigins.CENTER,
                    image=(
                        "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9"
                        "hAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdv"
                        "qGQAAADJSURBVDhPnZHRDcMgEEMZjVEYpaNklIzSEfLfD4qNnXAJSFWfhO7w2Zc0T"
                        "f9QG2rXrEzSUeZLOGm47WoH95x3Hl3jEgilvDgsOQUTqsNl68ezEwn1vae6lceSEE"
                        "YvvWNT/Rxc4CXQNGadho1NXoJ+9iaqc2xi2xbt23PJCDIB6TQjOC6Bho/sDy3fBQT"
                        "8PrVhibU7yBFcEPaRxOoeTwbwByCOYf9VGp1BYI1BA+EeHhmfzKbBoJEQwn1yzUZt"
                        "yspIQUha85MpkNIXB7GizqDEECsAAAAASUVORK5CYII="
                    ),
                    scale=1.5,
                    show=True,
                    verticalOrigin=VerticalOrigins.CENTER,
                ),
                label=Label(
                    horizontalOrigin=HorizontalOrigins.LEFT,
                    outlineWidth=2,
                    show=True,
                    style=LabelStyles.FILL_AND_OUTLINE,
                    text="Geoeye 1",
                    verticalOrigin=VerticalOrigins.CENTER,
                ),
                path=Path(
                    show=Sequence([IntervalValue(start=start, end=end, value=True)]),
                    width=1,
                    resolution=120,
                ),
                position=Position(
                    interpolationAlgorithm=InterpolationAlgorithms.LAGRANGE,
                    interpolationDegree=5,
                    referenceFrame=ReferenceFrames.INERTIAL,
                    epoch=start,
                ),
            ),
        ]
    )

    result = json.loads(simple.dumps())
    for ii, packet in enumerate(result):
        expected_packet = expected_result[ii]
        for key in packet:
            prop = packet[key]
            expected_prop = expected_packet[key]

            if isinstance(prop, dict):
                for sub_key in prop:
                    assert prop[sub_key] == expected_prop[sub_key]
            else:
                assert prop == expected_prop
