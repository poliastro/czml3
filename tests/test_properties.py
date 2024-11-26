import datetime as dt

import pytest
from pydantic import ValidationError

from czml3.enums import (
    ArcTypes,
    ClassificationTypes,
    ColorBlendModes,
    CornerTypes,
    HeightReferences,
    ShadowModes,
)
from czml3.properties import (
    ArcType,
    Box,
    BoxDimensions,
    CheckerboardMaterial,
    ClassificationType,
    Color,
    ColorBlendMode,
    CornerType,
    DistanceDisplayCondition,
    Ellipsoid,
    EllipsoidRadii,
    EyeOffset,
    GridMaterial,
    HeightReference,
    ImageMaterial,
    Label,
    Material,
    Model,
    NearFarScalar,
    Orientation,
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
    PositionListOfLists,
    RectangleCoordinates,
    ShadowMode,
    SolidColorMaterial,
    StripeMaterial,
    Tileset,
    Uri,
    ViewFrom,
)
from czml3.types import (
    Cartesian2Value,
    Cartesian3Value,
    CartographicDegreesListValue,
    DistanceDisplayConditionValue,
    IntervalValue,
    NearFarScalarValue,
    Sequence,
    TimeInterval,
    UnitQuaternionValue,
    format_datetime_like,
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
    assert str(box) == expected_result


def test_eyeOffset():
    expected_result = """{
    "cartesian": [
        1,
        2,
        3
    ]
}"""

    eyeOffset = EyeOffset(cartesian=Cartesian3Value(values=[1, 2, 3]))
    assert str(eyeOffset) == expected_result


def test_point():
    expected_result = """{
    "show": true,
    "pixelSize": 10,
    "scaleByDistance": {
        "nearFarScalar": [
            150.0,
            2.0,
            15000000.0,
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
    assert str(pnt) == expected_result


def test_arc_type():
    expected_result = """{
    "arcType": "NONE"
}"""
    arc_type = ArcType(arcType=ArcTypes.NONE)
    assert str(arc_type) == expected_result


def test_shadow_mode():
    expected_result = """{
    "shadowMode": "ENABLED"
}"""
    shadow_mode = ShadowMode(shadowMode=ShadowModes.ENABLED)
    assert str(shadow_mode) == expected_result


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
            classificationType=ClassificationTypes.CESIUM_3D_TILE
        ),
    )
    assert str(pol) == expected_result


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
    mat = Material(solidColor=SolidColorMaterial(color=Color(rgba=[200, 100, 30])))

    assert str(mat) == expected_result

    pol_mat = PolylineMaterial(
        solidColor=SolidColorMaterial(color=Color(rgba=[200, 100, 30]))
    )
    assert str(pol_mat) == expected_result


def test_arrowmaterial_color():
    expected_result = """{
    "polylineArrow": {
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
    pamat = PolylineArrowMaterial(
        polylineArrow=PolylineArrow(color=Color(rgba=[200, 100, 30, 255])),
    )

    assert str(pamat) == expected_result


def test_dashmaterial_colors():
    expected_result = """{
    "polylineDash": {
        "color": {
            "rgba": [
                200,
                100,
                30,
                255
            ]
        },
        "gapColor": {
            "rgba": [
                100,
                200,
                0,
                255
            ]
        },
        "dashLength": 16,
        "dashPattern": 255
    }
}"""
    dashmat = PolylineDashMaterial(
        polylineDash=PolylineDash(
            color=Color(rgba=[200, 100, 30, 255]),
            gapColor=Color(rgba=[100, 200, 0, 255]),
            dashLength=16,
            dashPattern=255,
        ),
    )

    assert str(dashmat) == expected_result


def test_glowmaterial_color():
    expected_result = """{
    "polylineGlow": {
        "color": {
            "rgba": [
                200,
                100,
                30,
                255
            ]
        },
        "glowPower": 0.7,
        "taperPower": 0.3
    }
}"""
    glowmat = PolylineGlowMaterial(
        polylineGlow=PolylineGlow(
            color=Color(rgba=[200, 100, 30, 255]), glowPower=0.7, taperPower=0.3
        )
    )
    assert str(glowmat) == expected_result


def test_outline_material_colors():
    expected_result = """{
    "polylineOutline": {
        "color": {
            "rgba": [
                200,
                100,
                30,
                255
            ]
        },
        "outlineColor": {
            "rgba": [
                100,
                200,
                0,
                255
            ]
        },
        "outlineWidth": 3
    }
}"""
    omat = PolylineOutlineMaterial(
        polylineOutline=PolylineOutline(
            color=Color(rgba=[200, 100, 30, 255]),
            outlineColor=Color(rgba=[100, 200, 0, 255]),
            outlineWidth=3,
        )
    )
    assert str(omat) == expected_result


def test_positionlist_epoch():
    expected_result = """{
    "epoch": "2019-06-11T12:26:58.000000Z",
    "cartographicDegrees": [
        200,
        100,
        30
    ]
}"""
    p = PositionList(
        epoch=dt.datetime(2019, 6, 11, 12, 26, 58, tzinfo=dt.timezone.utc),
        cartographicDegrees=[200, 100, 30],
    )
    assert str(p) == expected_result


def test_colors_rgba():
    Color(rgba=[255, 204, 0, 55])
    Color(rgba=[255, 204, 55])
    Color(rgba=[0.5, 0.6, 0.2])
    Color(rgba="0xFF0000")
    Color(rgba="0xFFFFFFFF")
    Color(rgba="0xFF3223")
    Color(rgba="0xFF322332")
    Color(rgba="#FF3223")
    Color(rgba="#FF322332")
    Color(rgba=[255, 204, 55])
    Color(rgba=[255, 204, 55, 255])
    Color(rgba=[0.127568, 0.566949, 0.550556])
    Color(rgba=[0.127568, 0.566949, 0.550556, 1.0])


def test_colors_rgbaf():
    Color(rgbaf=[255, 204, 0, 55])
    Color(rgbaf=[255, 204, 55])
    Color(rgbaf="0xFF3223")
    Color(rgbaf="0xFF322332")
    Color(rgbaf="#FF3223")
    Color(rgbaf="#FF322332")
    Color(rgbaf=[255, 204, 55])
    Color(rgbaf=[255, 204, 55, 255])
    Color(rgbaf=[0.127568, 0.566949, 0.550556])
    Color(rgbaf=[0.127568, 0.566949, 0.550556, 1.0])


def test_color_invalid_colors_rgba():
    with pytest.raises(TypeError):
        Color(rgba=[256, 204, 0, 55])
    with pytest.raises(TypeError):
        Color(rgba=[-204, 0, 55])
    with pytest.raises(TypeError):
        Color(rgba=[255, 204])
    with pytest.raises(TypeError):
        Color(rgba=[255, 232, 300])
    with pytest.raises(TypeError):
        Color(rgba="0xFF3223324")
    with pytest.raises(TypeError):
        Color(rgba=-3)  # type: ignore
    with pytest.raises(ValidationError):
        Color(rgba="totally valid color")
    with pytest.raises(TypeError):
        Color(rgba="#FF322332432")
    with pytest.raises(TypeError):
        Color(rgba=[255, 204, 55, 255, 42])
    with pytest.raises(TypeError):
        Color(rgba=[0.127568, 0.566949, 0.550556, 1.0, 3.0])


def test_color_invalid_colors_rgbaf():
    with pytest.raises(TypeError):
        Color(rgbaf=[256, 204, 0, 55])
    with pytest.raises(TypeError):
        Color(rgbaf=[-204, 0, 55])
    with pytest.raises(TypeError):
        Color(rgbaf=[255, 204])
    with pytest.raises(TypeError):
        Color(rgbaf=[255, 232, 300])
    with pytest.raises(TypeError):
        Color(rgbaf="0xFF3223324")
    with pytest.raises(TypeError):
        Color(rgbaf=-3)  # type: ignore
    with pytest.raises(ValidationError):
        Color(rgbaf="totally valid color")
    with pytest.raises(TypeError):
        Color(rgbaf="#FF322332432")
    with pytest.raises(TypeError):
        Color(rgbaf=[255, 204, 55, 255, 42])
    with pytest.raises(TypeError):
        Color(rgbaf=[0.127568, 0.566949, 0.550556, 1.0, 3.0])


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
        }
    }
}"""

    mat = Material(
        image=ImageMaterial(
            image=Uri(uri="https://site.com/image.png"),
            repeat=[2, 2],
            color=Color(rgba=[200, 100, 30]),
        )
    )
    assert str(mat) == expected_result


def test_material_image_uri():
    expected_result = """{
    "image": {
        "image": "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7",
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
        }
    }
}"""

    mat = Material(
        image=ImageMaterial(
            image=Uri(
                uri="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"
            ),
            repeat=[2, 2],
            color=Color(rgba=[200, 100, 30]),
        )
    )
    assert str(mat) == expected_result


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
        color=Color(rgba=[20, 20, 30]),
        cellAlpha=1.0,
        lineCount=[16, 16],
        lineThickness=[2.0, 2.0],
        lineOffset=[0.3, 0.4],
    )
    assert str(pol_mat) == expected_result


def test_nested_delete():
    expected_result = """{
    "color": {
        "delete": true
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
        color=Color(rgba=[20, 20, 30], delete=True),
        cellAlpha=1.0,
        lineCount=[16, 16],
        lineThickness=[2.0, 2.0],
        lineOffset=[0.3, 0.4],
    )
    assert str(pol_mat) == expected_result


def test_material_stripe():
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
    "offset": 0.3,
    "repeat": 4
}"""

    pol_mat = StripeMaterial(
        evenColor=Color(rgba=[0, 0, 0]),
        oddColor=Color(rgba=[255, 255, 255]),
        offset=0.3,
        repeat=4,
    )
    assert str(pol_mat) == expected_result


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
        evenColor=Color(rgba=[0, 0, 0]),
        oddColor=Color(rgba=[255, 255, 255]),
        repeat=4,
    )
    assert str(pol_mat) == expected_result


def test_position_has_delete():
    pos = Position(delete=True, cartesian=[])

    assert pos.delete


def test_position_no_values_raises_error():
    with pytest.raises(TypeError) as exc:
        Position()

    assert (
        "One of cartesian, cartographicDegrees, cartographicRadians or reference must be given"
        in exc.exconly()
    )


def test_position_with_delete_has_nothing_else():
    expected_result = """{
    "delete": true
}"""
    pos_list = Position(delete=True, cartesian=[1, 2, 3])
    pos_val = Position(delete=True, cartesian=Cartesian3Value(values=[1, 2, 3]))

    assert str(pos_list) == str(pos_val) == expected_result


def test_position_has_given_epoch():
    expected_epoch = format_datetime_like(
        dt.datetime(2019, 6, 11, 12, 26, 58, tzinfo=dt.timezone.utc)
    )

    pos = Position(epoch=expected_epoch, cartesian=[])

    assert pos.epoch == expected_epoch


def test_positionlist_has_given_epoch():
    expected_epoch = format_datetime_like(
        dt.datetime(2019, 6, 11, 12, 26, 58, tzinfo=dt.timezone.utc)
    )

    pos = PositionList(epoch=expected_epoch, cartesian=[])

    assert pos.epoch == expected_epoch


def test_position_renders_epoch():
    expected_result = """{
    "epoch": "2019-03-20T12:00:00.000000Z",
    "cartesian": []
}"""
    pos = Position(
        epoch=dt.datetime(2019, 3, 20, 12, tzinfo=dt.timezone.utc), cartesian=[]
    )

    assert str(pos) == expected_result


def test_position_cartographic_degrees():
    expected_result = """{
    "cartographicDegrees": [
        10.0,
        20.0,
        0.0
    ]
}"""
    pos = Position(cartographicDegrees=[10.0, 20.0, 0.0])

    assert str(pos) == expected_result


def test_position_reference():
    expected_result = """{
    "cartesian": [
        0
    ],
    "reference": "this#satellite"
}"""
    pos = Position(cartesian=[0], reference="this#satellite")

    assert str(pos) == expected_result


def test_viewfrom_reference():
    expected_result = """{
    "cartesian": [
        1.0
    ],
    "reference": "this#satellite"
}"""
    v = ViewFrom(reference="this#satellite", cartesian=[1.0])

    assert str(v) == expected_result


def test_viewfrom_cartesian():
    expected_result = """{
    "cartesian": [
        -1000,
        0,
        300
    ]
}"""
    v = ViewFrom(cartesian=Cartesian3Value(values=[-1000, 0, 300]))

    assert str(v) == expected_result


def test_viewfrom_has_delete():
    v = ViewFrom(delete=True, cartesian=[14.0, 12.0])

    assert v.delete


def test_viewfrom_no_values_raises_error():
    with pytest.raises(ValidationError) as _:
        ViewFrom()  # type: ignore


def test_single_interval_value():
    expected_result = """{
    "interval": "2019-01-01T00:00:00.000000Z/2019-01-02T00:00:00.000000Z",
    "boolean": true
}"""

    start = dt.datetime(2019, 1, 1, tzinfo=dt.timezone.utc)
    end = dt.datetime(2019, 1, 2, tzinfo=dt.timezone.utc)

    prop = IntervalValue(start=start, end=end, value=True)

    assert str(prop) == expected_result


def test_multiple_interval_value():
    expected_result = """[
    {
        "interval": "2019-01-01T00:00:00.000000Z/2019-01-02T00:00:00.000000Z",
        "boolean": true
    },
    {
        "interval": "2019-01-02T00:00:00.000000Z/2019-01-03T00:00:00.000000Z",
        "boolean": false
    }
]"""

    start0 = dt.datetime(2019, 1, 1, tzinfo=dt.timezone.utc)
    end0 = start1 = dt.datetime(2019, 1, 2, tzinfo=dt.timezone.utc)
    end1 = dt.datetime(2019, 1, 3, tzinfo=dt.timezone.utc)

    prop = Sequence(
        values=[
            IntervalValue(start=start0, end=end0, value=True),
            IntervalValue(start=start1, end=end1, value=False),
        ]
    )

    assert str(prop) == expected_result


def test_multiple_interval_decimal_value():
    expected_result = """[
    {
        "interval": "2019-01-01T01:02:03.456789Z/2019-01-02T01:02:03.456789Z",
        "boolean": true
    },
    {
        "interval": "2019-01-02T01:02:03.456789Z/2019-01-03T01:02:03.456789Z",
        "boolean": false
    }
]"""

    start0 = dt.datetime(2019, 1, 1, 1, 2, 3, 456789, tzinfo=dt.timezone.utc)
    end0 = start1 = dt.datetime(2019, 1, 2, 1, 2, 3, 456789, tzinfo=dt.timezone.utc)
    end1 = dt.datetime(2019, 1, 3, 1, 2, 3, 456789, tzinfo=dt.timezone.utc)

    prop = Sequence(
        values=[
            IntervalValue(start=start0, end=end0, value=True),
            IntervalValue(start=start1, end=end1, value=False),
        ]
    )

    assert str(prop) == expected_result


def test_orientation():
    expected_result = """{
    "unitQuaternion": [
        0,
        0,
        0,
        1
    ]
}"""

    result = Orientation(unitQuaternion=UnitQuaternionValue(values=[0, 0, 0, 1]))

    assert str(result) == expected_result


def test_model():
    expected_result = """{
    "gltf": "https://sandcastle.cesium.com/SampleData/models/CesiumAir/Cesium_Air.glb"
}"""

    result = Model(
        gltf="https://sandcastle.cesium.com/SampleData/models/CesiumAir/Cesium_Air.glb"
    )

    assert str(result) == expected_result


def test_bad_uri_raises_error():
    with pytest.raises(TypeError) as excinfo:
        Uri(uri="a")

    assert "uri must be a URL or a data URI" in excinfo.exconly()


def test_ellipsoid():
    expected_result = """{
    "radii": {
        "cartesian": [
            20.0,
            30.0,
            40.0
        ]
    },
    "fill": false,
    "outline": true
}"""

    ell = Ellipsoid(
        radii=EllipsoidRadii(cartesian=[20.0, 30.0, 40.0]), fill=False, outline=True
    )
    assert str(ell) == expected_result


def test_ellipsoid_parameters():
    expected_result = """{
    "radii": {
        "cartesian": [
            500000.0,
            500000.0,
            500000.0
        ]
    },
    "innerRadii": {
        "cartesian": [
            10000.0,
            10000.0,
            10000.0
        ]
    },
    "minimumClock": -15.0,
    "maximumClock": 15.0,
    "minimumCone": 75.0,
    "maximumCone": 105.0,
    "material": {
        "solidColor": {
            "rgba": [
                255,
                0,
                0,
                100
            ]
        }
    },
    "outline": true,
    "outlineColor": {
        "rgbaf": [
            0,
            0,
            0,
            1
        ]
    }
}"""

    ell = Ellipsoid(
        radii=EllipsoidRadii(cartesian=[500000.0, 500000.0, 500000.0]),
        innerRadii=EllipsoidRadii(cartesian=[10000.0, 10000.0, 10000.0]),
        minimumClock=-15.0,
        maximumClock=15.0,
        minimumCone=75.0,
        maximumCone=105.0,
        material=Material(
            solidColor=Color(rgba=[255, 0, 0, 100]),
        ),
        outline=True,
        outlineColor=Color(rgbaf=[0, 0, 0, 1]),
    )
    assert str(ell) == expected_result


def test_polygon_with_hole():
    expected_result = """{
    "positions": {
        "cartographicDegrees": [
            30.0,
            40.0,
            1.0
        ]
    },
    "holes": {
        "cartographicDegrees": [
            [
                20.0,
                20.0,
                0.0
            ],
            [
                10.0,
                10.0,
                0.0
            ]
        ]
    }
}"""

    p = Polygon(
        positions=PositionList(cartographicDegrees=[30.0, 40.0, 1.0]),
        holes=PositionListOfLists(
            cartographicDegrees=[[20.0, 20.0, 0.0], [10.0, 10.0, 0.0]]
        ),
    )
    assert str(p) == expected_result


def test_polygon_interval():
    """This only tests one interval"""

    expected_result = """{
    "positions": {
        "cartographicDegrees": [
            10.0,
            20.0,
            0.0
        ],
        "interval": "2019-03-20T12:00:00.000000Z/2019-04-20T12:00:00.000000Z"
    }
}"""
    t = TimeInterval(
        start=dt.datetime(2019, 3, 20, 12, tzinfo=dt.timezone.utc),
        end=dt.datetime(2019, 4, 20, 12, tzinfo=dt.timezone.utc),
    )
    poly = Polygon(
        positions=PositionList(cartographicDegrees=[10.0, 20.0, 0.0], interval=t)
    )
    assert str(poly) == expected_result


def test_polygon_outline():
    expected_result = """{
    "positions": {
        "cartographicDegrees": [
            10.0,
            20.0,
            0.0
        ]
    },
    "material": {
        "solidColor": {
            "color": {
                "rgba": [
                    255,
                    100,
                    0,
                    100
                ]
            }
        }
    },
    "outlineColor": {
        "rgba": [
            0,
            0,
            0,
            255
        ]
    },
    "outline": true,
    "extrudedHeight": 0,
    "perPositionHeight": true
}"""
    poly = Polygon(
        positions=PositionList(cartographicDegrees=[10.0, 20.0, 0.0]),
        material=Material(
            solidColor=SolidColorMaterial(
                color=Color(
                    rgba=[255, 100, 0, 100],
                ),
            ),
        ),
        outlineColor=Color(
            rgba=[0, 0, 0, 255],
        ),
        outline=True,
        extrudedHeight=0,
        perPositionHeight=True,
    )
    assert str(poly) == expected_result


def test_polygon_interval_with_position():
    """This only tests one interval"""

    expected_result = """{
    "positions": {
        "cartographicDegrees": [
            10.0,
            20.0,
            0.0
        ],
        "interval": "2019-03-20T12:00:00.000000Z/2019-04-20T12:00:00.000000Z"
    }
}"""
    t = TimeInterval(
        start=dt.datetime(2019, 3, 20, 12, tzinfo=dt.timezone.utc),
        end=dt.datetime(2019, 4, 20, 12, tzinfo=dt.timezone.utc),
    )
    poly = Polygon(
        positions=Position(cartographicDegrees=[10.0, 20.0, 0.0], interval=t)
    )
    assert str(poly) == expected_result


def test_label_offset():
    expected_result = """{
    "pixelOffset": {
        "cartesian2": [
            5,
            5
        ]
    }
}"""

    label = Label(pixelOffset=Cartesian2Value(values=[5, 5]))
    assert str(label) == expected_result


def test_tileset():
    expected_result = """{
    "uri": "../SampleData/Cesium3DTiles/Batched/BatchedColors/tileset.json",
    "show": true
}"""
    tileset = Tileset(
        show=True, uri="../SampleData/Cesium3DTiles/Batched/BatchedColors/tileset.json"
    )
    assert str(tileset) == expected_result


def test_check_classes_with_references():
    assert (
        str(ViewFrom(cartesian=[0, 0], reference="this#that"))
        == """{
    "cartesian": [
        0,
        0
    ],
    "reference": "this#that"
}"""
    )
    assert (
        str(EllipsoidRadii(cartesian=[0, 0], reference="this#that"))
        == """{
    "cartesian": [
        0,
        0
    ],
    "reference": "this#that"
}"""
    )
    assert (
        str(ArcType(arcType=ArcTypes.GEODESIC, reference="this#that"))
        == """{
    "arcType": "GEODESIC",
    "reference": "this#that"
}"""
    )
    assert (
        str(Position(cartesian=[0, 0], reference="this#that"))
        == """{
    "cartesian": [
        0,
        0
    ],
    "reference": "this#that"
}"""
    )
    assert (
        str(Orientation(unitQuaternion=[0, 0, 0, 0], reference="this#that"))
        == """{
    "unitQuaternion": [
        0,
        0,
        0,
        0
    ],
    "reference": "this#that"
}"""
    )
    assert (
        str(NearFarScalar(nearFarScalar=[0, 0], reference="this#that"))
        == """{
    "nearFarScalar": [
        0,
        0
    ],
    "reference": "this#that"
}"""
    )
    assert (
        str(CornerType(cornerType=CornerTypes.BEVELED, reference="this#that"))
        == """{
    "cornerType": "BEVELED",
    "reference": "this#that"
}"""
    )
    assert (
        str(
            ColorBlendMode(
                colorBlendMode=ColorBlendModes.HIGHLIGHT, reference="this#that"
            )
        )
        == """{
    "colorBlendMode": "HIGHLIGHT",
    "reference": "this#that"
}"""
    )
    assert (
        str(
            HeightReference(
                heightReference=HeightReferences.NONE, reference="this#that"
            )
        )
        == """{
    "heightReference": "NONE",
    "reference": "this#that"
}"""
    )
    assert (
        str(EyeOffset(cartesian=[0, 0], reference="this#that"))
        == """{
    "cartesian": [
        0,
        0
    ],
    "reference": "this#that"
}"""
    )
    assert (
        str(RectangleCoordinates(wsen=[0, 0], reference="this#that"))
        == """{
    "wsen": [
        0,
        0
    ],
    "reference": "this#that"
}"""
    )
    assert (
        str(
            BoxDimensions(
                cartesian=Cartesian3Value(values=[0, 0, 1]), reference="this#that"
            )
        )
        == """{
    "cartesian": [
        0,
        0,
        1
    ],
    "reference": "this#that"
}"""
    )
    assert (
        str(
            DistanceDisplayCondition(
                distanceDisplayCondition=DistanceDisplayConditionValue(
                    values=[0, 1, 2]
                ),
                reference="this#that",
            )
        )
        == """{
    "distanceDisplayCondition": [
        0,
        1,
        2
    ],
    "reference": "this#that"
}"""
    )
    assert (
        str(
            ClassificationType(
                classificationType=ClassificationTypes.BOTH, reference="this#that"
            )
        )
        == """{
    "classificationType": "BOTH",
    "reference": "this#that"
}"""
    )
    assert (
        str(ShadowMode(shadowMode=ShadowModes.CAST_ONLY, reference="this#that"))
        == """{
    "shadowMode": "CAST_ONLY",
    "reference": "this#that"
}"""
    )


def test_rectangle_coordinates_delete():
    assert (
        str(RectangleCoordinates(wsen=[0, 0], reference="this#that", delete=True))
        == """{
    "delete": true
}"""
    )
