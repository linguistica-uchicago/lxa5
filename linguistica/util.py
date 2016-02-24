# -*- encoding: utf8 -*-

from itertools import groupby


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
              }

PARAMETERS_FILENAME = 'parameters.json'


def fix_punctuations(line):
    line = line.replace('.', ' . ')
    line = line.replace(',', ' , ')
    line = line.replace(';', ' ; ')
    line = line.replace('!', ' ! ')
    line = line.replace('?', ' ? ')
    line = line.replace(':', ' : ')
    line = line.replace(')', ' ) ')
    line = line.replace('(', ' ( ')
    return line


def double_sorted(input_object, key=lambda x: x, reverse=False,
                  subkey=lambda x: x, subreverse=False):
    if not input_object:
        print("Warning: object is empty. Sorting aborted.")
        return

    new_sorted_list = list()
    sorted_list = sorted(input_object, key=key, reverse=reverse)

    for k, group in groupby(sorted_list, key=key):  # groupby from itertools

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


def output_latex_table(iter_obj, file, title=None, headers=None,
                       row_functions=None, column_widths=None, index=True):
    """
    Output LaTeX table code for *iter_obj* to *file*.

    :param iter_obj: an iterable object
    :param file: a file object (e.g. open(...))
    :param title: table title str
    :param headers: list of headers
    :param row_functions: list of row cell rendering functions.
        Each function takes only one argument and returns a str.
    :param column_widths: list of column widths.
    :param index: whether the table has an index column; defaults to True.
    """
    if not title:
        title = file.name
    if not headers:
        headers = ['header']
    if not row_functions:
        row_functions = [lambda x: str(x)]
    if not column_widths:
        column_widths = [0]

    if not (len(headers) == len(row_functions) == len(column_widths)):
        raise ValueError('headers, row_format, and column_widths '
                         'not of the same size')

    header_list = list()

    index_str_length = 10
    if index:
        header_list = ['Index'.ljust(index_str_length)]

    for header, col_width in zip(headers, column_widths):
        header_list.append(header.ljust(col_width))

    number_of_columns = len(header_list)

    print(title + '\n', file=file)
    print('\\begin{{tabular}}{{{}}}'.format('l' * number_of_columns), file=file)
    print('\\toprule', file=file)

    print('{} \\\\'.format(' & '.join(header_list)), file=file)
    print('\\midrule', file=file)

    for i, row_obj in enumerate(iter_obj, 1):
        if index:
            row_list = [str(i).ljust(index_str_length)]
        else:
            row_list = list()

        for row_func, col_width in zip(row_functions, column_widths):
            row_list.append(str(row_func(row_obj)).ljust(col_width))

        print('{} \\\\'.format(' & '.join(row_list)), file=file)

    print('\\bottomrule', file=file)
    print('\\end{tabular}\n', file=file)


def vprint(*objects, verbose=False, sep='', end='\n', flush=True):
    """
    Verbose print; defaults to False.
    """
    if verbose:
        print(*objects, sep=sep, end=end, flush=flush)
    else:
        return
