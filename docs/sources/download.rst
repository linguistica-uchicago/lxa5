.. _download:

Download and install
====================

Linguistica 5 is available through ``pip``:

.. code-block:: bash

   $ pip install linguistica

Linguistica 5 requires Python 3.4 or above. Core dependencies are NumPy, SciPy, and NetworkX.
If you encounter issues in installing these dependencies,
consider using the Python distribution `Anaconda <https://www.continuum.io/downloads>`_
(or `Miniconda <http://conda.pydata.org/miniconda.html>`_)
with these dependencies installed.

To use the graphical user interface, PyQt5 and SIP are required.
PyQt5 is readily available from ``pip``:

.. code-block:: bash

   $ pip install PyQt5

At the time of writing (March 2017), SIP is best downloaded and installed from
`its source <http://pyqt.sourceforge.net/Docs/sip4/installation.html>`_.
(SIP is available through ``pip``, but it does not include
the C/C++ code generator for PyQt5.)

To test the installation:

.. code-block:: python

   >>> import linguistica as lxa
   >>> lxa.__version__  # show version number

