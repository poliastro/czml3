:Name: czml3
:Author: Juan Luis Cano Rodríguez |orcid|

.. |orcid| image:: https://img.shields.io/badge/id-0000--0002--2187--161X-a6ce39.svg
   :target: http://orcid.org/0000-0002-2187-161X

.. |circleci| image:: https://img.shields.io/circleci/project/github/poliastro/czml3/master.svg?style=flat-square&logo=circleci
   :target: https://circleci.com/gh/poliastro/czml3

.. |codecov| image:: https://img.shields.io/codecov/c/github/poliastro/czml3.svg?style=flat-square
   :target: https://codecov.io/github/poliastro/czml3?branch=master

.. |license| image:: https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square
   :target: https://github.com/poliastro/czml3/raw/master/LICENSE

.. |matrix| image:: https://img.shields.io/matrix/poliastro-czml:matrix.org.svg?style=flat-square
   :alt: Join the chat at https://chat.openastronomy.org/#/room/#poliastro-czml:matrix.org
   :target: https://chat.openastronomy.org/#/room/#poliastro-czml:matrix.org

|circleci| |codecov| |license| |matrix|

czml3 is a Python library to write CZML.

What is CZML?
=============

[TODO]

Installation
============

You can install czml3 using pip::

  $ pip install czml3

czml3 requires Python >= 3.6. Would you like to help us
`supporting Python 3.5 <https://github.com/poliastro/czml3/pull/12>`_ as well?

Let us know if you want to lend a hand
by `making czml3 available on conda-forge <https://github.com/poliastro/czml3/issues/13>`_
too.

Examples
========

A CZML document is a list of *packets*, which have several properties.
When using czml3 in an interactive interpreter,
all objects show as nice CZML (JSON)::

  >>> from czml3 import Packet
  >>> Packet()
  {
      "id": "adae4d3a-7087-4fda-a70b-d18a262a890e"
  }
  >>> packet0 = Packet(id="Facility/AGI", name="AGI")
  >>> packet0
  {
      "id": "Facility/AGI",
      "name": "AGI"
  }
  >>> packet0.dumps()
  '{"id": "Facility/AGI", "name": "AGI"}'

Check out `the tests <https://github.com/poliastro/czml3/tree/master/tests>`_
to get an idea of the current capabilities of the library.

Support
=======

|matrix|

If you find any issue on czml3 or have questions,
please `open an issue on our repository <https://github.com/poliastro/czml3/issues/new>`_
and join `our chat`_!

.. _`our chat`: https://chat.openastronomy.org/#/room/#poliastro-czml:matrix.org

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

This will apply black, isort, and lots of love ❤️

License
=======

|license|

czml3 is released under the MIT license, hence allowing commercial
use of the library. Please refer to the :code:`LICENSE` file.
