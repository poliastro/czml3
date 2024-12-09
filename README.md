# czml3
![pypi](https://img.shields.io/pypi/v/czml3)
![conda](https://img.shields.io/conda/vn/conda-forge/czml3?label=conda)
![Python](https://img.shields.io/pypi/pyversions/czml3)
![codecov](https://img.shields.io/codecov/c/github/poliastro/czml3.svg?style=flat-square)
![pypi-downloads](https://img.shields.io/pepy/dt/czml3?label=pypi%20downloads)
![conda-downloads](https://img.shields.io/conda/dn/conda-forge/czml3?label=conda%20downloads)
![workflow-status](https://img.shields.io/github/actions/workflow/status/poliastro/czml3/workflow.yml?branch=main)
![license](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)

czml3 aims to make the process of writing CZML files in Python easy by:
- Type checking properties
- Conversion of properties to their expected format

From the official [CZML Guide](https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/CZML-Guide):
> CZML is a JSON format for describing a time-dynamic graphical scene, primarily for display in a web browser running Cesium. It describes lines, points, billboards, models, and other graphical primitives, and specifies how they change with time.

## Insallation
You can install czml3 using pip:
```
pip install czml3
```

or conda:
```
conda install czml3 --channel conda-forge
```

## Examples
A CZML document is a list of *packets*, which have several properties. Recreating the blue box from Cesium sandcastle's [CZML Box](https://sandcastle.cesium.com/?src=CZML%20Box.html&label=CZML):

```
from czml3 import Document, Packet, Preamble
from czml3.properties import (
    Box,
    BoxDimensions,
    Cartesian3Value,
    Color,
    Material,
    Position,
    SolidColorMaterial,
)
packet_box = Packet(
    position=Position(cartographicDegrees=[-114.0, 40.0, 300000.0]),
    box=Box(
        dimensions=BoxDimensions(
            cartesian=Cartesian3Value(values=[400000.0, 300000.0, 500000.0])
        ),
        material=Material(
            solidColor=SolidColorMaterial(color=Color(rgba=[0, 0, 255, 255]))
        ),
    ),
)
doc = Document(packets=[Preamble(name="box"), packet_box])
print(doc)
```
```
[
    {
        "id": "document",
        "version": "1.0",
        "name": "box"
    },
    {
        "id": "b9f211b1-6e9d-45b2-b484-516d127ffa22",
        "position": {
            "cartographicDegrees": [
                -114.0,
                40.0,
                300000.0
            ]
        },
        "box": {
            "dimensions": {
                "cartesian": [
                    400000.0,
                    300000.0,
                    500000.0
                ]
            },
            "material": {
                "solidColor": {
                    "color": {
                        "rgba": [
                            0.0,
                            0.0,
                            255.0,
                            255.0
                        ]
                    }
                }
            }
        }
    }
]
```

czml3 uses [pydantic](https://docs.pydantic.dev/latest/) for all classes. As such czml3 automatically converts some properties to their appropriate type. For example, the following creates a Position property of doubles using a numpy array of interger type:
```
import numpy as np
from czml3.properties import Position
print(Position(cartographicDegrees=np.array([-114, 40, 300000], dtype=int)))
```
```
{
    "cartographicDegrees": [
        -114.0,
        40.0,
        300000.0
    ]
}
```

## Jupyter Widget
You can easily display your CZML document using our interactive widget:
```
from czml3.examples import simple
from czml3.widget import CZMLWidget
CZMLWidget(simple)
```
![Widget](https://raw.githubusercontent.com/poliastro/czml3/master/widget-screenshot.png)

## Contributing
You want to contribute? Awesome! There are lots of [CZML properties](https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Packet) that we still did not implement. Also, it would be great to have better validation, a Cesium widget in Jupyter notebook and JupyterLab... Ideas welcome!

Before you send us a pull request, remember to reformat all the code: `tox -e reformat`. This will apply ruff and lots of love ❤️