:Name: czml3
:Authors: Juan Luis Cano Rodríguez, Eleftheria Chatziargyriou

.. |circleci| image:: https://img.shields.io/circleci/project/github/poliastro/czml3/master.svg?style=flat-square&logo=circleci
   :target: https://circleci.com/gh/poliastro/czml3

.. |codecov| image:: https://img.shields.io/codecov/c/github/poliastro/czml3.svg?style=flat-square
   :target: https://codecov.io/github/poliastro/czml3?branch=master

.. |license| image:: https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square
   :target: https://github.com/poliastro/czml3/raw/master/LICENSE

.. |matrix| image:: https://img.shields.io/matrix/poliastro-czml:matrix.org.svg?style=flat-square
   :alt: Join the chat at https://openastronomy.riot.im/#/room/#poliastro-czml:matrix.org
   :target: https://openastronomy.riot.im/#/room/#poliastro-czml:matrix.org

|circleci| |codecov| |license| |matrix|

czml3 is a Python library to write CZML.

What is CZML?
=============

From the official
`CZML Guide <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/CZML-Guide>`_:

  CZML is a JSON format for describing a time-dynamic graphical scene,
  primarily for display in a web browser running Cesium.
  It describes lines, points, billboards, models, and other graphical primitives,
  and specifies how they change with time.
  While Cesium has a rich client-side API,
  CZML allows it to be data-driven
  so that a generic Cesium viewer can display a rich scene
  without the need for any custom code.

Installation
============

You can install czml3 using pip::

  $ pip install czml3

or conda::

  $ conda install czml3 --channel conda-forge

czml3 requires Python >= 3.7.

Examples
========

A CZML document is a list of *packets*, which have several properties.
When using czml3 in an interactive interpreter,
all objects show as nice CZML (JSON)::

  >>> from czml3 import Packet
  >>> print(Packet())
  {
      "id": "adae4d3a-7087-4fda-a70b-d18a262a890e"
  }
  >>> packet0 = Packet(id="Facility/AGI", name="AGI")
  >>> print(packet0)
  {
      "id": "Facility/AGI",
      "name": "AGI"
  }
  >>> packet0.dumps()
  '{"id": "Facility/AGI", "name": "AGI"}'

And there are more complex examples available::

  >>> from czml3.examples import simple
  >>> print(simple)
  [
      {
          "id": "document",
          "version": "1.0",
          "name": "simple",
          "clock": {
              "interval": "2012-03-15T10:00:00Z/2012-03-16T10:00:00Z",
              "currentTime": "2012-03-15T10:00:00Z",
              "multiplier": 60,
              "range": "LOOP_STOP",
              "step": "SYSTEM_CLOCK_MULTIPLIER"
          }
      },
  ...

Jupyter widget
--------------

You can easily display your CZML document using our interactive widget::

  In [1]: from czml3.examples import simple

  In [2]: from czml3.widget import CZMLWidget

  In [3]: CZMLWidget(simple)

And this would be the result:

.. image:: https://raw.githubusercontent.com/poliastro/czml3/master/widget-screenshot.png

Support
=======

|matrix|

If you find any issue on czml3 or have questions,
please `open an issue on our repository <https://github.com/poliastro/czml3/issues/new>`_
and join `our chat`_!

.. _`our chat`: https://openastronomy.riot.im/#/room/#poliastro-czml:matrix.org

Contributing
============

You want to contribute? Awesome! There are lots of
`CZML properties <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Packet>`_
that we still did not implement. Also, it would be great to have
better validation, a Cesium widget in Jupyter notebook and JupyterLab...
Ideas welcome!

We recommend `this GitHub workflow <https://www.asmeurer.com/git-workflow/>`_
to fork the repository. To run the tests,
use `tox <https://tox.readthedocs.io/>`_::

  $ tox

Before you send us a pull request, remember to reformat all the code::

  $ tox -e reformat

This will apply ruff and lots of love ❤️

License
=======

|license|

czml3 is released under the MIT license, hence allowing commercial
use of the library. Please refer to the :code:`LICENSE` file.
