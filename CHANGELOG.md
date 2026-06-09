Change log
==========

v5.3.0 (2026-06-09)
-------------------

This release is a top-to-bottom modernization of the codebase, which had been
untouched since 2018.

* **Python support.** Dropped Python 2 entirely (and Python 3.4–3.11); the
  package now targets **Python 3.12–3.14**. Removed all Python 2 compatibility
  baggage (`six`, `from __future__` imports, `io.open`/`FileNotFoundError`
  shims, encoding declarations, old-style `super()` calls).

* **Packaging.** Consolidated to a single PEP 621 **`pyproject.toml`**
  (setuptools backend), replacing `setup.py`/`setup.cfg`, the
  `requirements.txt`/`dev-requirements.txt` files, and the `VERSION`/`release.py`
  version plumbing. The version is now resolved at runtime via
  `importlib.metadata`. Tooling lives in `dev`, `docs`, and `gui` extras.

* **Project layout.** Moved to a `src/linguistica/` layout with a top-level
  `tests/` directory.

* **Formatting, linting & CI.** Adopted **black** and **flake8** (88-column,
  black-compatible). Replaced Travis with **GitHub Actions** (lint, test matrix
  across Python 3.12/3.13/3.14, headless GUI smoke test, and build).

* **Type annotations.** Added PEP 484 type annotations across the non-GUI
  library modules, shipped a `py.typed` marker, and added a **mypy** type-check
  gate to the CI `lint` job.

* **API.** `read_corpus`, `read_wordlist`, and the `Lexicon` constructor now
  accept any `os.PathLike` (e.g. a `pathlib.Path`) for the input file path, not
  just a `str`; `Lexicon.output_all_results` likewise accepts a `PathLike`
  output directory.

* **GUI.** The PyQt5 GUI now runs on Python 3.14 via wheels, with
  `PyQtWebEngine` for the manifold view and the SIP build hassle gone. Added
  menu options to load the shipped datasets directly, and a parameter dialog
  that can save-and-rerun or cancel.

* **Manifold visualization.** Upgraded the bundled d3 from v3.5.6 (2015) to
  **v7.9.0**, rewriting the force-directed graph against the modern
  `d3.forceSimulation`/`d3.zoom`/`d3.drag` APIs and fixing the zoom/drag
  conflicts and layout stutter.

* **Documentation.** Migrated to a standard Sphinx `Makefile` build (no more
  committing built HTML), with sources hosted on **Read the Docs**. Switched the
  README to Markdown and added a `CONTRIBUTING.md`.

* **Bug fixes.** Fixed a manifold determinism/stability issue (pinned ARPACK
  start vector and real-valued eigenvectors), an internal lexicon state bug, and
  a case where word n-grams and word manifolds were computed for wordlist (not
  corpus) input.

v5.2.1 (2018-10-12)
-------------------

* Relax dependency requirements by removing the upper version number bounds.

v5.2.0 (2017-04-09)
-------------------

* Cross compatibility for both Python 2 and 3.
  Linguistica 5 works on Python 2.7, 3.4, 3.5, and 3.6.
  (The GUI works on Python 3 only.)
  
* Travis CI was greatly simplified.

* Minor stylistic fixes.
  `flake8` checks for code quality (and is part of Travis CI).

v5.1.1 (2017-03-05)
-------------------

* Switch from the removed `QtWebKitWidgets` to `QtWebEngineWidgets` in the GUI
  code. (`QtWebKitWidgets` was deprecated in Qt 5.5 and removed in Qt 5.6.)
  
* `linguistica` is now a terminal command for launching the command line
  interface or the graphical user interface.

v5.1.0 (2016-12-16)
-------------------

* The major modules now available:
  - `lexicon`
  - `ngram`
  - `signature`
  - `manifold`
  - `trie`
  - `phon`

* Include graphical user interface (GUI) and command line interface (CLI)
