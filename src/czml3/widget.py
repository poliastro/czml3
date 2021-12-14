from uuid import uuid4

import attr

from .core import Document, Preamble

TERRAIN = {
    "Cesium": "Cesium.createWorldTerrain()",
    "Ellipsoid": "new Cesium.EllipsoidTerrainProvider()",
}

IMAGERY = {
    "Bing_Aerial": "Cesium.createWorldImagery()",
    "OSM": "new Cesium.OpenStreetMapImageryProvider()",
}

CESIUM_TPL = """
<link rel="stylesheet" href="https://cesium.com/downloads/cesiumjs/releases/{cesium_version}/Build/Cesium/Widgets/widgets.css" type="text/css">
<div id="cesiumContainer-{container_id}" style="width:100%; height:{widget_height};"></div>
<script type="text/javascript">
{script}
</script>"""

SCRIPT_TPL = """
require.config({{
    paths: {{
        'cesium': 'https://cesium.com/downloads/cesiumjs/releases/{cesium_version}/Build/Cesium/Cesium'
    }}
}});

// Set this global variable to avoid problems with non-local Jupyter deployments
// Basically this line:
// https://github.com/AnalyticalGraphicsInc/cesium/blob/1.64/Source/Core/buildModuleUrl.js#L13
// Fails because of this:
// https://github.com/jupyter/notebook/blob/6.0.2/notebook/templates/page.html#L25-L27
// Also, finding out about CESIUM_BASE_URL was not very straightforward,
// see https://github.com/AnalyticalGraphicsInc/cesium/issues/8327
var CESIUM_BASE_URL = 'https://cesium.com/downloads/cesiumjs/releases/{cesium_version}/Build/Cesium/'

require(['cesium'], function (Cesium) {{
    var czml = {czml};

    var ion_token = '{ion_token}';
    if (ion_token !== '') {{
        Cesium.Ion.defaultAccessToken = ion_token;
    }}
    var viewer = new Cesium.Viewer('cesiumContainer-{container_id}', {{
        terrainProvider: {terrain},
        imageryProvider: {imagery},
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
    cesium_version = attr.ib(default="1.88")
    ion_token = attr.ib(default="")
    terrain = attr.ib(default=TERRAIN["Ellipsoid"])
    imagery = attr.ib(default=IMAGERY["OSM"])

    _container_id = attr.ib(factory=uuid4)

    def build_script(self):
        return SCRIPT_TPL.format(
            cesium_version=self.cesium_version,
            czml=self.document.dumps(),
            container_id=self._container_id,
            ion_token=self.ion_token,
            terrain=self.terrain,
            imagery=self.imagery,
        )

    def to_html(self, widget_height="400px"):
        return CESIUM_TPL.format(
            cesium_version=self.cesium_version,
            script=self.build_script(),
            container_id=self._container_id,
            widget_height=widget_height,
        )

    def _repr_html_(self):
        return self.to_html()
