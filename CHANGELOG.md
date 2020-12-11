# v0.5.4

* Add several new properties: `ViewFrom`, `Box`, `Corridor`,
  `Cylinder`, `Ellipse`, `Ellipsoid`, `TileSet`, `Wall`
* Add new materials: `PolylineOutlineMaterial`, `PolylineGlowMaterial`,
  `PolylineArrowMaterial`, `PolylineDashMaterial`
* Add `Position.cartesianVelocity`, `Billboard.eyeOffset`, and
  `Label.pixelOffset`
* Add utilities to create and validate colors: `Color.is_valid`,
  `utils.get_color_list`
* Other minor additions and bug fixes

Thanks to all contributors!

- Clément Jonglez
- Eleftheria Chatziargyriou
- Idan Miara
- Joris Olympio
- Juan Luis Cano Rodríguez
- Michael Haberler

# v0.5.3

* Add `Rectangle` and `RectangleCoordinates`

# v0.5.2

* Fix packaging

# v0.5.1

* Fix widget for non-local Jupyter notebook deployments

# v0.5.0

* Upgrade for Cesium 1.64
* Allow for custom Ion access tokens
* Fix HTML output

# v0.4.0

* Rewrite internals using `attrs`!
* Properly support packet comparison
* Use unique container ids for the CZML widget
* New properties `Model` and `Orientation`
* New type `UnitQuaternionValue`
* Some new enumerations

# v0.3.0

* Changelog!
* General improvements in README
* New `CZMLWidget` to display a Cesium window in Jupyter
* New `czml3.examples` with some more complex CZML examples
* New properties `Box`, `BoxDimensions`, `EyeOffset`
* New `czml3.utils.get_color`
* Stricter validation for `Position`
