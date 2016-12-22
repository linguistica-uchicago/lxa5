.. _dev:

For developers
==============

This page provides technical notes for the developers of the Linguistica 5
group. For introductory background about the Linguistica 5 codebase,
please consult :ref:`codebase`.


Setting up the development environment
--------------------------------------

To work on the Linguistica 5 code:

1. Set up a personal GitHub account

   Pick a username preferably with lowercase letters only, e.g. "joesmith".
   The Linguistica 5 codebase is hosted on GitHub.
   Your contributions will be added to it via the GitHub interface.


2. Download and install ``git``

   ``git`` is the version control system of the Linguistica 5 project.
   Your contributions will be managed and passed from your local drive to
   GitHub by ``git``.


3. Download and install Miniconda

   You may want to take advantage of Miniconda for having a dedicated
   environment with a specific Python version and other dependencies
   for the Linguistica 5 project.
   Having such a dedicated environment is desirable as you are likely working
   on multiple projects at any given time (Linguistica 5 being just one of them),
   and you don't want the environment for one project to contaminate that for
   another project.

   Install Miniconda for Python 3.5. (This installs a new Python distribution
   on your machine, but we are not going to use it directly.)

   After Miniconda is installed, by default you are at the root environment.
   If you fire up your Python interpreter from the command line,
   you should see you are on Python 3.5 whose distribution is by
   Continuum Analytics, Inc. (the company that maintains Miniconda).
   Exit the interpreter, and run the following command to create the new environment
   for Linguistica 5.

   .. code::

      $ conda create -n lxa5 python=3.5 numpy scipy networkx

   This command creates the new environment called ``lxa5`` with Python 3.5
   as well as the specified dependencies for Linguistica 5. After this command
   is done with all the installation work, run the following to activate the
   new environment:

   .. code::

      $ source activate lxa5

   Now you are in the ``lxa5`` environment (no longer in the root environment).
   As an indicator for this change, your command line prompt is now prefixed
   with ``(lxa5)``.

   To deactivate the environment (for going back to the root environment, or
   for preparing to switch to another environment), simply run this:

   .. code::

      $ source deactivate


Getting Linguistica 5
---------------------

Each person working on the code has to have their own fork under their GitHub account. Steps for each person:

1. Make a personal GitHub account (if not done already).
2. Log on to GitHub and go to https://github.com/linguistica-uchicago/lxa5
3. At the top right hand corner, click "Fork". (If prompted for "where should we fork this repository", choose your own personal GitHub name.)
4. Now under your personal GitHub, you see a new repository called "lxa5".
5. Clone this repository (i.e. <your-github-name>/lxa5, not linguistica-chicago/lxa5) onto your local disk using git, and also install the linguistica library:

$ git clone https://github.com/<your-github-name>/lxa5.git
$ cd lxa5
$ python setup.py develop

(If you're on linux, you will likely need "sudo" for the last command above).

6. Test if you have the library installed. Fire up your python interpreter:

>>> import linguistica  # there should be no ImportError

Workflow
--------

Now you have the python library "linguistica" installed in development mode (i.e. changes in source code are immediately effective -- no need to uninstall and reinstall to try out new code). And you're ready to do awesome work by changing the source code:

1. Never ever work from the "master" branch. (Run "git branch" to see what branches you have and which branch you're on.)
2. Instead, work on a different branch whose name indicates what you are doing, e.g. "fix-bug-in-stems-to-signatures", "update-docs". You can create a branch by "git checkout -b <branch-name>"
3. Now (and finally!) you can actually make changes to the source code. Make changes incrementally and commit them with git. Run this pair of commands for each commit:

$ git add <files-changed>
$ git commit -m "<commit-message>"

Write brief and meaningful commit messages.

4. Repeat step 3 above as many time as needed for making the new feature you're working on great. If possible, please limit the number of lines changes to below 300, so that it won't take forever to review your changes.

5. When you're ready to get comments on your changes, you will push your code to your fork on github and make a pull request.
6. To push your code to your fork:

$ git push origin <branch-name>

7. To make a pull request (i.e. you want linguistica-chicago/lxa5 to get the changes from <your-github-name>/lxa5, as it were), go to your GitHub page and then to the forked "lxa5" repository. Click "Pull request" (or something like "Make pull request" -- should be something fairly prominent visually). Now you'll wait for feedback.


(old intro)
-----------

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

A plain text file that specifies the version number -- currently ``5.1.0``.

