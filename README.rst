Linguistica 5
=============

.. image:: https://badge.fury.io/py/linguistica.svg
   :target: https://pypi.python.org/pypi/linguistica
   :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/linguistica.svg
   :target: https://pypi.python.org/pypi/linguistica
   :alt: Supported Python versions

.. image:: https://img.shields.io/pypi/wheel/linguistica.svg
   :target: https://pypi.python.org/pypi/linguistica
   :alt: Wheel

.. image:: https://travis-ci.org/linguistica-uchicago/lxa5.svg?branch=master
   :target: https://travis-ci.org/linguistica-uchicago/lxa5
   :alt: Build

.. image:: https://landscape.io/github/linguistica-uchicago/lxa5/master/landscape.svg?style=flat
   :target: https://landscape.io/github/linguistica-uchicago/lxa5/master
   :alt: Code Health

Linguistica 5 is a Python library for unsupervised learning
of linguistic structure.

Full documentation: http://linguistica-uchicago.github.io/lxa5/

Apart from being a Python library, Linguistica 5 provides two additional
interfaces: (i) graphical user interface; (ii) command line interface.

Work by Jackson Lee and John Goldsmith


Please note that this code (Linguistica 5) is not John Goldsmith's development code,
which can be found on
`his GitHub repository <https://github.com/JohnAGoldsmith/lxa5_0>`_.
The most recent release of John Goldsmith's code is Linguistica 4; see
`Linguistica at UChicago <http://linguistica.uchicago.edu/>`_.


Download and install
--------------------

Linguistica 5 is available through ``pip``:

.. code-block:: bash

   $ pip install linguistica

Linguistica 5 works with Python 2.7 and 3.4+.

To use the graphical user interface, only Python 3 is supported.
In addition, PyQt5 and SIP are required.
PyQt5 is readily available from ``pip``:

.. code-block:: bash

   $ pip install PyQt5

At the time of writing (April 2017), SIP is best downloaded and installed from
`its source <http://pyqt.sourceforge.net/Docs/sip4/installation.html>`_.
(SIP is available through ``pip``, but it does not include
the C/C++ code generator for PyQt5.)


Using Linguistica 5
-------------------

To use Linguistica 5 as a Python library, simply import ``linguistica``
in your Python programs:

.. code-block:: python

   import linguistica as lxa

Quick library demo `here <http://linguistica-uchicago.github.io/lxa5/demo.html>`_.

To launch the Linguistica 5 graphical user interface
(with SIP and PyQt5 installed):

.. code-block:: bash

   $ linguistica gui

To launch the Linguistica 5 command line interface:

.. code-block:: bash

   $ linguistica cli


Citation
--------

If you use Linguistica 5, please cite this paper::

   @InProceedings{lee-goldsmith:2016:lxa5,
     author    = {Lee, Jackson L. and Goldsmith, John A.},
     title     = {Linguistica 5: Unsupervised Learning of Linguistic Structure},
     booktitle = {Proceedings of the 2016 Conference of the North American Chapter of the Association for Computational Linguistics},
     month     = {June},
     year      = {2016},
     address   = {San Diego, California},
     publisher = {Association for Computational Linguistics},
     pages     = {22--26},
     url       = {http://www.aclweb.org/anthology/N16-3005}
   }


Source code
-----------

The source code of Linguistica 5 is officially released on PyPI: https://pypi.python.org/pypi/linguistica

It is also hosted on GitHub, possibly with work in progress: https://github.com/linguistica-uchicago/lxa5


Technical support
-----------------

Please `open issues <https://github.com/linguistica-uchicago/lxa5/issues/new>`_
for questions and bug reports.
Alternatively, please feel free to contact
`Jackson Lee <http://jacksonllee.com/>`_ and
`John Goldsmith <http://people.cs.uchicago.edu/~jagoldsm/>`_.


License
-------

MIT License

See ``LICENSE.txt`` on the `GitHub repository <https://github.com/linguistica-uchicago/lxa5>`_.
