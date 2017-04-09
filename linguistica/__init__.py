# -*- encoding: utf8 -*-

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
