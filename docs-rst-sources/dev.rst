.. _dev:

For developers
==============

These notes record various details and potential gotchas regarding
the source code of Linguistica 5.
They should be helpful for the core developers of
Linguistica 5 or whoever would like to mess with the code.
At the moment the notes are added onto this page as they pop up in the mind of
the Linguistica 5 developers, and are revamped in a more organized form
from time to time.

All notes here assume that you are at the project root directory ``lxa5``:

.. code-block:: bash

   $ git clone http://github.com/linguistica-uchicago/lxa5.git
   $ cd lxa5

This is important, as all references to commands, paths, files etc depend on it.

The command ``python3`` as referred to throughout is meant to point to your
Python 3 interpreter. Depending on your setup, the command might simply be
``python`` for you. (In any event, Linguistica 5 requires Python 3.4 or above.)


First steps
-----------

* Install the Linguistica 5 library **as a developer**.
  Run ``sudo python3 setup.py develop``. The ``develop`` argument means that
  you "install" the library by placing a symlink at your ``lxa5`` project
  directory so that your Python interpreter recognizes ``linguistica``
  at the current directory as a library and
  you can keep changing the code with immediate effects,
  without having to actually uninstall and reinstall all the time.

* Install the packages needed for testing. Run
  ``sudo python3 -m pip -r test_requirements.txt``.

* Use `PyCharm <https://www.jetbrains.com/pycharm/>`_ as your IDE.

General remarks
---------------

Notes in this section are to be better organized...

* Follow `PEP 8 <https://www.python.org/dev/peps/pep-0008/>`_ in coding.
  Use `PyCharm <https://www.jetbrains.com/pycharm/>`_ which nicely checks code,
  detects PEP 8 violations, and fixes everything.
  Do **NOT** use any generic text/code editors.

* Never ever make API changes!

* **Before and after each coding session**, run ``python3 nosetests_run.py``
  to make sure nothing breaks.

* Write brief and crisp code. For long routines/functions/methods, break them
  up into meaningful, smaller chunks.
  Doing this is desirable because it makes the code much more readable and
  essentially self-documenting. Also, writing shorter functions and methods
  apparently has great potential for performance gain because of fewer
  variables in a given namespace.

* If possible, the actual code is doing the job of documentation;
  this point is related to a previous one about writing shorter functions
  and methods.
  Minimize the use of comments in the code.
  Use ``vprint()`` defined in the ``util`` module for verbose print.

* **Sorting:** Avoid using the in-place method ``sort()``.
  Use the ``sorted()`` function that explicitly returns a new copy.
  This avoids accidentally sorting the source object.

* We do **NOT** use multiprocessing/threading.
  The library runs pretty fast anyway.
  The gain with parallelizing the processes (especially for running
  all modules for a given corpus), if any,
  isn't worth all the effort to struggle with potential issues for both
  the developers and users.

* All ``.py`` files must have ``# -*- encoding: utf8 -*-`` as the very first
  line. (Exception: the empty ``__init__.py`` files)
  It is true that Python 3 assumes UTF-8 for ``.py`` files by default,
  but let's be explicit rather than rely on the implicit.

* Python 2 is **NOT** supported. First, we need Python 3 only features
  (better unicode support etc). Second, it's not worth our effort to
  maintain a Python 2 version while Python 2 will be history soon-ish.

* **Version number:** We follow http://semver.org/ for the ``major.minor.patch``
  format.
  The current version is ``5.1.0``.
  The major version is ``5`` because there's John's Linguistica 3 & 4
  written in C++.
  The minor version is ``1`` rather than ``0`` because John has his in-house
  ``5.0`` written in Python 2 circa/before 2012.
  The version number is specified in ``linguistica/VERSION`` (and nowhere else).

* To minimize any inconsistency and confusion,
  follow the "don't repeat yourself" principle.
  This practice is to be applied fairly broadly.
  Examples include:

  * Specifying library dependencies at only one place, the ``requirements.txt``
    file (which ``setup.py`` reads).
  * Specifying version number at only one place,
    the ``linguistica/VERSION`` file
    (which both ``setup.py`` and the library read).
  * No code duplication, if possible. For generic/utility-type functions,
    define them in the ``util`` module.

* Never ever use ``import *``.

* **File I/O and encoding**:
  Apparently, the default file encoding for ``open()``
  is platform-dependent (?).
  To be absolutely sure about the encoding,
  whenever ``open()`` is used, always explicitly specify
  the ``encoding`` parameter.
  For this purpose,
  in ``linguistica/util.py``, the constant ``ENCODING`` (= ``'utf8'``)
  is defined. This constant is imported in other ``.py`` files throughout the
  library, and all ``open()`` calls are something like
  ``open(file_path, encoding=ENCODING)`` or equivalent.


.. _ci:

Continuous integration
----------------------

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

Commits and pushes
------------------

* Each commit is one single meaning and small chunk.

* Write meaningful commit messages
  (see `here <http://chris.beams.io/posts/git-commit/>`_, for instance).
  Each commit message consists of two components:
  (1) the subject line, and (2) the message body.
  The subject line is an imperative sentence (e.g. "Update readme"); note
  the first word is capitalized and there's no ending period. It contains
  no more than 50 characters. The message body explains what the commit
  is about. (If the commit is for something minor, e.g. "Tweak readme format",
  then the message body can be omitted.)

* No need to push code to GitHub for every single commit.
  This is because the repository is connected to :ref:`ci`, and therefore we
  don't need to waste web resources to trigger the tests etc all the time,
  especially for minor commits. Also, before and after every commit,
  we run tests locally (i.e., running ``python3 nosetests_run.py``) to ensure
  nothing breaks anyway. So the practice of **not** pushing code for every
  commit is fine.


Testing
-------

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


``setup.py``
------------

(notes)


``readme.rst``
--------------

rst rather than markdown is used
because this is to be read as the
long description in ``setup.py``,
and PyPI recognizes rst but not markdown
to render the text formatting.


``changelog.md``
----------------

(notes)


Documentation
-------------

Using Sphinx. More notes needed here.


Graphical user interface
------------------------

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

* The CLI code is in ``linguistica/cli.py``, all wrapped in
  ``linguistica.cli.main()`` called in ``linguistica/__main__.py``.

* We don't output ``words_to_contexts``
  and ``contexts_to_words``, because they are huge...
  Or we could just output those whose counts are higher than some threshold?


``linguistica/VERSION``
-----------------------

A plain text file that specifies the version number -- currently ``5.1.0-dev``.


Codebase
--------

See :ref:`codebase`.
