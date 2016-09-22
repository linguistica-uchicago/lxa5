# -*- encoding: utf8 -*-

"""
To use Linguistica 5 as a Python library,
an essential step is to initialize a Linguistica object.
The way this can be done depends on the nature of your data source:

.. _source:

Data source
-----------

.. currentmodule:: linguistica

.. autosummary::

   read_corpus
   read_wordlist
   from_corpus
   from_wordlist

For instance, if the Brown corpus is available on
your local drive (see :ref:`rawtext`):

.. code-block:: python

   >>> import linguistica as lxa
   >>> lxa_object = lxa.read_corpus('path/to/english-brown.txt')

Use ``read_wordlist()``
if you have a wordlist text file instead
(see :ref:`wordlist`).

Use ``from_corpus()`` or ``from_wordlist()``
if your data is an in-memory Python object (either a corpus text or a wordlist).

.. _parameters:

Parameters
----------

The functions introduced in :ref:`source` all allow optional keyword
arguments which are parameters for the Linguistica object.
Different Linguistica modules make use of different parameters;
see :ref:`lexicon`.

For example, to deal with only the first 500,000 word tokens in the Brown
corpus:

.. code-block:: python

   >>> import linguistica as lxa
   >>> lxa_object = lxa.read_corpus('path/to/english-brown.txt', max_word_tokens=500000)

=====================  ====================================================  =========
Parameter              Meaning                                               Default
=====================  ====================================================  =========
``max_word_tokens``    maximum number of word tokens to be handled           0 (= all)
``max_word_types``     maximum number of word types to be handled            1000
``min_stem_length``    minimum stem length                                   4
``max_affix_length``   maximum affix length                                  4
``min_sig_count``      minimum number of stems for a valid signature         5
``min_context_count``  minimum number of occurrences for a valid context     3
``n_neighbors``        number of syntactic word neighbors                    9
``n_eigenvectors``     number of eigenvectors (in dimensionality reduction)  11
``suffixing``          whether the language is suffixing                     1 (= yes)
``keep_case``          whether case distinctions ("the" vs "The") are kept   0 (= no)
=====================  ====================================================  =========

The method ``parameters()`` returns the parameters and their values as a dict:

.. code-block:: python

   >>> from pprint import pprint
   >>> pprint(lxa_object.parameters())
   {'keep_case': 0,
    'max_affix_length': 4,
    'max_word_tokens': 0,
    'max_word_types': 1000,
    'min_context_count': 3,
    'min_sig_count': 5,
    'min_stem_length': 4,
    'n_eigenvectors': 11,
    'n_neighbors': 9,
    'suffixing': 1}

To change one or multiple parameters of a Linguistica object,
use ``change_parameters()`` with keyword arguments:

.. code-block:: python

   >>> lxa_object.parameters()['min_stem_length']  # before the change
   4
   >>> lxa_object.change_parameters(min_stem_length=3)
   >>> lxa_object.parameters()['min_stem_length']  # after the change
   3

To reset all parameters to their default values,
use ``use_default_parameters()``:

.. code-block:: python

   >>> lxa_object.parameters()['min_stem_length']  # non-default value
   3
   >>> lxa_object.use_default_parameters()
   >>> lxa_object.parameters()['min_stem_length']
   4

"""

from linguistica.release import __version__
from linguistica.util import ENCODING
from linguistica.lexicon import Lexicon


assert type(__version__) is str


def read_corpus(file_path, encoding=ENCODING, **kwargs):
    """
    Create a Linguistica object with a corpus data file.

    :param file_path: path of input corpus file
    :param encoding: encoding of the file at *file_path*. Default: ``'utf8'``
    :param kwargs: keyword arguments for parameters and their values.
    """
    return Lexicon(file_path=file_path, wordlist_file=False, encoding=encoding,
                   **kwargs)


def read_wordlist(file_path, encoding=ENCODING, **kwargs):
    """
    Create a Linguistica object with a wordlist file.

    :param file_path: path of input wordlist file where each line contains
        one word type (and, optionally, a whitespace plus the token count
        for that word).
    :param encoding: encoding of the file at *file_path*. Default: ``'utf8'``
    :param kwargs: keyword arguments for parameters and their values.
    """
    return Lexicon(file_path=file_path, wordlist_file=True, encoding=encoding,
                   **kwargs)


def from_corpus(corpus_object, **kwargs):
    """
    Create a Linguistica object with a corpus object.

    :param corpus_object: either a long string of text
        (with spaces separating word tokens) or a list of strings as word
        tokens
    :param kwargs: keyword arguments for parameters and their values.
    """
    return Lexicon(corpus_object=corpus_object, wordlist_file=False, **kwargs)


def from_wordlist(wordlist_object, **kwargs):
    """
    Create a Linguistica object with a wordlist object.

    :param wordlist_object: either a dict of word types (as strings) mapped to
        their token counts or an iterable of word types (as strings).
    :param kwargs: keyword arguments for parameters and their values.
    """
    return Lexicon(wordlist_object=wordlist_object, wordlist_file=False,
                   **kwargs)
