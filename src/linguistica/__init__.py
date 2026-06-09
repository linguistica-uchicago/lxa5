from __future__ import annotations

from importlib.metadata import version
from typing import Iterable, Unpack

__version__: str = version("linguistica")

from linguistica.util import ENCODING, FilePath  # noqa: E402
from linguistica.parameters import ParametersKwargs  # noqa: E402
from linguistica.lexicon import Lexicon  # noqa: E402

assert type(__version__) is str


def read_corpus(
    file_path: FilePath, encoding: str = ENCODING, **kwargs: Unpack[ParametersKwargs]
) -> Lexicon:
    """Create a Linguistica object with a corpus data file.

    :param file_path: path of input corpus file
    :param encoding: encoding of the file at *file_path*. Default: ``'utf8'``
    :param kwargs: keyword arguments for parameters and their values.
    """
    return Lexicon(
        file_path=file_path,
        wordlist_file=False,
        corpus_object=None,
        wordlist_object=None,
        encoding=encoding,
        **kwargs,
    )


def read_wordlist(
    file_path: FilePath, encoding: str = ENCODING, **kwargs: Unpack[ParametersKwargs]
) -> Lexicon:
    """Create a Linguistica object with a wordlist file.

    :param file_path: path of input wordlist file where each line contains
        one word type (and, optionally, a whitespace plus the token count
        for that word).
    :param encoding: encoding of the file at *file_path*. Default: ``'utf8'``
    :param kwargs: keyword arguments for parameters and their values.
    """
    return Lexicon(
        file_path=file_path,
        wordlist_file=True,
        corpus_object=None,
        wordlist_object=None,
        encoding=encoding,
        **kwargs,
    )


def from_corpus(
    corpus_object: str | list[str], **kwargs: Unpack[ParametersKwargs]
) -> Lexicon:
    """Create a Linguistica object with a corpus object.

    :param corpus_object: either a long string of text
        (with spaces separating word tokens) or a list of strings as word
        tokens
    :param kwargs: keyword arguments for parameters and their values.
    """
    return Lexicon(
        file_path=None,
        wordlist_file=False,
        corpus_object=corpus_object,
        wordlist_object=None,
        encoding=ENCODING,
        **kwargs,
    )


def from_wordlist(
    wordlist_object: dict[str, int] | Iterable[str],
    **kwargs: Unpack[ParametersKwargs],
) -> Lexicon:
    """Create a Linguistica object with a wordlist object.

    :param wordlist_object: either a dict of word types (as strings) mapped to
        their token counts or an iterable of word types (as strings).
    :param kwargs: keyword arguments for parameters and their values.
    """
    return Lexicon(
        file_path=None,
        wordlist_file=False,
        corpus_object=None,
        wordlist_object=wordlist_object,
        encoding=ENCODING,
        **kwargs,
    )
