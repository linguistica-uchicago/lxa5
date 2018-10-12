Change log
==========

v5.2.1 (2018-10-12)
-------------------

* Relax dependency requirements by removing the upper version number bounds.
* 

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
