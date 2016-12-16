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

   $ pip install -r requirements-gui.txt


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


For development
---------------

The Linguistica 5 code that may contain work in progress is hosted on GitHub:

.. code-block:: bash

    $ git clone https://github.com/linguistica-uchicago/lxa5.git
    $ cd lxa5
    $ python setup.py install

For development, you may probably want to use the ``develop`` option instead of ``install``
when running ``setup.py``. Also, install the dependencies for testing and documentation:

.. code-block:: bash

   $ pip install -r requirements-dev.txt

To run tests:

.. code-block:: bash

   $ pytest -v --cov


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


Technical support
-----------------

Please `open issues <https://github.com/linguistica-uchicago/lxa5/issues/new>`_
for questions and bug reports.
Alternatively, please feel free to contact
`Jackson Lee <http://jacksonllee.com/>`_ and
`John Goldsmith <http://people.cs.uchicago.edu/~jagoldsm/>`_.
