from uuid import uuid4

import attr

from .core import Document, Preamble

CESIUM_TPL = """
<link rel="stylesheet" href="https://cesium.com/downloads/cesiumjs/releases/{cesium_version}/Build/Cesium/Widgets/widgets.css" type="text/css">
<div id="cesiumContainer-{container_id}" style="width:100%; height:100%;"><div>
<script type="text/javascript">
{script}
</script>"""

SCRIPT_TPL = """
require.config({{
    paths: {{
        'cesium': 'https://cesium.com/downloads/cesiumjs/releases/{cesium_version}/Build/Cesium/Cesium'
    }}
}});

require(['cesium'], function (dependency) {{
    var czml = {czml};

    var viewer = new Cesium.Viewer('cesiumContainer-{container_id}', {{
        shouldAnimate : true
    }});

    // To have an inertial (ICRF) view
    function icrf(scene, time) {{
        var icrfToFixed = Cesium.Transforms.computeIcrfToFixedMatrix(time);
        if (Cesium.defined(icrfToFixed)) {{
            var camera = viewer.camera;
            var offset = Cesium.Cartesian3.clone(camera.position);
            var transform = Cesium.Matrix4.fromRotationTranslation(icrfToFixed);
            camera.lookAtTransform(transform, offset);
        }}
    }}
    // Temporarily disable inertial view
    // until we make it work with 2D Mercator view
    // and fix the zoom sensitivity, see
    // https://groups.google.com/d/msg/cesium-dev/vuXmepd4T2E/i71tq2I8EAAJ
    // viewer.scene.postUpdate.addEventListener(icrf);

    viewer.camera.flyHome(0);
    viewer.scene.globe.enableLighting = true;

    viewer.dataSources.add(Cesium.CzmlDataSource.load(czml));
}});
"""


@attr.s
class CZMLWidget:
    document = attr.ib(default=Document([Preamble()]))
    cesium_version = attr.ib(default="1.62")

    _container_id = attr.ib(factory=uuid4)

    def build_script(self):
        return SCRIPT_TPL.format(
            cesium_version=self.cesium_version,
            czml=self.document.dumps(),
            container_id=self._container_id,
        )

    def to_html(self):
        return CESIUM_TPL.format(
            cesium_version=self.cesium_version,
            script=self.build_script(),
            container_id=self._container_id,
        )

    def _repr_html_(self):
        return self.to_html()
