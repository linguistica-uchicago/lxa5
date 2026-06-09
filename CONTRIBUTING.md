# Contributing to Linguistica 5

This guide combines two things: a high-level tour of the Linguistica 5
**codebase** (how the project is organized and how the code works), and the
**developer workflow** notes for contributing changes via pull requests. The
first part orients you in the code; the second part walks through setting up
your environment and getting pull requests up.

---

# Codebase

This part gives a high-level overview of the Linguistica 5 codebase.

## Overview

How does the Linguistica 5 code work in general?
We get a good sense of it by understanding how the code gets us a dictionary of
signatures to stems:

```python
>>> import linguistica as lxa
>>> from linguistica.datasets import brown
>>> lxa_object = lxa.read_corpus(brown)
>>> sigs_to_stems = lxa_object.signatures_to_stems()
```

This overview walks through what happens under the hood
when this code snippet is run.

`brown` is a string which is the path pointing to the Brown corpus that comes
with the Linguistica 5 library on your local disk.

`lxa_object` (created by `lxa.read_corpus(brown)`) is an instance of the class
`Lexicon` defined in `src/linguistica/lexicon.py`.
`Lexicon` has many methods, one of which is `signatures_to_stems()`.

What is the magic behind `lxa_object.signatures_to_stems()`
which returns a dict of signatures to stems?
The answer lies in the design of the class `Lexicon`.
Given the definition of the class is fairly long, we will examine it step by step,
unfolding only the relevant bits as we move along:

```python
class Lexicon:

    def __init__(self, ...):

        self._initialize()

    def _initialize(self):

        # signature-related objects
        self._signatures_to_stems = None
```

When we create a Linguistica object by the line `lxa_object = lxa.read_corpus(brown)`,
an instance of the class `Lexicon` is created.
When this instance is created, `__init__()` is called.
`__init__()` initializes several attributes (those in the form of `self.X`)
and triggers the method `_initialize()`.

What does `_initialize()` do? It initializes all objects of interest.
Most of them are initialized as `None`, like `_signatures_to_stems`
as shown here. Very soon we will see why we need `_signatures_to_stems`
(named with a leading underscore so that it is a private attribute),
and why it is default to `None`.

Now that all initialization work is done and `lxa_object` is ready in the memory,
we examine what happens when the final line
`sigs_to_stems = lxa_object.signatures_to_stems()` in the code snippet is run.

When `lxa_object.signatures_to_stems()` is called, the method
`signatures_to_stems()` of the `Lexicon` class is called.
What does this method do? Let's check out the code:

```python
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
```

When `signatures_to_stems()` is called, an if statement is first executed.
The condition of this if statement, `self._signatures_to_stems is None`,
evaluates to `True`, because `self._signatures_to_stems` has just been
initialized to be `None`. Then `self._make_all_signature_objects()` is
executed (more on this below).
When it finishes, `self._signatures_to_stems` holds the expected
dict (no longer `None`) and is returned.
(If `signatures_to_stems()` is called again, `self._signatures_to_stems`
is not `None` anymore and the expensive computation at `self._make_all_signature_objects()`
is avoided. This explains why in general the Linguistica 5 code has the distinction
between the private attribute `self._x` and the public method `self.x()`
for most objects of interest).

So, what is the method `self._make_all_signature_objects()`? As its name suggests,
it makes all signature-related `self._x`. In the code shown above,
two of these `self._x` are shown, including `self._signatures_to_stems`.
The order by which these `self._x` is computed matters,
because there is dependency among them. For example, `self._signatures_to_stems`
depends on `self._stems_to_words` just computed in the same method.

We are potentially interested in many of the intermediate objects for
research purposes. In our example, `self._stems_to_words` is intermediate
for the computation of `self._signatures_to_stems`, but we expose it
(by making it `self._x` as well as allowing the `self.x()` API access)
because a mapping from stems to words is of interest.

To compute `self._x` in `_make_all_signature_objects()`, many function calls
in the form of `signature.make_x()` are made. Here, `signature` refers
to the imported module, and all the function calls `make_x()` are defined
in `src/linguistica/signature.py`.

So this is essentially how objects of interest are created via the `Lexicon`
class. They are initialized in some way and are *not* actually
computed until necessary. Once computed, they are available in memory for
immediate retrieval. All heavy lifting is only called but not done within
the class `Lexicon` -- the real work is done in the respective modules
such as `signature`, `manifold`, and so on.

Notes on the graphical user interface (GUI):

* The GUI requires `PyQt5` and `PyQtWebEngine` (the latter provides
  `QWebEngineView`, used to render the word-neighbor manifold; note that the
  modern `QtWebEngine` replaces the old `QtWebKit`).

* These are *optional* dependencies (the GUI is not an absolute must-have for
  Linguistica 5 to work), declared in the `gui` extra. Nowadays they install
  cleanly as binary wheels via `pip install "linguistica[gui]"` -- sip is
  bundled automatically as `PyQt5-sip`, with no separate SIP build step.

* The GUI code is in `src/linguistica/gui`. The GUI is launched by
  calling `linguistica.gui.main()` in `src/linguistica/__main__.py`.

* All GUI code is accessible through only `linguistica.gui.main()`
  defined in `src/linguistica/gui/__init__.py`.
  This is important, because PyQt5 may potentially be unavailable
  at the user's system. The `__init__.py` safeguards against import errors,
  but other `.py` files in `src/linguistica/gui` do not.
  Relatedly, when `linguistica.gui.main()` is to be called
  (as in `src/linguistica/__main__.py`), there is always code that checks
  whether PyQt5 is importable before `linguistica.gui.main()` can
  actually be called.

Notes on the command line interface (CLI):

* The CLI code is in `src/linguistica/cli.py`, all wrapped in
  `linguistica.cli.main()` which is called in `src/linguistica/__main__.py`.

* We don't output `words_to_contexts`
  and `contexts_to_words`, because they are huge...
  Or we could just output those whose counts are higher than some threshold?

## Dependencies

All packaging metadata and dependencies live in a single `pyproject.toml`
(PEP 621, with the setuptools build backend). The runtime dependencies --
`numpy`, `scipy`, and `networkx` -- are declared under
`[project.dependencies]` and are installed automatically with the library.

Tooling is grouped into optional-dependency *extras* under
`[project.optional-dependencies]`:

  * `dev` -- `black`, `flake8`, `pytest`, `pytest-cov`
    (running the tests and code-quality checks)
  * `docs` -- `Sphinx` and `sphinx_rtd_theme` (building this documentation)
  * `gui` -- `PyQt5` and `PyQtWebEngine` (the optional graphical interface)

Developers install the library in editable mode together with the `dev`
extra (see [For developers](#for-developers)):
`$ uv pip install -e ".[dev]"`.

## Tests

We use `pytest` as the testing framework. Developers and administrators
should install the `dev` extra, which pulls in the test dependencies:
`$ uv pip install -e ".[dev]"`.

Run tests as often as you can. In particular, they must be run before *and*
after each coding session:
`$ uv run pytest -vv --cov linguistica tests`.
`-vv` outputs a verbose test report. `--cov linguistica` means that we
check test coverage for `.py` files of the `linguistica` package
(so just the library code, under `src/linguistica`). Lastly, `tests` in the
command specifies the directory where pytest should look for
tests in `test_*.py`. `.coveragerc` configures the test coverage report.

The code is auto-formatted with `black` and linted with `flake8` for
maintaining high code quality. Essentially, no style violations are allowed --
not even trailing whitespace or extra empty lines. Run them with
`$ uv run black src tests` and `$ uv run flake8 src tests`. If you see no
terminal output from flake8, it means everything is compliant. Note that the
CI build tests also run black `--check` and flake8. Do not try to work
around the robots!

## Continuous integration

The Linguistica 5 repository is set up with [GitHub Actions](https://github.com/linguistica-uchicago/lxa5/actions)
for automatically
running build tests on every push and pull request. The configuration is in
`.github/workflows/python.yml`, which defines four jobs:

  * `lint` -- checks formatting with black `--check` and lints with flake8
  * `test` -- installs the library and runs the test suite across a matrix of
    supported Python versions
  * `gui` -- a headless smoke test of the PyQt5 graphical interface
  * `build` -- builds the sdist/wheel and validates them with `twine check`

Build tests are run for all supported Python versions (3.12, 3.13, and 3.14).

## `pyproject.toml`

`pyproject.toml` defines how the Linguistica 5 library is built and installed,
and specifies the metadata of the library (displayed on the PyPI site).
Developers and administrators install the library in editable mode for
development purposes with `$ uv pip install -e ".[dev]"`.

## Version

The version number is hard-coded in `pyproject.toml` (under
`[project] version`) and nowhere else. At runtime,
`linguistica.__version__` is resolved from the installed package metadata
via `importlib.metadata.version("linguistica")`, so it always reflects the
value in `pyproject.toml`.

We essentially follow http://semver.org/ for the `major.minor.patch`
format. The major version is `5` because there's John's Linguistica 3 & 4
written in C++. The minor version number increments when a new release comes
with new features. The patch number increments when a new release comes with
changes with no API ramifications such as bug fixes.

The first release of Linguistica 5 was 5.1.0 instead of 5.0.0, because 5.0.0
was John's in-house version written in Python 2.

## Documentation

We use Sphinx as the documentation framework, as it is the official tool for
Python projects (including the docs of the Python language itself).
The source files (in the reStructuredText mark-up language) are in `docs/`.
To build the documentation locally, install the `docs` extra and run
`make html` from the `docs/` directory:

```
$ uv pip install -e ".[docs]"
$ cd docs
$ make html
```

The generated HTML lands in `docs/_build/html/` (git-ignored, not committed).
The public documentation website is hosted on
[Read the Docs](https://linguistica.readthedocs.io/) and is rebuilt
automatically on every push; its build is configured by `.readthedocs.yaml`.
For reproducible builds, Read the Docs installs from the pinned lockfile
`docs/requirements.txt` (compiled from the `docs` extra). Regenerate it
whenever the documentation or runtime dependencies change:
`$ uv pip compile --extra docs -o docs/requirements.txt pyproject.toml`.

Changes (new features, bug fixes) together with new version releases
should be documented in `CHANGELOG.md`.

---

# For developers

This part provides technical notes for the developers of the Linguistica 5 project group.
For introductory background about the Linguistica 5 codebase,
please consult the [Codebase](#codebase) part above.

None of the development notes below are
new, as they all come from the collective wisdom of the open-source and
software development community -- notably, for what is known as "gitflow".
They should be taken as best practice recommendations, and nothing is set in stone.
While your general goal is to get pull requests up,
the way how you make pull requests is entirely up to you.
Naturally, you can deviate from any of the advice given here;
in that case, you are on your own and you know what you are doing.

## Important reminders

1. **Never commit changes to the main branch.**

      Not even at your own fork -- this ensures that the main branch
      is always clean and serves as a fall back.

2. **Create task-specific branches.**

      Never create a branch like "develop" and "research" and plan to vomit
      a huge amount of your great work into it before making any pull requests
      (this would make code review impossible). Think of a branch as something
      much more concrete like a mini project, with branch names like
      "add-feature-x" or "fix-function-x".

3. **Keep pull requests small.**

      A pull request has to be small (say, fewer than 300 lines of changes)
      so that the code review can be done efficiently and effectively with
      useful feedback.

4. **Follow PEP 8 in coding.**

      The [PEP 8](https://www.python.org/dev/peps/pep-0008/)
      coding conventions exist precisely because we would like to schedule
      exactly no time for discussing things like "how to name variables",
      "whether space is needed" and so on for coding.
      The code is auto-formatted with `black` and linted with `flake8`
      (both gated in CI), so most style questions are settled mechanically.
      There are also excellent IDEs such as [VS Code](https://code.visualstudio.com/)
      for maintaining Python
      projects at a high level of quality.

5. **Edit the documentation source.**

     To update the documentation, edit the source `.rst` files under
     `docs/`.
     To build it locally (so that you can verify changes locally), run `make html` (see [Documentation](#documentation)).
     The public documentation site is built automatically by
     [Read the Docs](https://linguistica.readthedocs.io/), upon either a push to the `main` branch or a GitHub release --
     there are no HTML files to commit.

## Setting up the development environment

1. You will need a [GitHub](https://github.com/) account. If you are creating a new one,
   pick a username preferably with lowercase letters only, e.g. "joesmith".
   The Linguistica 5 codebase is hosted on GitHub.
   Your contributions will be added to it via the GitHub interface.

2. You will need [Git](https://git-scm.com/) for version control.
   Your contributions will be managed and uploaded from your local drive to
   GitHub by Git.

3. Log on to your GitHub account and go to https://github.com/linguistica-uchicago/lxa5

4. At the top right hand corner, click "Fork".
   (If prompted for "where should we fork this repository", choose your own personal GitHub username.)

5. Now under your personal GitHub account, you see a new repository called "lxa5".

6. Clone this repository onto your local disk using Git,
   and install the Linguistica 5 Python library together with its
   development dependencies. We use [uv](https://docs.astral.sh/uv/) for all Python tooling:

   ```
   $ git clone https://github.com/<your-github-username>/lxa5.git
   $ cd lxa5
   $ uv venv
   $ uv pip install -e ".[dev]"
   ```

   The `-e` flag installs the `linguistica` package in *editable*
   (development) mode -- changes in the source code are immediately effective,
   with no need to uninstall and reinstall to try out new code.
   The `[dev]` extra additionally pulls in the tooling for running the tests
   and code-quality checks (`pytest`, `pytest-cov`, `black`, `flake8`).
   Run subsequent Python commands through `uv run` (e.g. `uv run pytest`)
   so they use this environment.

7. Add a link to the linguistica-uchicago/lxa5 repository:

   ```
   $ git remote add upstream https://github.com/linguistica-uchicago/lxa5.git
   ```

   This command adds a new link to the linguistica-uchicago/lxa5 repository
   (not your fork on GitHub) and names it as "upstream".
   From time to time, you will need to keep your local
   copy of the Linguistica 5 codebase up-to-date by pulling the latest code
   from the linguistica-uchicago/lxa5 repository. This added link (with the name
   "upstream") tells Git where to pull updates from.

   By default, after you have cloned and created a copy of Linguistica 5 on
   your local drive (in step 4 above), there is already a link called "origin"
   set up and linked to your fork on GitHub. Run the following to verify you
   have "origin" pointing to your fork and "upstream" pointing to
   linguistica-uchicago/lxa5:

   ```
   $ git remote -v
   ```

## Committing changes and making a pull request

After you have set up your system and downloaded Linguistica 5 as described above,
you are now (almost) ready to do awesome work!

1. **Verify that the main branch on your local drive is up-to-date in sync with
   the main on linguistica-uchicago/lxa5.**

      It is important to make sure you start working with the latest
      codebase:

      ```
      $ git checkout main  # go to main branch
      $ git pull upstream main  # pull latest from main branch of upstream
      ```

      Recall that "upstream" means the linguistica-uchicago/lxa5 repository.

2. **Create a new branch for your great work.**

      Never work from the main branch.
      (Run "git branch" anytime to see what branches you have and which branch you're on.)

      Instead, work on a different branch whose name indicates what you are doing,
      e.g. "revamp-stems-to-signatures", "update-docs", "fix-bug-in-function-x":

      ```
      $ git checkout -b <branch-name>
      ```

      After this command is run, the new branch is created *and* you are on
      that branch as well (no longer on main branch).

3. **Start committing changes to source code.**

      Now (and finally!) you can actually make changes to the source code.
      Make changes incrementally and commit them with Git.
      Run this pair of commands for each commit:

      ```
      $ git add <files-changed>
      $ git commit -m "<commit-message>"
      ```

      `<files-changed>` can be a single file (e.g. `foo.py`) or multiple ones
      separated by spaces (e.g. `foo.py bar.py`).

      Write brief and meaningful commit messages,
      e.g. "Fix bug in stems_to_signatures".
      Aim at making each commit a logical and meaningful chunk of changes.

4. **Repeat step 3 above as needed.**

      Repeat step 3 for making more commits on your way to what the branch
      is for. Limit the number of line changes to below 300 to make
      efficient and effective code review possible.

5. **Run tests to make sure nothing breaks.**

      Run the tests (and get a detailed report if anything breaks):

      ```
      $ uv run pytest -vv --cov linguistica tests
      ```

      Make sure the code is formatted and PEP8 compliant:

      ```
      $ uv run black src tests
      $ uv run flake8 src tests
      ```

6. **Push your changes to your fork on GitHub.**

      To make your changes available for review and for merging,
      you will first have to push your changes to your fork on GitHub:

      ```
      $ git push origin <branch-name>
      ```

      Recall that "origin" is the (default) name point to your fork <your-github-username>/lxa5 on GitHub.

7. **Make a pull request.**

      Log on to your GitHub and go to your fork <your-github-username>/lxa5.
      Now you are ready to make a pull request
      (i.e. you want linguistica-chicago/lxa5 to get the changes
      from your <branch-name> of <your-github-name>/lxa5, as it were).
      Click "Pull request"
      (or something like "Make pull request" -- it should be something fairly prominent visually).
      Create the pull request by giving your pull request a title
      (most probably something very similar to the branch name) and
      providing brief notes on what the new changes are in the "comments" section.
      Now you'll wait for feedback.

8. **Start a new branch for a new mini project.**

      After all your hard work in the pull request has been accepted (= merged
      into linguistica-uchicago/lxa5), you can go back to step 1
      to update your main branch for the latest code and prepare
      for a new branch and an upcoming pull request!
