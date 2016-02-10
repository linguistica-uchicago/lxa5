# -*- encoding: utf-8 -*-

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
    Create the Linguistica lexicon object with a corpus data file.

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
    Create the Linguistica lexicon object with a wordlist file.

    :param file_path: path of input wordlist file where each line contains
        one word type at the beginning of the line.
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
    Create the Linguistica lexicon object with a corpus object.

    :param corpus_object: a corpus object (e.g., a long string of text) to
        which ``str()`` applies.
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
    Create the Linguistica lexicon object with a wordlist object.

    :param wordlist_object: a wordlist object which is a sequence of word types
        as str.
    :param configfile: configuration filename. Default: ``config.json``
    :param keep_case: whether to keep case distinction (e.g., "the" vs "The").
        Default: ``False``
    :param kwargs: keyword arguments for configuration parameters.
    """
    return Lexicon(wordlist_object=wordlist_object, wordlist_file=False,
                   configfile=configfile, keep_case=keep_case, **kwargs)
