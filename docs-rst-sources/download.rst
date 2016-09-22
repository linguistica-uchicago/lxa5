.. _download:

Download and install
====================

Linguistica 5 requires Python 3.4 or above.

Dependencies (see :ref:`deps` below for notes):

* `NumPy <http://www.numpy.org/>`_
* `SciPy <http://scipy.org/>`_
* `NetworkX <https://networkx.github.io/>`_
* `SIP <https://www.riverbankcomputing.com/software/sip/download>`_
  and
  `PyQt5 <https://www.riverbankcomputing.com/software/pyqt/download5>`_
  (both are optional; required for the graphical user interface)

Currently, Linguistica 5 is hosted on GitHub:

.. code-block:: bash

    $ git clone https://github.com/linguistica-uchicago/lxa5.git
    $ cd lxa5
    $ python setup.py install

The command ``python`` is meant to point to your Python 3 interpreter
(the one with NumPy, SciPy, and NetworkX installed).
Administrative privileges (such as ``sudo`` on Unix-like systems)
may be required.

To test the installation:

.. code-block:: python

   >>> import linguistica as lxa
   >>> lxa.__version__  # show version number


.. _deps:

Installing dependencies
-----------------------

**NumPy, SciPy, and NetworkX**:
Naturally, it is possible to install these packages one by one on your own,
though the installation process might be convoluted with
various potential issues regarding other dependencies, paths etc.

If you do not have any of these packages installed
(and especially if you do not have Python 3, either),
then we recommend using a Python distribution shipped with these required packages.
If you have
`Anaconda <https://www.continuum.io/downloads>`_ installed,
then these three packages are already available to you.
Due to the large size of Anaconda
(download > 300 MB; about 1.5 GB after installation),
`Miniconda <http://conda.pydata.org/miniconda.html>`_
(with Python and the ``conda`` program only without other packages)
is available.
With Miniconda installed, run ``conda install numpy scipy networkx``.

More notes regarding specific platforms or packages:

**Ubuntu** (for Linux users) already has the command ``python3`` pointing
to the Python 3 interpreter shipped with the operating system.
NumPy, SciPy, NetworkX, SIP, and PyQt5 are available through ``apt-get``:

.. code-block:: bash

   $ sudo apt-get install python3-numpy python3-scipy python3-networkx python3-sip python3-pyqt5 python3-pyqt5.qtwebkit


**SciPy dependencies**:
If you install the packages separately,
SciPy itself depends on NumPy, so it is recommended that NumPy is installed
before SciPy.
Depending on how you try to install SciPy,
the installation may also require other tools (e.g. a Fortran compiler):

* **Ubuntu:** Run
  ``sudo apt-get install libblas-dev liblapack-dev libatlas-base-dev gfortran``
* **Mac:** (assuming you have installed `Homebrew <http://brew.sh/>`_) Run
  ``brew install gcc``
* **Windows:** Consider using the
  `pre-built Windows installer for SciPy <http://www.lfd.uci.edu/~gohlke/pythonlibs/#scipy>`_
  by Christoph Gohlke.
