.. _codebase:

Codebase
========

This page gives a high-level overview of the Linguistica 5 codebase.
If you are from the Linguistica 5 project group, the page :ref:`dev`
provides the technical notes.

.. _codebase_structure:

Structure of the project repository
-----------------------------------

The Linguistica 5 codebase is hosted at https://github.com/linguistica-uchicago/lxa5.
The codebase can be concretely considered as a directory containing several
components:

* The Python library source code in the directory ``linguistica``.
  This is arguably the core of the codebase where most of the research and development
  efforts go.
  To get a sense of how the code works,
  please see :ref:`codebase_overview` below.

* :ref:`codebase_documentation`

* :ref:`codebase_continuous_integration`

* :ref:`codebase_tests`

* :ref:`codebase_setup_dot_py`

* :ref:`codebase_dependencies`

* :ref:`codebase_license`

* :ref:`codebase_readme`

Developers of the Linguistica project shall consult the page :ref:`dev` for
setting up their environment.


.. _codebase_overview:

Overview
--------

How does the Linguistica 5 code work in general?
We get a good sense of it by understanding how the code gets us a dictionary of
signatures to stems:

.. code:: python

    >>> import linguistica as lxa
    >>> from linguistica.datasets import brown
    >>> lxa_object = lxa.read_corpus(brown)
    >>> sigs_to_stems = lxa_object.signatures_to_stems()

This overview walks through what happens under the hood
when this code snippet is run.

``brown`` is a string which is the path pointing to the Brown corpus that comes
with the Linguistica 5 library on your local disk.

``lxa_object`` (created by ``lxa.read_corpus(brown)``) is an instance of the class
``Lexicon`` defined in ``linguistica/lexicon.py``.
``Lexicon`` has many methods, one of which is ``signatures_to_stems()``.

What is the magic behind ``lxa_object.signatures_to_stems()``
which returns a dict of signatures to stems?
The answer lies in the design of the class ``Lexicon``.
Given the definition of the class is fairly long, we will examine it step by step,
unfolding only the relevant bits as we move along:

.. code::

    class Lexicon:

        def __init__(self, ...):

            self._initialize()

        def _initialize(self):

            # signature-related objects
            self._signatures_to_stems = None

When we create a Linguistica object by the line ``lxa_object = lxa.read_corpus(brown)``,
an instance of the class ``Lexicon`` is created.
When this instance is created, ``__init__()`` is called.
``__init__()`` initializes several attributes (those in the form of ``self.X``)
and triggers the method ``_initialize()``.

What does ``_initialize()`` do? It initializes all objects of interest.
Most of them are initialized as ``None``, like ``_signatures_to_stems``
as shown here. Very soon we will see why we need ``_signatures_to_stems``
(named with a leading underscore so that it is a private attribute),
and why it is default to ``None``.

Now that all initialization work is done and ``lxa_object`` is ready in the memory,
we examine what happens when the final line
``sigs_to_stems = lxa_object.signatures_to_stems()`` in the code snippet is run.

When ``lxa_object.signatures_to_stems()`` is called, the method
``signatures_to_stems()`` of the ``Lexicon`` class is called.
What does this method do? Let's check out the code:

.. code::

    class Lexicon:

        def signatures_to_stems(self):
            """
            Return a dict of morphological signatures to stems.

            :rtype: dict(tuple(str): set(str))
            """
            if self._signatures_to_stems is None:
                self._make_all_signature_objects()
            return self._signatures_to_stems

        def _make_all_signature_objects(self):
            self._stems_to_words = signature.make_stems_to_words(
                self.wordlist(), self.parameters_['min_stem_length'],
                self.parameters_['max_affix_length'], self.parameters_['suffixing'],
                self.parameters_['min_sig_count'])

            self._signatures_to_stems = signature.make_signatures_to_stems(
                self._stems_to_words, self.parameters_['max_affix_length'],
                self.parameters_['min_sig_count'], self.parameters_['suffixing'])

            ...

When ``signatures_to_stems()`` is called, an if statement is first executed.
The condition of this if statement, ``self._signatures_to_stems is None``,
evaluates to ``True``, because ``self._signatures_to_stems`` has just been
initialized to be ``None``. Then ``self._make_all_signature_objects()`` is
executed (more on this below).
When it finishes, ``self._signatures_to_stems`` holds the expected
dict (no longer ``None``) and is returned.
(If ``signatures_to_stems()`` is called again, ``self._signatures_to_stems``
is not ``None`` anymore and the expensive computation at ``self._make_all_signature_objects()``
is avoided. This explains why in general the Linguistica 5 code has the distinction
between the private attribute ``self._x`` and the public method ``self.x()``
for most objects of interest).

So, what is the method ``self._make_all_signature_objects()``? As its name suggests,
it makes all signature-related ``self._x``. In the code shown above,
two of these ``self._x`` are shown, including ``self._signatures_to_stems``.
The order by which these ``self._x`` is computed matters,
because there is dependency among them. For example, ``self._signatures_to_stems``
depends on ``self._stems_to_words`` just computed in the same method.

We are potentially interested in many of the intermediate objects for
research purposes. In our example, ``self._stems_to_words`` is intermediate
for the computation of ``self._signatures_to_stems``, but we expose it
(by making it ``self._x`` as well as allowing the ``self.x()`` API access)
because a mapping from stems to words is of interest.

To compute ``self._x`` in ``_make_all_signature_objects()``, many function calls
in the form of ``signature.make_x()`` are made. Here, ``signature`` refers
to the imported module, and all the function calls ``make_x()`` are defined
in ``linguistica/signature.py``.

So this is essentially how objects of interest are created via the ``Lexicon``
class. They are initialized in some way and are *not* actually
computed until necessary. Once computed, they are available in memory for
immediate retrieval. All heavy lifting is only called but not done within
the class ``Lexicon`` -- the real work is done in the respective modules
such as ``signature``, ``manifold``, and so on.


.. _codebase_documentation:

Documentation
-------------

Using Sphinx. More notes needed here.

changelog.md

build-doc.sh


.. _codebase_continuous_integration:

Continuous integration
----------------------

, .travis.yml, .coveragerc

* We take advantage of continuous integration to:

  * test whether the Linguistica 5 library can be successfully installed
  * check if all tests pass
  * measure test coverage
  * ensure that the codebase is compliant with PEP 8 coding style conventions

* The images for various continuous integration elements are directly shown
  at the top of ``readme.rst``. So be sure everything works and looks great
  at all times!

* We use `Travis-CI <https://travis-ci.org/>`_ to test the library installation
  as hosted on GitHub.
  ``.travis.yml`` in the repository provides the instructions for Travis CI to
  run the tests whenever a commit is pushed to the ``master`` branch.
  Under no circumstances can build tests be marked as "fail".

* We use `coveralls <https://coveralls.io/>`_ to measure test coverage.
  ``.travis.yml`` and ``.coveragerc`` configure the measurement and reportage.
  Under no circumstances can test coverage drop below 95%.

* ``.travis.yml`` runs ``ci/travis_install.sh`` to install all library
  dependencies and packages for testing. We use Miniconda for faster
  downloading
  (apt-get is sometimes too slow and there's a 50-minute cap for build tests
  on Travis CI).

* We use `landscape.io <https://landscape.io>`_ to check code health for
  ensuring the codebase abides by the PEP 8 coding style conventions.
  Under no circumstances can code health drop below 95%.

.. _codebase_tests:

Tests
-----

* Install the packages needed for testing. Run
  ``sudo python3 -m pip -r test_requirements.txt``.

* We use ``nose`` as the testing framework.
  To run tests, run ``python3 nosetests_run.py``.

* Run ``python3 nosetests_run.py``
  as often as possible to ensure nothing has broken.
  In particular, it must be run before *and* after each coding session.

* All testing-related files and scripts are in the directory ``tests``.

* ``tests/data`` contains all expected outputs rendered
  as Python literals, plus the corpus file ``english-brown.txt``.
  All scripts in ``tests`` are named ``test_X.py`` so that ``nose`` can
  recognize them. All tests are functions named ``test_X()``.

* All tests must be explicitly written as the ``test_X()`` functions in the
  ``test_X.py`` scripts.
  We do *NOT* use docstrings in the library code for the
  purposes of library testing.

* Note that ``tests`` are **NOT** included in the library under the directory
  ``linguistica``. This means that ``tests`` is available only through
  the GitHub repository and is not included in the library installation.
  This structure is intentional, because ``tests`` is only for the developers
  but not the users, and ``tests`` contains large files that the users
  wouldn't need.


* ``words_to_neighbors``:
  Syntactic word neighbor computation appears to be sensitive to the precise
  versions of NumPy and SciPy being used.
  This affects the precise word
  neighbors found. Since an exact match of neighbors between the test and
  expected results is *not* critical ("close enough" would do), the
  test for ``words_to_neighbors`` is intentionally lenient.


.. _codebase_setup_dot_py:

``setup.py``
------------


.. _codebase_dependencies:

Dependencies
------------

requirements.txt


.. _codebase_license:

License
-------

LICENSE.txt


.. _codebase_readme:

Readme
------

rst rather than markdown is used
because this is to be read as the
long description in ``setup.py``,
and PyPI recognizes rst but not markdown
to render the text formatting.


Version
-------

A plain text file that specifies the version number -- currently ``5.1.0``.

Defined in `linguistica/VERSION` and nowhere else.

* **Version number:** We follow http://semver.org/ for the ``major.minor.patch``
  format.
  The current version is ``5.1.0``.
  The major version is ``5`` because there's John's Linguistica 3 & 4
  written in C++.
  The minor version is ``1`` rather than ``0`` because John has his in-house
  ``5.0`` written in Python 2 circa/before 2012.
  The version number is specified in ``linguistica/VERSION`` (and nowhere else).


Graphical user interface
------------------------

(To be updated)

* Because SIP and PyQt5 are required for the GUI but their installation
  is possibly non-trivial, they are designated as *optional* dependencies
  for Linguistica 5 (the GUI is not an absolute must-have for Linguistica 5
  to work).

* The GUI code is in ``linguistica/gui``. The GUI is launched by
  calling ``linguistica.gui.main()`` in ``linguistica/__main__.py``.

* All GUI code is accessible through only ``linguistica.gui.main()``
  defined in ``linguistica/gui/__init__.py``.
  This is important, because PyQt5 may potentially be unavailable
  at the user's system. The ``__init__.py`` safeguards against import errors,
  but other ``.py`` files in ``linguistica/gui`` do not.
  Relatedly, when ``linguistica.gui.main()`` is to be called
  (as in ``linguistica/__main__.py``), there is always code that checks
  whether PyQt5 is importable before ``linguistica.gui.main()`` can
  actually be called.


Command line interface
----------------------

(To be updated)

* The CLI code is in ``linguistica/cli.py``, all wrapped in
  ``linguistica.cli.main()`` called in ``linguistica/__main__.py``.

* We don't output ``words_to_contexts``
  and ``contexts_to_words``, because they are huge...
  Or we could just output those whose counts are higher than some threshold?



``linguistica/__main__.py``
---------------------------

For running GUI and CLI


``linguistica/__init__.py``
---------------------------

``__init__.py`` sets up the functions for reading data.


``linguistica/release.py``
--------------------------

Metadata of the library (version etc)


``linguistica/util.py``
-----------------------

Constants and various utility functions.


``linguistica/lexicon.py``
--------------------------

The ``Lexicon`` class.


``linguistica/ngram.py``
------------------------

This ``ngram`` module is to get the word ngrams.


``linguistica/signature.py``
----------------------------

* Morphological signatures should really be sets, but they are tuples
  (e.g. ``('NULL', 's')``) with affixes ordered alphabetically.
  The signatures are very often the keys in some dicts, and Python doesn't
  allow sets to be dict keys...


``linguistica/phon.py``
-----------------------

The ``phon`` module is to perform various phonology-related computations.


``linguistica/trie.py``
-----------------------

Left-to-right and right-to-left tries. Successors. Predecessors.


``linguistica/manifold.py``
---------------------------

Syntactic word neighbors


``linguistica/fsm.py``
----------------------

(Forthcoming)
