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

* :ref:`codebase_dependencies`

* :ref:`codebase_tests`

* :ref:`codebase_continuous_integration`

* :ref:`codebase_setup_dot_py`

* :ref:`codebase_readme`

* :ref:`codebase_version`

* :ref:`codebase_documentation`


Developers of the Linguistica project shall consult the page :ref:`dev` for
set-up and workflow.


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

.. code:: python

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

.. code:: python

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

Notes on the graphicsl user interface (GUI):

* The GUI is Python 3 only. The main reason is tha the GUI requires PyQt5 (and
  SIP), and PyQt5 appears to be Python 3 only (at least officially?).

* Because SIP and PyQt5 are required for the GUI but their installation
  is possibly non-trivial. They are designated as *optional* dependencies
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


Notes on the command line interface (CLI):

* The CLI code is in ``linguistica/cli.py``, all wrapped in
  ``linguistica.cli.main()`` which is called in ``linguistica/__main__.py``.

* We don't output ``words_to_contexts``
  and ``contexts_to_words``, because they are huge...
  Or we could just output those whose counts are higher than some threshold?


.. _codebase_dependencies:

Dependencies
------------

The core dependencies are specified in ``requirements.txt`` which is read by
``setup.py`` and used in build tests by Travis CI.
For reproducibility, we pin down each dependency's major and minor version
numbers, while allowing flexibility for getting bug fixes.
For example, ``six>=1.10.0,<=1.10.99`` points to the latest six v1.10.x.

There is also ``dev-requirements.txt`` with dependencies for running tests and
code quality checks. Travis CI uses this file for build tests.
It is recommended that developers and administrators of the Linguistica 5
also install these dependencies and use them for maintaining high code quality.


.. _codebase_tests:

Tests
-----

We use ``pytest`` as the testing framework. Developers and administrators
should install the dependencies for running tests:
``$ pip install -r dev-requirements``

Run tests as often as you can. In particular, it must be run before *and*
after each coding session:
``$ pytest -vv --cov linguistica linguistica``.
``-vv`` outputs a verbose test report. ``--cov linguistica`` means that we
check test coverage for ``.py`` files under the directory ``linguistica``
(so just the library code). Lastly, the second ``linguistica`` in the command
specifies the directory (again, the library code) where pytest should look for
tests in ``test_*.py``. ``.coveragerc`` configures the test coverage report.

We are also using ``flake8`` for maintaining high code quality. Essentially,
no PEP8 violations are allowed -- not even trailing whitespace or extra
empty lines. Run flake8 with ``$ flake8 linguistica``. If you see no
terminal output, it means everything is compliant. Note that the Travis CI
build tests also run flake8. Do not try to work around the robots!


.. _codebase_continuous_integration:

Continuous integration
----------------------

The Linguistica 5 repository is set up with Travis CI for automatically
running build tests for all pull requests. The configuration is in
``.travis.yml``. We take advantage of continuous integration to:

  * test whether the Linguistica 5 library can be successfully installed
  * check if all tests pass
  * ensure that the codebase is compliant with PEP 8 coding style conventions

Build tests are run for all supported Python versions (2.7 and 3.4+).


.. _codebase_setup_dot_py:

``setup.py``
------------

``setup.py`` installs the Linguistica 5 library. It also specifies the metadata
of the library (displayed on the PyPI site). Developers and administrators
are recommended to install Linguisitca 5 with ``$ python setup.py develop``
for development purposes.


.. _codebase_readme:

Readme
------

The readme, ``README.rst``, is in reStructuredText instead of Markdown,
simply because PyPI
does not seem to render Markdown mark-up for the ``long_description`` in
``setup.py``.

``readme-dev.md`` contains notes for the administrators of the Linguistica 5
project.


.. _codebase_version:

Version
-------

The version number is specified in the text file `linguistica/VERSION` and
nowhere else. The version number in both ``setup.py`` and
``linguistica.__version__`` points to this text file. It is important to
**not** hard-code or even mention the current version number anywhere else
(not even in the source ``.rst`` of this documentation) to avoid confusion.

We essentially follow http://semver.org/ for the ``major.minor.patch``
format. The major version is ``5`` because there's John's Linguistica 3 & 4
written in C++. The minor version number increments when a new release comes
with new features. The patch number increments when a new release comes with
changes with no API ramifications such as bug fixes.

The first release of Linguistica 5 was 5.1.0 instead of 5.0.0, because 5.0.0
was John's in-house version written in Python 2.


.. _codebase_documentation:

Documentation
-------------

We use Sphinx as the documentation framework, as it is the official tool for
Python projects (including the docs of the Python language itself).
The source files (in the reStructuredText mark-up language) are in
``docs/sources/``. These source files are what generates the ``docs/*.html``
files, which GitHub renders as the documentation website
(= what you are reading now). To update the HTML files after the source
``.rst`` files are updated, run ``$ sh build-doc.sh``.


Changes (new features, bug fixes) together with new version releases
should be documented in ``CHANGELOG.md``.
