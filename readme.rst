Linguistica 5
=============

.. image:: https://travis-ci.org/linguistica-uchicago/lxa5.svg?branch=master
   :target: https://travis-ci.org/linguistica-uchicago/lxa5

.. image:: https://coveralls.io/repos/github/linguistica-uchicago/lxa5/badge.svg?branch=master
   :target: https://coveralls.io/github/linguistica-uchicago/lxa5?branch=master

.. image:: https://landscape.io/github/linguistica-uchicago/lxa5/master/landscape.svg?style=flat
   :target: https://landscape.io/github/linguistica-uchicago/lxa5/master
   :alt: Code Health

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


Using Linguistica 5
-------------------

To use Linguistica 5 as a Python library, simply import ``linguistica``
in your Python programs:

.. code-block:: python

   import linguistica as lxa

To launch the Linguistica 5 graphical user interface
(with SIP and PyQt5 installed):

.. code-block:: bash

   $ python -m linguistica gui

To launch the Linguistica 5 command line interface:

.. code-block:: bash

   $ python -m linguistica cli


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
   }


Technical support
-----------------

Please `open issues <https://github.com/linguistica-uchicago/lxa5/issues/new>`_
for questions and bug reports.
Alternatively, please feel free to contact
`Jackson Lee <http://jacksonllee.com/>`_ and
`John Goldsmith <http://people.cs.uchicago.edu/~jagoldsm/>`_.

.. _deps:

Dependencies
------------

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
