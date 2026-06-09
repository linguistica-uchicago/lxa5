.. _download:

Download and install
====================

Linguistica 5 is available through ``pip``:

.. code-block:: bash

   pip install linguistica

Linguistica 5 works with Python 3.12+.

The graphical user interface (GUI) requires ``PyQt5`` and ``PyQtWebEngine`` (the latter
powers the word-neighbor manifold visualization). Install them together with the
``gui`` extra:

.. code-block:: bash

   pip install "linguistica[gui]"

These install as binary wheels on x86_64 Linux, Windows, and macOS (including Apple
Silicon).
On aarch64 Linux or Alpine/musl, where wheels are not published, ``pip`` may build
from source instead.

To test the installation:

.. code-block:: python

   >>> import linguistica as lxa
   >>> lxa.__version__  # show version number
