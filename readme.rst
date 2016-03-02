Linguistica 5
=============

.. image:: https://travis-ci.org/linguistica-uchicago/lxa5.svg?branch=master
    :target: https://travis-ci.org/linguistica-uchicago/lxa5

.. image:: https://coveralls.io/repos/github/linguistica-uchicago/lxa5/badge.svg?branch=master
    :target: https://coveralls.io/github/linguistica-uchicago/lxa5?branch=master

Linguistica 5 is a Python library for unsupervised learning
of linguistic structure, based on Goldsmith (2001, 2006) and all subsequent
developments.

Full documentation: http://linguistica-uchicago.github.io/lxa5/

Apart from being a Python library, Linguistica 5 provides two additional
interfaces: (i) graphical user interface; (ii) command line interface.

Work by Jackson Lee and John Goldsmith


Download and install
--------------------

Linguistica 5 requires Python 3.4 or above.

Dependencies:

* `NumPy <http://www.numpy.org/>`_
* `SciPy <http://scipy.org/>`_
* `NetworkX <https://networkx.github.io/>`_
* `SIP <https://www.riverbankcomputing.com/software/sip/download>`_
  and
  `PyQt5 <https://www.riverbankcomputing.com/software/pyqt/download5>`_
  (both are optional; required for the graphical user interface)

.. note::
   **SciPy dependencies** --
   SciPy itself depends on NumPy, so it is recommended that NumPy is installed
   before SciPy.
   Depending on how you try to install SciPy,
   the installation may also require other tools (e.g. a Fortran compiler):

   * **Linux:** (for Ubuntu) run
     ``sudo apt-get install libblas-dev liblapack-dev libatlas-base-dev gfortran``
   * **Mac:** (assuming you have installed `Homebrew <http://brew.sh/>`_) run
     ``brew install gcc``
   * **Windows:** Consider simply using the
     `pre-built Windows installer for SciPy <http://www.lfd.uci.edu/~gohlke/pythonlibs/#scipy>`_
     by Christoph Gohlke so that you don't have to worry about the dependencies

.. note::
   **SIP and PyQt5 installation** --

   * **Linux:** (for Ubuntu) run
     ``sudo apt-get install python3-sip python3-pyqt5 python3-pyqt5.qtwebkit``
   * **Mac:** [notes forthcoming]
   * **Windows:** [notes forthcoming]

Be sure that all these packages are installed for the Python 3
distribution with which you plan to use Linguistica 5.

Currently, Linguistica 5 is hosted on GitHub:

.. code-block:: bash

    $ git clone https://github.com/linguistica-uchicago/lxa5.git
    $ cd lxa5
    $ python3 setup.py install

``python3`` is meant to point to your Python 3 interpreter.
Administrative privileges (such as ``sudo`` on Unix-like systems)
may be required.


Using Linguistica 5
-------------------

To use Linguistica 5 as a Python library, simply import ``linguistica``
in your Python programs:

.. code-block:: python

   import linguistica as lxa

To launch the Linguistica 5 graphical user interface:

.. code-block:: bash

   $ python3 -m linguistica gui

To launch the Linguistica 5 command line interface:

.. code-block:: bash

   $ python3 -m linguistica cli
