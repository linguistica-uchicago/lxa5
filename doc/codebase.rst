.. _codebase:

Code base
=========

Notes on the code base


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
