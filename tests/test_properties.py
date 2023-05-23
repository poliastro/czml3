import datetime as dt

import pytest

from czml3.core import Packet
from czml3.enums import (
    ArcTypes,
    ClassificationTypes,
    InterpolationAlgorithms,
    ReferenceFrames,
    ShadowModes,
)
from czml3.properties import (
    ArcType,
    Box,
    BoxDimensions,
    CheckerboardMaterial,
    ClassificationType,
    Color,
    DistanceDisplayCondition,
    Ellipsoid,
    EllipsoidRadii,
    EyeOffset,
    GridMaterial,
    ImageMaterial,
    Material,
    Model,
    NearFarScalar,
    Orientation,
    Path,
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
    Rectangle,
    RectangleCoordinates,
    ShadowMode,
    SolidColorMaterial,
    StripeMaterial,
    Uri,
    ViewFrom,
    Wall,
)
from czml3.types import (
    Cartesian3Value,
    CartographicDegreesListValue,
    DistanceDisplayConditionValue,
    IntervalValue,
    NearFarScalarValue,
    Sequence,
    UnitQuaternionValue,
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


def test_polyline_svg():
    expected_result = '<svg xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMinYMin meet" width="300.0" height="300.0" viewBox="1960.0 2960.0 1080.0 1080.0"><g transform="matrix(1,0,0,-1,0,7000.0)"><polyline stroke="rgba(200,100,30,255)" fill="none" points="2000.0,3000.0 2500.0,3500.0 3000.0,4000.0" /></g></svg>'
    pol = Polyline(
        positions=PositionList(
            cartographicDegrees=CartographicDegreesListValue(
                values=[20, 30, 10, 25, 35, 10, 30, 40, 10]
            )
        ),
        arcType=ArcType(arcType="GEODESIC"),
        distanceDisplayCondition=DistanceDisplayCondition(
            distanceDisplayCondition=DistanceDisplayConditionValue(values=[14, 81])
        ),
        classificationType=ClassificationType(
            classificationType=ClassificationTypes.CESIUM_3D_TILE
        ),
        material=Material(solidColor=SolidColorMaterial.from_list([200, 100, 30])),
    )
    str_svg = pol._repr_svg_()
    assert str_svg == expected_result


def test_polygon_svg():
    expected_result = '<svg xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMinYMin meet" width="300.0" height="300.0" viewBox="1940.0 2940.0 1620.0 1120.0"><g transform="matrix(1,0,0,-1,0,7000.0)"><path d="M 2000.0,3000.0 L 3500.0,3500.0 L 2000.0,4000.0 z" fill="rgba(200,100,30,255)"/></g></svg>'
    pol = Polygon(
        positions=PositionList(
            cartographicDegrees=CartographicDegreesListValue(
                values=[20, 30, 10, 35, 35, 10, 20, 40, 10]
            )
        ),
        material=Material(solidColor=SolidColorMaterial.from_list([200, 100, 30])),
    )
    str_svg = pol._repr_svg_()
    assert expected_result == str_svg


def test_no_svg():
    expected_result = """<svg xmlns="http://www.w3.org/2000/svg"
xmlns:xlink="http://www.w3.org/1999/xlink"
width="50%" viewBox="0 0 1000 1000">
<path d="M512 85.333333C277.333333 85.333333 85.333333 277.333333 85.333333 512s192 426.666667 426.666667 426.666667 426.666667-192 426.666667-426.666667S746.666667 85.333333 512 85.333333z" fill="#7CB342" /><path d="M960 512c0 249.6-202.666667 448-448 448S64 761.6 64 512 262.4 64 512 64s448 198.4 448 448z m-452.266667 206.933333c0-8.533333-4.266667-12.8-12.8-17.066666-27.733333-8.533333-53.333333-8.533333-76.8-32-4.266667-8.533333-4.266667-17.066667-8.533333-27.733334-8.533333-8.533333-32-12.8-44.8-17.066666h-89.6c-12.8-4.266667-23.466667-23.466667-32-36.266667 0-4.266667 0-12.8-8.533333-12.8-8.533333-4.266667-17.066667 4.266667-27.733334 0-4.266667-4.266667-4.266667-8.533333-4.266666-12.8 0-12.8 8.533333-27.733333 17.066666-36.266667 12.8-8.533333 27.733333 4.266667 40.533334 4.266667 4.266667 0 4.266667 0 8.533333 4.266667 12.8 4.266667 17.066667 21.333333 17.066667 36.266666v8.533334c0 4.266667 4.266667 4.266667 8.533333 4.266666 4.266667-23.466667 4.266667-44.8 8.533333-68.266666 0-27.733333 27.733333-53.333333 49.066667-61.866667 8.533333-4.266667 12.8 4.266667 23.466667 0 27.733333-8.533333 93.866667-36.266667 81.066666-72.533333-8.533333-32-36.266667-61.866667-72.533333-57.6-8.533333 4.266667-12.8 8.533333-21.333333 12.8-12.8 8.533333-40.533333 36.266667-53.333334 36.266666-23.466667-4.266667-23.466667-36.266667-17.066666-49.066666 4.266667-17.066667 44.8-76.8 72.533333-66.133334l17.066667 17.066667c8.533333 4.266667 23.466667 4.266667 36.266666 4.266667 4.266667 0 8.533333 0 12.8-4.266667 4.266667-4.266667 4.266667-4.266667 4.266667-8.533333 0-12.8-12.8-27.733333-21.333333-36.266667-8.533333-8.533333-23.466667-17.066667-36.266667-23.466667-44.8-12.8-117.333333 4.266667-151.466667 36.266667s-61.866667 85.333333-81.066666 130.133333c-8.533333 27.733333-17.066667 61.866667-21.333334 93.866667-4.266667 21.333333-8.533333 40.533333 4.266667 61.866667 12.8 27.733333 40.533333 53.333333 68.266667 72.533333 17.066667 12.8 53.333333 12.8 72.533333 36.266667 12.8 17.066667 8.533333 40.533333 8.533333 61.866666 0 27.733333 17.066667 49.066667 27.733334 72.533334 4.266667 12.8 8.533333 32 12.8 44.8 0 4.266667 4.266667 32 4.266666 36.266666 27.733333 12.8 49.066667 27.733333 81.066667 36.266667 4.266667 0 21.333333-27.733333 21.333333-32 12.8-12.8 23.466667-32 36.266667-40.533333 8.533333-4.266667 17.066667-8.533333 27.733333-17.066667 8.533333-8.533333 12.8-27.733333 17.066667-40.533333 2.133333-10.666667 6.4-27.733333 2.133333-40.533334z m8.533334-413.866666c4.266667 0 8.533333-4.266667 17.066666-8.533334 12.8-8.533333 27.733333-23.466667 40.533334-32 12.8-8.533333 27.733333-23.466667 36.266666-32 12.8-8.533333 23.466667-27.733333 27.733334-40.533333 4.266667-8.533333 17.066667-27.733333 12.8-40.533333-4.266667-8.533333-27.733333-12.8-36.266667-17.066667-36.266667-8.533333-66.133333-12.8-102.4-12.8-12.8 0-32 4.266667-36.266667 17.066667-4.266667 23.466667 12.8 17.066667 32 23.466666 0 0 4.266667 36.266667 4.266667 40.533334 4.266667 21.333333-8.533333 36.266667-8.533333 57.6 0 12.8 0 36.266667 8.533333 44.8h4.266667zM891.733333 618.666667c4.266667-8.533333 4.266667-23.466667 8.533334-32 4.266667-21.333333 4.266667-44.8 4.266666-66.133334 0-44.8-4.266667-89.6-17.066666-130.133333-8.533333-12.8-12.8-27.733333-17.066667-40.533333-8.533333-23.466667-21.333333-44.8-40.533333-61.866667-17.066667-23.466667-40.533333-85.333333-81.066667-66.133333-12.8 4.266667-21.333333 21.333333-32 32-8.533333 12.8-17.066667 27.733333-27.733333 40.533333-4.266667 4.266667-8.533333 12.8-4.266667 17.066667 0 4.266667 4.266667 4.266667 8.533333 4.266666 8.533333 4.266667 12.8 4.266667 21.333334 8.533334 4.266667 0 8.533333 4.266667 4.266666 8.533333 0 0 0 4.266667-4.266666 4.266667-21.333333 23.466667-44.8 40.533333-66.133334 61.866666-4.266667 4.266667-8.533333 12.8-8.533333 17.066667 0 4.266667 4.266667 4.266667 4.266667 8.533333s-4.266667 4.266667-8.533334 8.533334c-8.533333 4.266667-17.066667 8.533333-23.466666 12.8-4.266667 8.533333 0 23.466667-4.266667 32-4.266667 23.466667-17.066667 40.533333-27.733333 61.866666-8.533333 12.8-12.8 27.733333-21.333334 40.533334 0 17.066667-4.266667 32 4.266667 44.8 21.333333 32 61.866667 12.8 93.866667 27.733333 8.533333 4.266667 17.066667 4.266667 23.466666 12.8 12.8 12.8 12.8 36.266667 17.066667 49.066667 4.266667 17.066667 8.533333 36.266667 17.066667 53.333333 4.266667 21.333333 12.8 44.8 17.066666 61.866667 40.533333-32 76.8-66.133333 102.4-110.933334 32-27.733333 44.8-64 57.6-100.266666z" fill="#0277BD" />
<text x="200" y="-790" fill="red" transform="rotate(90 0 0)" style="font-family:ariel;font-size:300">czml3</text>
<defs>
<path id="curve1" d="M 10 100 C 200 30 300 250 350 50"
stroke="black" fill="none" stroke-width="5" />
<path id="curve2" d="M 100 300 C 300 -50 600 20 800 125"
stroke="black" fill="none" stroke-width="5"  transform="translate(0,20)"/>
</defs>
<!-- <text id="T" style="font-family:ariel;font-size:16">
<textPath xlink:href="#curve1" startOffset ="10" fill="red">
<animate attributeName="startOffset" dur="7s" from="0" to="320"
repeatCount="1" />
Property has no position!
</textPath>
</text> -->
<text id="T" fill="black" style="font-family:ariel;font-size:90">
<textPath xlink:href="#curve2">
No position found.
</textPath>
</text>
</svg>"""
    pnt = Point(
        show=True,
        pixelSize=10,
        scaleByDistance=NearFarScalar(
            nearFarScalar=NearFarScalarValue(values=[150, 2.0, 15000000, 0.5])
        ),
        disableDepthTestDistance=1.2,
        color=Color(rgba=[200, 100, 30, 255]),
    )
    assert pnt._repr_svg_() == expected_result


def test_position_svg():
    expected_result = '<svg xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMinYMin meet" width="100.0" height="100.0" viewBox="990.0 1980.0 20.0 40.0"><g transform="matrix(1,0,0,-1,0,4000.0)"><circle fill="black" cx="1000.0" cy="2000.0" r="2.0" /></g></svg>'
    pos = Position(cartographicDegrees=[10.0, 20.0, 0.0])
    str_svg = pos._repr_svg_()
    assert str_svg == expected_result


def test_positionlist_svg():
    expected_result = '<svg xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMinYMin meet" width="108.0" height="108.0" viewBox="996.0 1096.0 108.0 108.0"><g transform="matrix(1,0,0,-1,0,2300.0)"><circle fill="black" cx="1000.0" cy="1100.0" r="2.0" /><circle fill="black" cx="1100.0" cy="1200.0" r="2.0" /></g></svg>'
    pos = PositionList(cartographicDegrees=[10.0, 11.0, 0.0, 11, 12, 0])
    str_svg = pos._repr_svg_()
    assert str_svg == expected_result


def test_packet_svg_with_point():
    expected_result = '<svg xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMinYMin meet" width="216.0" height="216.0" viewBox="3592.0 3592.0 216.0 216.0"><g transform="matrix(1,0,0,-1,0,7400.0)"><circle fill="rgba(200,100,30,255)" cx="3800.0" cy="3800.0" r="2.32" /><path d="M 3720.0000000000005,3729.9999999999995 L 3800.0,3800.0 L 3750.0,3690.0 z" fill="rgba(200,100,30,255)"/><polyline stroke="rgba(0,255,0,255)" fill="none" points="3700.0,3700.0 3600.0,3600.0" /></g></svg>'
    p = Packet(
        id="AreaTarget/Pennsylvania",
        name="Pennsylvania",
        position=Position(cartographicDegrees=[38, 38, 10]),
        point=Point(
            show=True,
            pixelSize=10,
            scaleByDistance=NearFarScalar(
                nearFarScalar=NearFarScalarValue(values=[150, 2.0, 15000000, 0.5])
            ),
            disableDepthTestDistance=1.2,
            color=Color(rgba=[200, 100, 30, 255]),
        ),
        polygon=Polygon(
            positions=PositionList(
                cartographicDegrees=CartographicDegreesListValue(
                    values=[37.2, 37.3, 10, 38, 38, 10, 37.5, 36.9, 10]
                )
            ),
            material=Material(solidColor=SolidColorMaterial.from_list([200, 100, 30])),
        ),
        polyline=Polyline(
            material=Material(solidColor=SolidColorMaterial.from_list([0, 255, 0])),
            positions=PositionList(
                cartographicDegrees=CartographicDegreesListValue(
                    values=[37, 37, 10, 36, 36, 10]
                )
            ),
            arcType=ArcType(arcType="GEODESIC"),
            distanceDisplayCondition=DistanceDisplayCondition(
                distanceDisplayCondition=DistanceDisplayConditionValue(values=[14, 81])
            ),
            classificationType=ClassificationType(
                classificationType=ClassificationTypes.CESIUM_3D_TILE
            ),
        ),
    )
    str_svg = p._repr_svg_()
    assert str_svg == expected_result


def test_rectangle_svg():
    expected_restult = '<svg xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMinYMin meet" width="300.0" height="300.0" viewBox="-12040.0 3960.0 1080.0 1080.0"><g transform="matrix(1,0,0,-1,0,9000.0)"><polyline stroke="black" fill="none" points="-12000.0,4000.0 -12000.0,5000.0 -11000.0,5000.0 -11000.0,4000.0 -12000.0,4000.0" /></g></svg>'
    r = Rectangle(coordinates=RectangleCoordinates(wsenDegrees=[-120, 40, -110, 50]))
    str_svg = r._repr_svg_()
    assert str_svg == expected_restult


def test_wall_svg():
    expected_result = '<svg xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMinYMin meet" width="300.0" height="300.0" viewBox="3707.6000000000004 3677.6 304.7999999999997 334.8000000000002"><g transform="matrix(1,0,0,-1,0,7690.0)"><polyline stroke="black" fill="none" points="3720.0000000000005,3729.9999999999995 3800.0,3800.0 3750.0,3690.0 4000.0,4000.0" /></g></svg>'
    w = Wall(
        positions=PositionList(
            cartographicDegrees=CartographicDegreesListValue(
                values=[37.2, 37.3, 10, 38, 38, 10, 37.5, 36.9, 10, 40, 40, 0]
            )
        )
    )
    str_svg = w._repr_svg_()
    assert str_svg == expected_result


def test_packet_svg_with_path():
    expected_result = '<svg xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMinYMin meet" width="300.0" height="300.0" viewBox="2920.0 2920.0 1160.0 2160.0"><g transform="matrix(1,0,0,-1,0,8000.0)"><polyline stroke="rgba(0,255,0,255)" fill="none" points="3000.0,3000.0 3100.0,3200.0 3300.0,5000.0 4000.0,3900.0" /><path d="M 3720.0000000000005,3729.9999999999995 L 3800.0,3800.0 L 3750.0,3690.0 z" fill="rgba(200,100,30,255)"/><polyline stroke="rgba(0,255,0,255)" fill="none" points="3700.0,3700.0 3600.0,3600.0" /></g></svg>'
    start = dt.datetime(2012, 3, 15, 10, tzinfo=dt.timezone.utc)
    end = dt.datetime(2012, 3, 16, 10, tzinfo=dt.timezone.utc)
    p = Packet(
        id="AreaTarget/Pennsylvania",
        name="Pennsylvania",
        position=Position(
            interpolationAlgorithm=InterpolationAlgorithms.LAGRANGE,
            interpolationDegree=5,
            referenceFrame=ReferenceFrames.INERTIAL,
            epoch=start,
            cartographicDegrees=[30, 30, 0, 31, 32, 10, 33, 50, 0, 40, 39, 0],
        ),
        path=Path(
            show=Sequence([IntervalValue(start=start, end=end, value=True)]),
            width=1,
            resolution=120,
            material=Material(solidColor=SolidColorMaterial.from_list([0, 255, 0])),
        ),
        polygon=Polygon(
            positions=PositionList(
                cartographicDegrees=CartographicDegreesListValue(
                    values=[37.2, 37.3, 10, 38, 38, 10, 37.5, 36.9, 10]
                )
            ),
            material=Material(solidColor=SolidColorMaterial.from_list([200, 100, 30])),
        ),
        polyline=Polyline(
            material=Material(solidColor=SolidColorMaterial.from_list([0, 255, 0])),
            positions=PositionList(
                cartographicDegrees=CartographicDegreesListValue(
                    values=[37, 37, 10, 36, 36, 10]
                )
            ),
            arcType=ArcType(arcType="GEODESIC"),
            distanceDisplayCondition=DistanceDisplayCondition(
                distanceDisplayCondition=DistanceDisplayConditionValue(values=[14, 81])
            ),
            classificationType=ClassificationType(
                classificationType=ClassificationTypes.CESIUM_3D_TILE
            ),
        ),
    )
    str_svg = p._repr_svg_()
    assert str_svg == expected_result


def test_packet_svg_no_position_for_point():
    expected_result = "No coordinates found."
    with pytest.raises(ValueError) as e:
        p = Packet(
            id="AreaTarget/Pennsylvania",
            name="Pennsylvania",
            point=Point(
                show=True,
                pixelSize=10,
                scaleByDistance=NearFarScalar(
                    nearFarScalar=NearFarScalarValue(values=[150, 2.0, 15000000, 0.5])
                ),
                disableDepthTestDistance=1.2,
                color=Color(rgba=[200, 100, 30, 255]),
            ),
        )
        p._repr_svg_()
    assert str(e.value) == expected_result


def test_no_position_error():
    expected_result = """<svg xmlns="http://www.w3.org/2000/svg"
xmlns:xlink="http://www.w3.org/1999/xlink"
width="50%" viewBox="0 0 1000 1000">
<path d="M512 85.333333C277.333333 85.333333 85.333333 277.333333 85.333333 512s192 426.666667 426.666667 426.666667 426.666667-192 426.666667-426.666667S746.666667 85.333333 512 85.333333z" fill="#7CB342" /><path d="M960 512c0 249.6-202.666667 448-448 448S64 761.6 64 512 262.4 64 512 64s448 198.4 448 448z m-452.266667 206.933333c0-8.533333-4.266667-12.8-12.8-17.066666-27.733333-8.533333-53.333333-8.533333-76.8-32-4.266667-8.533333-4.266667-17.066667-8.533333-27.733334-8.533333-8.533333-32-12.8-44.8-17.066666h-89.6c-12.8-4.266667-23.466667-23.466667-32-36.266667 0-4.266667 0-12.8-8.533333-12.8-8.533333-4.266667-17.066667 4.266667-27.733334 0-4.266667-4.266667-4.266667-8.533333-4.266666-12.8 0-12.8 8.533333-27.733333 17.066666-36.266667 12.8-8.533333 27.733333 4.266667 40.533334 4.266667 4.266667 0 4.266667 0 8.533333 4.266667 12.8 4.266667 17.066667 21.333333 17.066667 36.266666v8.533334c0 4.266667 4.266667 4.266667 8.533333 4.266666 4.266667-23.466667 4.266667-44.8 8.533333-68.266666 0-27.733333 27.733333-53.333333 49.066667-61.866667 8.533333-4.266667 12.8 4.266667 23.466667 0 27.733333-8.533333 93.866667-36.266667 81.066666-72.533333-8.533333-32-36.266667-61.866667-72.533333-57.6-8.533333 4.266667-12.8 8.533333-21.333333 12.8-12.8 8.533333-40.533333 36.266667-53.333334 36.266666-23.466667-4.266667-23.466667-36.266667-17.066666-49.066666 4.266667-17.066667 44.8-76.8 72.533333-66.133334l17.066667 17.066667c8.533333 4.266667 23.466667 4.266667 36.266666 4.266667 4.266667 0 8.533333 0 12.8-4.266667 4.266667-4.266667 4.266667-4.266667 4.266667-8.533333 0-12.8-12.8-27.733333-21.333333-36.266667-8.533333-8.533333-23.466667-17.066667-36.266667-23.466667-44.8-12.8-117.333333 4.266667-151.466667 36.266667s-61.866667 85.333333-81.066666 130.133333c-8.533333 27.733333-17.066667 61.866667-21.333334 93.866667-4.266667 21.333333-8.533333 40.533333 4.266667 61.866667 12.8 27.733333 40.533333 53.333333 68.266667 72.533333 17.066667 12.8 53.333333 12.8 72.533333 36.266667 12.8 17.066667 8.533333 40.533333 8.533333 61.866666 0 27.733333 17.066667 49.066667 27.733334 72.533334 4.266667 12.8 8.533333 32 12.8 44.8 0 4.266667 4.266667 32 4.266666 36.266666 27.733333 12.8 49.066667 27.733333 81.066667 36.266667 4.266667 0 21.333333-27.733333 21.333333-32 12.8-12.8 23.466667-32 36.266667-40.533333 8.533333-4.266667 17.066667-8.533333 27.733333-17.066667 8.533333-8.533333 12.8-27.733333 17.066667-40.533333 2.133333-10.666667 6.4-27.733333 2.133333-40.533334z m8.533334-413.866666c4.266667 0 8.533333-4.266667 17.066666-8.533334 12.8-8.533333 27.733333-23.466667 40.533334-32 12.8-8.533333 27.733333-23.466667 36.266666-32 12.8-8.533333 23.466667-27.733333 27.733334-40.533333 4.266667-8.533333 17.066667-27.733333 12.8-40.533333-4.266667-8.533333-27.733333-12.8-36.266667-17.066667-36.266667-8.533333-66.133333-12.8-102.4-12.8-12.8 0-32 4.266667-36.266667 17.066667-4.266667 23.466667 12.8 17.066667 32 23.466666 0 0 4.266667 36.266667 4.266667 40.533334 4.266667 21.333333-8.533333 36.266667-8.533333 57.6 0 12.8 0 36.266667 8.533333 44.8h4.266667zM891.733333 618.666667c4.266667-8.533333 4.266667-23.466667 8.533334-32 4.266667-21.333333 4.266667-44.8 4.266666-66.133334 0-44.8-4.266667-89.6-17.066666-130.133333-8.533333-12.8-12.8-27.733333-17.066667-40.533333-8.533333-23.466667-21.333333-44.8-40.533333-61.866667-17.066667-23.466667-40.533333-85.333333-81.066667-66.133333-12.8 4.266667-21.333333 21.333333-32 32-8.533333 12.8-17.066667 27.733333-27.733333 40.533333-4.266667 4.266667-8.533333 12.8-4.266667 17.066667 0 4.266667 4.266667 4.266667 8.533333 4.266666 8.533333 4.266667 12.8 4.266667 21.333334 8.533334 4.266667 0 8.533333 4.266667 4.266666 8.533333 0 0 0 4.266667-4.266666 4.266667-21.333333 23.466667-44.8 40.533333-66.133334 61.866666-4.266667 4.266667-8.533333 12.8-8.533333 17.066667 0 4.266667 4.266667 4.266667 4.266667 8.533333s-4.266667 4.266667-8.533334 8.533334c-8.533333 4.266667-17.066667 8.533333-23.466666 12.8-4.266667 8.533333 0 23.466667-4.266667 32-4.266667 23.466667-17.066667 40.533333-27.733333 61.866666-8.533333 12.8-12.8 27.733333-21.333334 40.533334 0 17.066667-4.266667 32 4.266667 44.8 21.333333 32 61.866667 12.8 93.866667 27.733333 8.533333 4.266667 17.066667 4.266667 23.466666 12.8 12.8 12.8 12.8 36.266667 17.066667 49.066667 4.266667 17.066667 8.533333 36.266667 17.066667 53.333333 4.266667 21.333333 12.8 44.8 17.066666 61.866667 40.533333-32 76.8-66.133333 102.4-110.933334 32-27.733333 44.8-64 57.6-100.266666z" fill="#0277BD" />
<text x="200" y="-790" fill="red" transform="rotate(90 0 0)" style="font-family:ariel;font-size:300">czml3</text>
<defs>
<path id="curve1" d="M 10 100 C 200 30 300 250 350 50"
stroke="black" fill="none" stroke-width="5" />
<path id="curve2" d="M 100 300 C 300 -50 600 20 800 125"
stroke="black" fill="none" stroke-width="5"  transform="translate(0,20)"/>
</defs>
<!-- <text id="T" style="font-family:ariel;font-size:16">
<textPath xlink:href="#curve1" startOffset ="10" fill="red">
<animate attributeName="startOffset" dur="7s" from="0" to="320"
repeatCount="1" />
Property has no position!
</textPath>
</text> -->
<text id="T" fill="black" style="font-family:ariel;font-size:90">
<textPath xlink:href="#curve2">
No position found.
</textPath>
</text>
</svg>"""
    p = Material(
        image=ImageMaterial(
            image=Uri(uri="https://site.com/image.png"),
            repeat=[2, 2],
            color=Color.from_list([200, 100, 30]),
        )
    )
    str_svg = p._repr_svg_()
    assert str_svg == expected_result


def test_packet_svg_no_color():
    expected_result = '<svg xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMinYMin meet" width="216.0" height="216.0" viewBox="3592.0 3592.0 216.0 216.0"><g transform="matrix(1,0,0,-1,0,7400.0)"><circle fill="black" cx="3800.0" cy="3800.0" r="2.32" /><path d="M 3720.0000000000005,3729.9999999999995 L 3800.0,3800.0 L 3750.0,3690.0 z" fill="black"/><polyline stroke="black" fill="none" points="3700.0,3700.0 3600.0,3600.0" /></g></svg>'
    p = Packet(
        id="AreaTarget/Pennsylvania",
        name="Pennsylvania",
        position=Position(cartographicDegrees=[38, 38, 10]),
        point=Point(
            show=True,
            pixelSize=10,
            scaleByDistance=NearFarScalar(
                nearFarScalar=NearFarScalarValue(values=[150, 2.0, 15000000, 0.5])
            ),
            disableDepthTestDistance=1.2,
        ),
        polygon=Polygon(
            positions=PositionList(
                cartographicDegrees=CartographicDegreesListValue(
                    values=[37.2, 37.3, 10, 38, 38, 10, 37.5, 36.9, 10]
                )
            ),
            # material=Material(solidColor=SolidColorMaterial.from_list([200, 100, 30])),
        ),
        polyline=Polyline(
            positions=PositionList(
                cartographicDegrees=CartographicDegreesListValue(
                    values=[37, 37, 10, 36, 36, 10]
                )
            ),
            arcType=ArcType(arcType="GEODESIC"),
            distanceDisplayCondition=DistanceDisplayCondition(
                distanceDisplayCondition=DistanceDisplayConditionValue(values=[14, 81])
            ),
            classificationType=ClassificationType(
                classificationType=ClassificationTypes.CESIUM_3D_TILE
            ),
        ),
    )
    str_svg = p._repr_svg_()
    assert str_svg == expected_result


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
    mat = Material(solidColor=SolidColorMaterial.from_list([200, 100, 30]))

    assert str(mat) == expected_result

    pol_mat = PolylineMaterial(solidColor=SolidColorMaterial.from_list([200, 100, 30]))
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


def test_color_isvalid():
    assert Color.is_valid([255, 204, 0, 55])
    assert Color.is_valid([255, 204, 55])
    assert Color.is_valid(0xFF3223)
    assert Color.is_valid(32)
    assert Color.is_valid(0xFF322332)
    assert Color.is_valid("#FF3223")
    assert Color.is_valid("#FF322332")
    assert Color.is_valid((255, 204, 55))
    assert Color.is_valid((255, 204, 55, 255))
    assert Color.is_valid((0.127568, 0.566949, 0.550556))
    assert Color.is_valid((0.127568, 0.566949, 0.550556, 1.0))


def test_color_isvalid_false():
    assert Color.is_valid([256, 204, 0, 55]) is False
    assert Color.is_valid([-204, 0, 55]) is False
    assert Color.is_valid([249.1, 204.3, 55.4]) is False
    assert Color.is_valid([255, 204]) is False
    assert Color.is_valid([255, 232, 300]) is False
    assert Color.is_valid(0xFF3223324) is False
    assert Color.is_valid(-3) is False
    assert Color.is_valid("totally valid color") is False
    assert Color.is_valid("#FF322332432") is False
    assert Color.is_valid((255, 204, 55, 255, 42)) is False
    assert Color.is_valid((0.127568, 0.566949, 0.550556, 1.0, 3.0)) is False


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
            color=Color.from_list([200, 100, 30]),
        )
    )
    assert str(mat) == expected_result

    pol_mat = PolylineMaterial(
        image=ImageMaterial(
            image=Uri(uri="https://site.com/image.png"),
            repeat=[2, 2],
            color=Color.from_list([200, 100, 30]),
        )
    )
    assert str(pol_mat) == expected_result


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
        color=Color.from_list([20, 20, 30]),
        cellAlpha=1.0,
        lineCount=[16, 16],
        lineThickness=[2.0, 2.0],
        lineOffset=[0.3, 0.4],
    )
    assert str(pol_mat) == expected_result


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
        evenColor=Color.from_list([0, 0, 0]),
        oddColor=Color.from_list([255, 255, 255]),
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
        evenColor=Color.from_list([0, 0, 0]),
        oddColor=Color.from_list([255, 255, 255]),
        repeat=4,
    )
    assert str(pol_mat) == expected_result


def test_position_has_delete():
    pos = Position(delete=True, cartesian=[])

    assert pos.delete


def test_position_no_values_raises_error():
    with pytest.raises(ValueError) as exc:
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
    expected_epoch = dt.datetime(2019, 6, 11, 12, 26, 58, tzinfo=dt.timezone.utc)

    pos = Position(epoch=expected_epoch, cartesian=[])

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
    "reference": "satellite"
}"""
    pos = Position(reference="satellite")

    assert str(pos) == expected_result


def test_viewfrom_reference():
    expected_result = """{
    "reference": "satellite"
}"""
    v = ViewFrom(reference="satellite")

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
    v = ViewFrom(delete=True, cartesian=[])

    assert v.delete


def test_viewfrom_no_values_raises_error():
    with pytest.raises(ValueError) as exc:
        ViewFrom()

    assert "One of cartesian or reference must be given" in exc.exconly()


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
        [
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
        [
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
    with pytest.raises(ValueError) as excinfo:
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


def test_color_rgbaf_from_tuple():
    expected_result = """{
    "rgbaf": [
        0.127568,
        0.566949,
        0.550556,
        1.0
    ]
}"""
    tc = Color.from_tuple((0.127568, 0.566949, 0.550556, 1.0))
    assert str(tc) == expected_result


def test_color_rgba_from_tuple():
    expected_result = """{
    "rgba": [
        100,
        200,
        255,
        255
    ]
}"""
    tc = Color.from_tuple((100, 200, 255))
    assert str(tc) == expected_result
