from __future__ import annotations

import os
from itertools import groupby
from time import strftime
from pprint import pformat
import platform
from typing import Any, Callable, Iterable

import scipy
import numpy
import networkx

import linguistica

# Type aliases for the nested shapes that recur throughout the library.
Signature = tuple[str, ...]  # e.g. ("NULL", "s", "ed", "ing")
Bigram = tuple[str, str]
Trigram = tuple[str, str, str]
SigTransform = tuple[Signature, str]
FilePath = str | os.PathLike[str]  # str or any pathlib.Path-like object

lxa_version = linguistica.__version__
scipy_version = scipy.__version__
numpy_version = numpy.__version__
networkx_version = networkx.__version__

ENCODING = "utf8"

SUFFIXING_LANGUAGES: set[str] = {
    "english",
    "french",
    "hungarian",
    "turkish",
    "russian",
    "german",
    "spanish",
    "test",
}

PREFIXING_LANGUAGES: set[str] = {"swahili"}

SEP_SIG = "/"  # separator between affixes in a sig (NULL/s/ed/ing)
SEP_SIGTRANSFORM = "."  # separator between sig and affix (NULL-s-ed-ing.ed)
SEP_NGRAM = "\t"  # separator between words in an ngram
# (e.g. 'the\tunited\tstates' means the 3-gram 'the united states')

NULL = "NULL"


def fix_punctuations(line: str) -> str:
    import re

    line = line.replace(".", " . ")
    line = line.replace(",", " , ")
    line = line.replace(";", " ; ")
    line = line.replace("!", " ! ")
    line = line.replace("?", " ? ")
    line = line.replace(":", " : ")
    line = line.replace(")", " ) ")
    line = line.replace("(", " ( ")
    return re.sub(r"\s", " ", line)


def double_sorted(
    input_object: Iterable[Any],
    key: Callable[[Any], Any] = lambda x: x,
    reverse: bool = False,
    subkey: Callable[[Any], Any] = lambda x: x,
    subreverse: bool = False,
) -> list[Any]:
    new_sorted_list: list[Any] = list()
    sorted_list = sorted(input_object, key=key, reverse=reverse)

    for _, group in groupby(sorted_list, key=key):  # groupby from itertools

        # must use "list(group)", cannot use just "group"!
        sublist = sorted(list(group), key=subkey, reverse=subreverse)
        # see python 3.4 documentation:
        # https://docs.python.org/3/library/itertools.html#itertools.groupby
        # "The returned group is itself an iterator that shares the underlying
        # iterable with groupby(). Because the source is shared, when the
        # groupby() object is advanced, the previous group is no longer
        # visible. So, if that data is needed later, it should be stored as a
        # list"

        new_sorted_list.extend(sublist)

    return new_sorted_list


def output_latex(
    iter_obj: Iterable[Any],
    file_path: str,
    title: str,
    headers: list[str],
    row_functions: list[Callable[[Any], Any]],
    column_widths: list[int],
    index: bool = True,
    lxa_parameters: dict[str, int] | None = None,
    test: bool = False,
    encoding: str = ENCODING,
    number_of_word_types: int = 0,
    number_of_word_tokens: int = 0,
    input_file_path: str | None = "",
) -> None:
    """Output LaTeX table code.

    :param iter_obj: an iterable object
    :param file_path: file path
    :param title: table title str
    :param headers: list of headers
    :param row_functions: list of row cell rendering functions.
        Each function takes only one argument and returns a str.
    :param column_widths: list of column widths.
    :param index: whether the table has an index column; defaults to True.
    :param lxa_parameters: the parameter dict
    :param test: whether nosetests are being run; defaults to False.
        If True, *file_path* is overridden by `os.devnull`` so that no
        text files are produced.
    """
    if not iter_obj:
        return

    if test:
        file_path = os.devnull

    file = open(file_path, "w", encoding=encoding)

    if not (len(headers) == len(row_functions) == len(column_widths)):
        raise ValueError(
            "headers, row_format, and column_widths " "not of the same size"
        )

    print("Time:", strftime("%Y-%m-%d %H:%M:%S"), file=file)
    print("Path of this file:", file_path, file=file)
    print(file=file)

    print("System info:\n" "=============================================", file=file)

    uname = platform.uname()
    print("System:", uname.system, file=file)
    print("Node:", uname.node, file=file)
    print("Release:", uname.release, file=file)
    print("Version:", uname.version, file=file)
    print("Machine:", uname.machine, file=file)
    print("Processor:", uname.processor, file=file)
    print("Python version:", platform.python_version(), file=file)
    print(file=file)

    print("Packages:\n" "=============================================", file=file)

    print("Linguistica", lxa_version, file=file)
    print("SciPy", scipy_version, file=file)
    print("NumPy", numpy_version, file=file)
    print("NetworkX", networkx_version, file=file)
    print(file=file)

    print(
        "Linguistica parameters:\n" "=============================================",
        file=file,
    )
    print(pformat(lxa_parameters), file=file)
    print(file=file)

    print(
        "Input file information:\n" "=============================================",
        file=file,
    )
    print("Path:", input_file_path, file=file)
    print("Number of word types:", number_of_word_types, file=file)
    print("Number of word tokens:", number_of_word_tokens, file=file)
    print(file=file)

    print("Results:\n=============================================", file=file)

    header_list: list[str] = list()

    index_str_length = 10
    if index:
        header_list = ["Index".ljust(index_str_length)]

    for header, col_width in zip(headers, column_widths):
        header_list.append(header.ljust(col_width))

    number_of_columns = len(header_list)

    print(title + "\n", file=file)
    print("\\begin{{tabular}}{{{}}}".format("l" * number_of_columns), file=file)
    print("\\toprule", file=file)

    print("{} \\\\".format(" & ".join(header_list)), file=file)
    print("\\midrule", file=file)

    for i, row_obj in enumerate(iter_obj, 1):
        if index:
            row_list = [str(i).ljust(index_str_length)]
        else:
            row_list = list()

        for row_func, col_width in zip(row_functions, column_widths):
            row_list.append(str(row_func(row_obj)).ljust(col_width))

            print("{} \\\\".format(" & ".join(row_list)), file=file)

    print("\\bottomrule", file=file)
    print("\\end{tabular}\n", file=file)

    file.close()


def vprint(verbose: bool = False, *objects: object, **kwargs: Any) -> None:
    """Verbose print; defaults to False."""
    if verbose:
        print(*objects, **kwargs)
    else:
        return
