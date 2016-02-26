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
* `PyQt5 <https://www.riverbankcomputing.com/software/pyqt/download5>`_
  (for the graphical user interface; including the WebKit module)

.. note::
   Linux users -- SciPy has its own dependencies. If you are on Ubuntu,
   run this before installing SciPy:
   ``sudo apt-get install libblas-dev liblapack-dev libatlas-base-dev gfortran``

.. note::
   PyQt5 -- Ubuntu users can install it by running this:
   ``sudo apt-get install python3-sip python3-pyqt5 python3-pyqt5.qtwebkit``

NumPy, SciPy, and NetworkX are conveniently available via ``pip``
(and will be automatically installed when Linguistica 5 is installed,
if they are absent on your system).

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
