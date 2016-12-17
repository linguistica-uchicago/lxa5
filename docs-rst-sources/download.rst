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

To use the graphical user interface, PyQt5 and SIP are required:

.. code-block:: bash

   $ pip install sip PyQt5

To test the installation:

.. code-block:: python

   >>> import linguistica as lxa
   >>> lxa.__version__  # show version number

