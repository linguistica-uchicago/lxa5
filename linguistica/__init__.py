# -*- encoding: utf8 -*-

"""
A Linguistica object is initialized with some data.
The way this can be done depends on the nature of your data source:

.. currentmodule:: linguistica

.. autosummary::

   read_corpus
   read_wordlist
   from_corpus
   from_wordlist

For instance, if the Brown corpus (Kučera and Francis 1967) is available on
your local drive:

.. code-block:: python

   >>> import linguistica as lxa
   >>> lxa_object = lxa.read_corpus('path/to/english.brown.txt')

Use ``read_wordlist()``
if you have a wordlist text file instead (where each line contains
one word type, optionally followed by whitespace plus frequency count for that
word).

Use ``from_corpus()`` or ``from_wordlist()``
if your data is an in-memory Python object (either a corpus text or a wordlist).

"""

import os

from linguistica.lexicon import Lexicon
from linguistica.util import (ENCODING, CONFIG_FILENAME)

# Version
version_filename = os.path.join(os.path.dirname(__file__), 'VERSION')
try:
    with open(version_filename) as f:
        __version__ = f.read().strip()
except FileNotFoundError:
    __version__ = 'unknown version; VERSION file not found'


def read_corpus(file_path, encoding=ENCODING,
                configfile=CONFIG_FILENAME, keep_case=False,
                **kwargs):
    """
    Create a Linguistica object with a corpus data file.

    :param file_path: path of input corpus file
    :param encoding: encoding of the file at *file_path*. Default: ``'utf8'``
    :param configfile: configuration filename. Default: ``config.json``
    :param keep_case: whether to keep case distinction (e.g., "the" vs "The").
        Default: ``False``
    :param kwargs: keyword arguments for configuration parameters.
    """
    return Lexicon(file_path=file_path, wordlist_file=False, encoding=encoding,
                   configfile=configfile, keep_case=keep_case, **kwargs)


def read_wordlist(file_path, encoding=ENCODING,
                  configfile=CONFIG_FILENAME, keep_case=False,
                  **kwargs):
    """
    Create a Linguistica object with a wordlist file.

    :param file_path: path of input wordlist file where each line contains
        one word type (and, optionally, a whitespace plus the token count
        for that word).
    :param encoding: encoding of the file at *file_path*. Default: ``'utf8'``
    :param configfile: configuration filename. Default: ``config.json``
    :param keep_case: whether to keep case distinction (e.g., "the" vs "The").
        Default: ``False``
    :param kwargs: keyword arguments for configuration parameters.
    """
    return Lexicon(file_path=file_path, wordlist_file=True, encoding=encoding,
                   configfile=configfile, keep_case=keep_case, **kwargs)


def from_corpus(corpus_object, configfile=CONFIG_FILENAME, keep_case=False,
                **kwargs):
    """
    Create a Linguistica object with a corpus object.

    :param corpus_object: a long string of text to which ``str()`` applies.
    :param configfile: configuration filename. Default: ``config.json``
    :param keep_case: whether to keep case distinction (e.g., "the" vs "The").
        Default: ``False``
    :param kwargs: keyword arguments for configuration parameters.
    """
    return Lexicon(corpus_object=corpus_object, wordlist_file=False,
                   configfile=configfile, keep_case=keep_case, **kwargs)


def from_wordlist(wordlist_object, configfile=CONFIG_FILENAME, keep_case=False,
                  **kwargs):
    """
    Create a Linguistica object with a wordlist object.

    :param wordlist_object: a sequence of unique word types as str
    :param configfile: configuration filename. Default: ``config.json``
    :param keep_case: whether to keep case distinction (e.g., "the" vs "The").
        Default: ``False``
    :param kwargs: keyword arguments for configuration parameters.
    """
    return Lexicon(wordlist_object=wordlist_object, wordlist_file=False,
                   configfile=configfile, keep_case=keep_case, **kwargs)
