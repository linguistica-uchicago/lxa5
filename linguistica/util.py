# -*- encoding: utf8 -*-

from __future__ import print_function, unicode_literals

import os
from itertools import groupby
from time import strftime
from pprint import pformat
import platform
from io import open  # not using built-in open(), for py2+3 cross compatibility

import six
import scipy
import numpy
import networkx

import linguistica


lxa_version = linguistica.__version__
scipy_version = scipy.__version__
numpy_version = numpy.__version__
networkx_version = networkx.__version__

REQUIRED_PY_VERSION = (3, 4)

ENCODING = 'utf8'

SUFFIXING_LANGUAGES = {'english', 'french', 'hungarian', 'turkish', 'russian',
                       'german', 'spanish', 'test'}

PREFIXING_LANGUAGES = {'swahili'}

SEP_SIG = '/'           # separator between affixes in a sig (NULL/s/ed/ing)
SEP_SIGTRANSFORM = '.'  # separator between sig and affix (NULL-s-ed-ing.ed)
SEP_NGRAM = '\t'        # separator between words in an ngram
# (e.g. 'the\tunited\tstates' means the 3-gram 'the united states')

NULL = 'NULL'

# ------------------------------------------------------------------------------
# parameters, with the "factory settings"

# What programs use what parameters:
#
# ngram:     max_word_tokens
# signature: min_stem_length, max_affix_length, min_sig_count
# phon:      (no parameters so far)
# trie:      min_stem_length, min_affix_length, min_sf_pf_count
# manifold:  max_word_types, n_neighbors, n_eigenvectors, min_context_count
# (See the individual programs for what these parameters mean.)

PARAMETERS = {'max_word_tokens': 0,  # zero means all word tokens
              'min_stem_length': 4,
              'max_affix_length': 4,
              'min_sig_count': 5,
              # 'min_affix_length': 1,
              # 'min_sf_pf_count': 3,
              'n_neighbors': 9,
              'n_eigenvectors': 11,
              'min_context_count': 3,
              'max_word_types': 1000,
              'suffixing': 1,  # 1 means yes, 0 means no
              'keep_case': 0,  # 1 means yes, 0 means no
              }

PARAMETERS_RANGES = {'max_word_tokens': (0, 1000000000),
                     'min_stem_length': (1, 10),
                     'max_affix_length': (1, 10),
                     'min_sig_count': (5, 50),
                     'n_neighbors': (5, 20),
                     'n_eigenvectors': (5, 20),
                     'min_context_count': (1, 10),
                     'max_word_types': (0, 1000000000),
                     'suffixing': (0, 1),  # 1 means yes, 0 means no
                     'keep_case': (0, 1),  # 1 means yes, 0 means no
                     }

PARAMETERS_HINTS = {'max_word_tokens': '0 = all word tokens',
                    'min_stem_length': '',
                    'max_affix_length': '',
                    'min_sig_count': '',
                    'n_neighbors': '',
                    'n_eigenvectors': '',
                    'min_context_count': '',
                    'max_word_types': '',
                    'suffixing': '1 = yes; 0 = no',
                    'keep_case': '1 = yes; 0 = no',
                    }


def fix_punctuations(line):
    import re
    line = line.replace('.', ' . ')
    line = line.replace(',', ' , ')
    line = line.replace(';', ' ; ')
    line = line.replace('!', ' ! ')
    line = line.replace('?', ' ? ')
    line = line.replace(':', ' : ')
    line = line.replace(')', ' ) ')
    line = line.replace('(', ' ( ')
    return re.sub('\s', ' ', line)


def double_sorted(input_object, key=lambda x: x, reverse=False,
                  subkey=lambda x: x, subreverse=False):
    new_sorted_list = list()
    sorted_list = sorted(input_object, key=key, reverse=reverse)

    for _, group in groupby(sorted_list, key=key):  # groupby from itertools

        # must use "list(group)", cannot use just "group"!
        sublist = sorted(list(group), key=subkey, reverse=subreverse)
        # see python 3.4 documentation:
        # https://docs.python.org/3/library/itertools.html#itertools.groupby
        # "The returned group is itself an iterator that shares the underlying
        # iterable with groupby(). Because the source is shared, when the 
        # groupby() object is advanced, the previous group is no longer visible.
        # So, if that data is needed later, it should be stored as a list"

        new_sorted_list.extend(sublist)

    return new_sorted_list


def output_latex(iter_obj, file_path, title, headers,
                 row_functions, column_widths, index=True,
                 lxa_parameters=None, test=False, encoding=ENCODING,
                 number_of_word_types=0, number_of_word_tokens=0,
                 input_file_path=''):
    """
    Output LaTeX table code for *iter_obj* to *file*.

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

    file = open(file_path, 'w', encoding=encoding)

    if not (len(headers) == len(row_functions) == len(column_widths)):
        raise ValueError('headers, row_format, and column_widths '
                         'not of the same size')

    uprint('Time:', strftime('%Y-%m-%d %H:%M:%S'), file=file)
    uprint('Path of this file:', file_path, file=file)
    uprint(file=file)

    uprint('System info:\n'
           '=============================================', file=file)

    uname = platform.uname()
    uprint('System:', uname.system, file=file)
    uprint('Node:', uname.node, file=file)
    uprint('Release:', uname.release, file=file)
    uprint('Version:', uname.version, file=file)
    uprint('Machine:', uname.machine, file=file)
    uprint('Processor:', uname.processor, file=file)
    uprint('Python version:', platform.python_version(), file=file)
    uprint(file=file)

    uprint('Packages:\n'
           '=============================================', file=file)

    uprint('Linguistica', lxa_version, file=file)
    uprint('SciPy', scipy_version, file=file)
    uprint('NumPy', numpy_version, file=file)
    uprint('NetworkX', networkx_version, file=file)
    uprint(file=file)

    uprint('Linguistica parameters:\n'
          '=============================================', file=file)
    uprint(pformat(lxa_parameters), file=file)
    uprint(file=file)

    uprint('Input file information:\n'
           '=============================================', file=file)
    uprint('Path:', input_file_path, file=file)
    uprint('Number of word types:', number_of_word_types, file=file)
    uprint('Number of word tokens:', number_of_word_tokens, file=file)
    uprint(file=file)

    uprint('Results:\n=============================================', file=file)

    header_list = list()

    index_str_length = 10
    if index:
        header_list = ['Index'.ljust(index_str_length)]

    for header, col_width in zip(headers, column_widths):
        header_list.append(header.ljust(col_width))

    number_of_columns = len(header_list)

    uprint(title + '\n', file=file)
    uprint('\\begin{{tabular}}{{{}}}'.format('l' * number_of_columns),
           file=file)
    uprint('\\toprule', file=file)

    uprint('{} \\\\'.format(' & '.join(header_list)), file=file)
    uprint('\\midrule', file=file)

    for i, row_obj in enumerate(iter_obj, 1):
        if index:
            row_list = [str(i).ljust(index_str_length)]
        else:
            row_list = list()

        for row_func, col_width in zip(row_functions, column_widths):
            row_list.append(str(row_func(row_obj)).ljust(col_width))

            uprint('{} \\\\'.format(' & '.join(row_list)), file=file)

    uprint('\\bottomrule', file=file)
    uprint('\\end{tabular}\n', file=file)

    file.close()


def vprint(verbose=False, *objects, **kwargs):
    """
    Verbose print; defaults to False.
    """
    if verbose:
        print(*objects, **kwargs)
    else:
        return


def uprint(*args, **kwargs):
    """
    Same as ``print(*args, **kwargs)``, but all ``args`` are first passed
    through ``six.u`` to ensure unicode. This function is used specifically
    for printing to a file.

    :param args: objects to print
    :param kwargs: kwargs for ``print``
    """
    # args = [six.u(x) for x in args]
    # for x in args:
    #     print(x, type(x))
    print(*args, **kwargs)
