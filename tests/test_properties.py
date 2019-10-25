import datetime as dt

import pytest

from czml3.properties import (
    ArcType,
    Box,
    BoxDimensions,
    CheckerboardMaterial,
    ClassificationType,
    Color,
    DistanceDisplayCondition,
    EyeOffset,
    GridMaterial,
    HeightReference,
    ImageMaterial,
    Material,
    NearFarScalar,
    Point,
    Polyline,
    PolylineMaterial,
    Position,
    PositionList,
    ShadowMode,
    SolidColorMaterial,
    StripeMaterial,
)
from czml3.types import (
    ArcTypeValue,
    Cartesian3Value,
    CartographicDegreesListValue,
    ClassificationTypeValue,
    DistanceDisplayConditionValue,
    HeightReferenceValue,
    IntervalValue,
    NearFarScalarValue,
    Sequence,
    ShadowModeValue,
    Uri,
)


def test_box():
    expected_result = """{
    "show": true,
    "dimensions": {
        "cartesian": [
            5,
            6,
            3
        ]
    }
}"""

    box = Box(
        show=True, dimensions=BoxDimensions(cartesian=Cartesian3Value(values=[5, 6, 3]))
    )
    assert repr(box) == expected_result


def test_eyeOffset():
    expected_result = """{
    "cartesian": [
        1,
        2,
        3
    ]
}"""

    eyeOffset = EyeOffset(cartesian=Cartesian3Value(values=[1, 2, 3]))
    assert repr(eyeOffset) == expected_result


def test_point():
    expected_result = """{
    "show": true,
    "pixelSize": 10,
    "scaleByDistance": {
        "nearFarScalar": [
            150,
            2.0,
            15000000,
            0.5
        ]
    },
    "disableDepthTestDistance": 1.2
}"""

    pnt = Point(
        show=True,
        pixelSize=10,
        scaleByDistance=NearFarScalar(
            nearFarScalar=NearFarScalarValue(values=[150, 2.0, 15000000, 0.5])
        ),
        disableDepthTestDistance=1.2,
    )
    assert repr(pnt) == expected_result


def test_arc_type():
    expected_result = """{
    "arcType": "NONE"
}"""
    arc_type = ArcType(arcType=ArcTypeValue(string="NONE"))
    assert repr(arc_type) == expected_result


def test_shadow_mode():
    expected_result = """{
    "shadowMode": "ENABLED"
}"""
    shadow_mode = ShadowMode(shadowMode=ShadowModeValue(string="ENABLED"))
    assert repr(shadow_mode) == expected_result


def test_polyline():
    expected_result = """{
    "positions": {
        "cartographicDegrees": [
            20,
            30,
            10
        ]
    },
    "arcType": {
        "arcType": "GEODESIC"
    },
    "distanceDisplayCondition": {
        "distanceDisplayCondition": [
            14,
            81
        ]
    },
    "classificationType": {
        "classificationType": "CESIUM_3D_TILE"
    }
}"""
    pol = Polyline(
        positions=PositionList(
            cartographicDegrees=CartographicDegreesListValue(values=[20, 30, 10])
        ),
        arcType=ArcType(arcType="GEODESIC"),
        distanceDisplayCondition=DistanceDisplayCondition(
            distanceDisplayCondition=DistanceDisplayConditionValue(values=[14, 81])
        ),
        classificationType=ClassificationType(
            classificationType=ClassificationTypeValue(string="CESIUM_3D_TILE")
        ),
    )
    assert repr(pol) == expected_result


def test_material_solid_color():
    expected_result = """{
    "solidColor": {
        "color": {
            "rgba": [
                200,
                100,
                30,
                255
            ]
        }
    }
}"""
    mat = Material(solidColor=SolidColorMaterial(color=Color(rgba=[200, 100, 30, 255])))

    assert repr(mat) == expected_result

    pol_mat = PolylineMaterial(
        solidColor=SolidColorMaterial(color=Color(rgba=[200, 100, 30, 255]))
    )
    assert repr(pol_mat) == expected_result


def test_material_image():
    expected_result = """{
    "image": {
        "image": "https://site.com/image.png",
        "repeat": [
            2,
            2
        ],
        "color": {
            "rgba": [
                200,
                100,
                30,
                255
            ]
        },
        "transparent": false
    }
}"""

    mat = Material(
        image=ImageMaterial(
            image=Uri(uri="https://site.com/image.png"),
            repeat=[2, 2],
            color=Color(rgba=[200, 100, 30, 255]),
        )
    )
    assert repr(mat) == expected_result

    pol_mat = PolylineMaterial(
        image=ImageMaterial(
            image=Uri(uri="https://site.com/image.png"),
            repeat=[2, 2],
            color=Color(rgba=[200, 100, 30, 255]),
        )
    )
    assert repr(pol_mat) == expected_result


def test_material_grid():
    expected_result = """{
    "color": {
        "rgba": [
            20,
            20,
            30,
            255
        ]
    },
    "cellAlpha": 1.0,
    "lineCount": [
        16,
        16
    ],
    "lineThickness": [
        2.0,
        2.0
    ],
    "lineOffset": [
        0.3,
        0.4
    ]
}"""

    pol_mat = GridMaterial(
        color=Color(rgba=[20, 20, 30, 255]),
        cellAlpha=1.0,
        lineCount=[16, 16],
        lineThickness=[2.0, 2.0],
        lineOffset=[0.3, 0.4],
    )
    assert repr(pol_mat) == expected_result


def test_material_stripe():
    expected_result = """{
    "orientation": "HORIZONTAL",
    "evenColor": {
        "rgba": [
            0,
            0,
            0,
            255
        ]
    },
    "oddColor": {
        "rgba": [
            255,
            255,
            255,
            255
        ]
    },
    "offset": 0.3,
    "repeat": 4
}"""

    pol_mat = StripeMaterial(
        evenColor=Color(rgba=[0, 0, 0, 255]),
        oddColor=Color(rgba=[255, 255, 255, 255]),
        offset=0.3,
        repeat=4,
    )
    assert repr(pol_mat) == expected_result


def test_material_checkerboard():
    expected_result = """{
    "evenColor": {
        "rgba": [
            0,
            0,
            0,
            255
        ]
    },
    "oddColor": {
        "rgba": [
            255,
            255,
            255,
            255
        ]
    },
    "repeat": 4
}"""

    pol_mat = CheckerboardMaterial(
        evenColor=Color(rgba=[0, 0, 0, 255]),
        oddColor=Color(rgba=[255, 255, 255, 255]),
        repeat=4,
    )
    assert repr(pol_mat) == expected_result


def test_position_has_delete():
    pos = Position(delete=True, cartesian=[])

    assert pos.delete


def test_position_no_values_raises_error():
    with pytest.raises(ValueError) as exc:
        Position()

    assert (
        "One of cartesian, cartographicDegrees or cartographicRadians must be given"
        in exc.exconly()
    )


def test_position_with_delete_has_nothing_else():
    expected_result = """{
    "delete": true
}"""
    pos_list = Position(delete=True, cartesian=[1, 2, 3])
    pos_val = Position(delete=True, cartesian=Cartesian3Value(values=[1, 2, 3]))

    assert repr(pos_list) == repr(pos_val) == expected_result


def test_position_has_given_epoch():
    expected_epoch = dt.datetime(2019, 6, 11, 12, 26, 58, tzinfo=dt.timezone.utc)

    pos = Position(epoch=expected_epoch, cartesian=[])

    assert pos.epoch == expected_epoch


def test_position_renders_epoch():
    expected_result = """{
    "epoch": "2019-03-20T12:00:00Z",
    "cartesian": []
}"""
    pos = Position(
        epoch=dt.datetime(2019, 3, 20, 12, tzinfo=dt.timezone.utc), cartesian=[]
    )

    assert repr(pos) == expected_result


def test_position_cartographic_degrees():
    expected_result = """{
    "cartographicDegrees": [
        10.0,
        20.0,
        0.0
    ]
}"""
    pos = Position(cartographicDegrees=[10.0, 20.0, 0.0])

    assert repr(pos) == expected_result


def test_single_interval_value():
    expected_result = """{
    "interval": "2019-01-01T00:00:00Z/2019-01-02T00:00:00Z",
    "boolean": true
}"""

    start = dt.datetime(2019, 1, 1, tzinfo=dt.timezone.utc)
    end = dt.datetime(2019, 1, 2, tzinfo=dt.timezone.utc)

    prop = IntervalValue(start=start, end=end, value=True)

    assert repr(prop) == expected_result


def test_multiple_interval_value():
    expected_result = """[
    {
        "interval": "2019-01-01T00:00:00Z/2019-01-02T00:00:00Z",
        "boolean": true
    },
    {
        "interval": "2019-01-02T00:00:00Z/2019-01-03T00:00:00Z",
        "boolean": false
    }
]"""

    start0 = dt.datetime(2019, 1, 1, tzinfo=dt.timezone.utc)
    end0 = start1 = dt.datetime(2019, 1, 2, tzinfo=dt.timezone.utc)
    end1 = dt.datetime(2019, 1, 3, tzinfo=dt.timezone.utc)

    prop = Sequence(
        [
            IntervalValue(start=start0, end=end0, value=True),
            IntervalValue(start=start1, end=end1, value=False),
        ]
    )

    assert repr(prop) == expected_result


def test_height_reference():
    expected_result = """{
    "heightReference": "CLAMP_TO_GROUND"
}"""
    height_reference = HeightReference(
        heightReference=HeightReferenceValue(string="CLAMP_TO_GROUND")
    )

    assert repr(height_reference) == expected_result
