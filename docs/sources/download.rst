.. _download:

Download and install
====================

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

To test the installation:

.. code-block:: python

   >>> import linguistica as lxa
   >>> lxa.__version__  # show version number

