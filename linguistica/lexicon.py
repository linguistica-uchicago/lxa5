# -*- encoding: utf8 -*-

"""
Once a Linguistica object (such as ``lxa_object`` below with the Brown corpus)
is initialized, various methods and attributes are available for automatic
linguistic analysis:

.. code-block:: python

   >>> import linguistica as lxa
   >>> lxa_object = lxa.read_corpus('path/to/english-brown.txt')
   >>> words = lxa_object.wordlist()  # using wordlist()

Basic information
-----------------

.. currentmodule:: linguistica.lexicon.Lexicon

.. autosummary::

   number_of_word_tokens
   number_of_word_types

Word ngrams
-----------

Parameter: ``max_word_tokens``

.. currentmodule:: linguistica.lexicon.Lexicon

.. autosummary::

   wordlist
   word_unigram_counter
   word_bigram_counter
   word_trigram_counter

Morphological signatures
------------------------

Parameters: ``min_stem_length``, ``max_affix_length``, ``min_sig_count``, ``suffixing``

.. currentmodule:: linguistica.lexicon.Lexicon

.. autosummary::

   signatures
   stems
   affixes

   signatures_to_stems
   signatures_to_words
   affixes_to_signatures
   stems_to_signatures
   stems_to_words
   words_in_signatures
   words_to_signatures
   words_to_sigtransforms

Word manifolds and syntactic word neighborhood
----------------------------------------------

Parameters: ``max_word_types``, ``min_context_count``, ``n_neighbors``, ``n_eigenvectors``

.. currentmodule:: linguistica.lexicon.Lexicon

.. autosummary::

   words_to_neighbors
   neighbor_graph
   words_to_contexts
   contexts_to_words

Phonology
---------

.. currentmodule:: linguistica.lexicon.Lexicon

.. autosummary::

   phone_unigram_counter
   phone_bigram_counter
   phone_trigram_counter

Tries
-----

Parameter: ``min_stem_length``

.. currentmodule:: linguistica.lexicon.Lexicon

.. autosummary::

   broken_words_left_to_right
   broken_words_right_to_left
   successors
   predecessors

Other methods and attributes
----------------------------

.. currentmodule:: linguistica.lexicon.Lexicon

.. autosummary::

   parameters
   change_parameters
   use_default_parameters
   reset

"""

import sys
import os
from io import StringIO

from linguistica import (ngram, signature, manifold, phon, trie)
from linguistica.util import (ENCODING, PARAMETERS, SEP_SIG, SEP_SIGTRANSFORM,
                              double_sorted, fix_punctuations,
                              output_latex, vprint)


class Lexicon:
    """
    A class for a Linguistica object. It is called "Lexicon" for the historical
    reason that the same element in the C++ version of Linguistica 4 is also
    called as such.
    """

    def __init__(self, file_path=None, wordlist_file=False, corpus_object=None,
                 wordlist_object=None, encoding=ENCODING, **kwargs):
        self.file_abspath = self._check_file_path(file_path)

        if self.file_abspath is None:
            self.directory = None
        else:
            self.directory = os.path.dirname(self.file_abspath)

        self.file_is_wordlist = wordlist_file
        self.encoding = encoding
        self.corpus_object = corpus_object
        self.wordlist_object = wordlist_object
        self.parameters_ = self._determine_parameters(**kwargs)

        self._initialize()

    @staticmethod
    def _check_file_path(file_path):
        """
        Return the absolute path of *file_path*.
        """
        if file_path is None:
            return None

        if type(file_path) != str:
            raise TypeError('file path must be a str -- ' + file_path)

        if sys.platform.startswith('win'):
            file_path = file_path.replace('/', os.sep)
        else:
            file_path = file_path.replace('\\', os.sep)

        file_abspath = os.path.abspath(file_path)
        if not os.path.isfile(file_abspath):
            raise FileNotFoundError(file_path)
        else:
            return file_abspath

    @staticmethod
    def _determine_parameters(**kwargs):
        """
        Determine the parameter dict.
        """
        temp_parameters = dict(PARAMETERS)

        for parameter in kwargs.keys():
            if parameter not in PARAMETERS:
                raise KeyError('unknown parameter -- ' + parameter)
            else:
                temp_parameters[parameter] = kwargs[parameter]

        return temp_parameters

    def parameters(self):
        """
        Return the parameter dict.

        :rtype: dict(str: int)
        """
        return self.parameters_

    def change_parameters(self, **kwargs):
        """
        Change parameters specified by *kwargs*.

        :param kwargs: keyword arguments for parameters and their new values
        """
        for parameter, new_value in kwargs.items():
            if parameter not in self.parameters_:
                raise KeyError('unknown parameter -- ' + parameter)

            self.parameters_[parameter] = new_value

    def use_default_parameters(self):
        """
        Reset parameters to their default values.
        """
        self.parameters_ = dict(PARAMETERS)

    def _initialize(self):
        # number of word types and tokens
        self._number_of_word_types = None
        self._number_of_word_tokens = None

        # word ngrams
        self._word_unigram_counter = None
        self._word_bigram_counter = None
        self._word_trigram_counter = None

        # wordlist
        self._wordlist = None
        if self.wordlist_object is not None:
            # self.wordlist_object is
            # either an iterable or a dict of word-count pairs
            if type(self.wordlist_object) is dict:
                word_count_dict = dict()
                if self.parameters_['keep_case']:
                    word_count_dict = self.wordlist_object
                else:
                    for word, count in self.wordlist_object:
                        word = word.lower()
                        if word not in word_count_dict:
                            word_count_dict[word] = 0
                        word_count_dict[word] += count

                self._wordlist = [word for word, _ in
                                  double_sorted(word_count_dict.items(),
                                                key=lambda x: x[1],
                                                reverse=True)]
                self._word_unigram_counter = word_count_dict

            elif hasattr(self.wordlist_object, '__iter__'):
                if self.parameters_['keep_case']:
                    self._wordlist = sorted(set(self.wordlist_object))
                else:
                    self._wordlist = sorted(
                        set(w.lower() for w in self.wordlist_object))
                self._word_unigram_counter = {w: 1 for w in self._wordlist}

            else:
                raise TypeError('wordlist object must be a dict of word-count'
                                'pairs or an iterable of words')

        # signature-related objects
        self._stems_to_words = None
        self._signatures_to_stems = None
        self._stems_to_signatures = None
        self._words_to_signatures = None
        self._signatures_to_words = None
        self._words_to_sigtransforms = None

        self._signatures = None
        self._affixes_to_signatures = None
        self._words_in_signatures = None
        self._affixes = None
        self._stems = None

        # corpus file object
        if self.corpus_object is not None:
            # self.corpus_object is either a list of strings or a long str
            if type(self.corpus_object) is list:
                corpus_str = fix_punctuations(' '.join(self.corpus_object))
            elif type(self.corpus_object) is str:
                corpus_str = fix_punctuations(self.corpus_object)
            else:
                raise TypeError('corpus object must be either a str or a list')
            self.corpus_file_object = StringIO(corpus_str)
        elif self.file_abspath and not self.file_is_wordlist:
            self.corpus_file_object = open(self.file_abspath,
                                           encoding=self.encoding)
        else:
            self.corpus_file_object = None

        # wordlist file object
        if self.file_is_wordlist:
            self.wordlist_file_object = open(self.file_abspath,
                                             encoding=self.encoding)
        else:
            self.wordlist_file_object = StringIO()

        # manifold-related objects
        self._words_to_neighbors = None
        self._words_to_contexts = None
        self._contexts_to_words = None
        self._neighbor_graph = None

        # phon objects
        self._phone_unigram_counter = None
        self._phone_bigram_counter = None
        self._phone_trigram_counter = None

        self._phone_dict = None
        self._biphone_dict = None
        self._word_dict = None
        self._words_to_phones = None

        # trie objects
        self._broken_words_left_to_right = None
        self._broken_words_right_to_left = None
        self._successors = None
        self._predecessors = None

    def reset(self):
        """
        Reset the Linguistica object. While the file path information is
        retained, all computed objects (ngrams, signatures, word neighbors, etc)
        are reset to ``NULL``; if they are called again, they are re-computed.
        """
        self._initialize()

    def run_all_modules(self, verbose=False):
        """
        Run all modules.
        """
        self.run_ngram_module(verbose=verbose)
        self.run_phon_module(verbose=verbose)
        self.run_signature_module(verbose=verbose)
        self.run_trie_module(verbose=verbose)

        if self.corpus_file_object:
            self.run_manifold_module(verbose=verbose)

    def output_all_results(self, directory=None, verbose=False, test=False):
        """
        Output all Linguistica results to *directory*.

        :param directory: output directory. If not specified, it defaults to
            the current directory given by ``os.getcwd()``.
        """
        if not directory:
            output_dir = os.getcwd()
        else:
            output_dir = os.path.abspath(directory)

        # ----------------------------------------------------------------------
        if self.corpus_file_object:
            vprint('ngram objects', verbose=verbose)

            fname = 'word_bigrams.txt'
            obj = double_sorted(self.word_bigram_counter().items(),
                                key=lambda x: x[1], reverse=True)
            f_path = os.path.join(output_dir, fname)
            output_latex(obj, f_path,
                         title='Word bigrams',
                         headers=['Word bigram', 'Count'],
                         row_functions=[lambda x: ' '.join(x[0]),
                                        lambda x: x[1]],
                         column_widths=[50, 10],
                         lxa_parameters=self.parameters(),
                         test=test, encoding=self.encoding,
                         number_of_word_types=self.number_of_word_types(),
                         number_of_word_tokens=self.number_of_word_tokens(),
                         input_file_path=self.file_abspath)
            vprint('\t' + fname, verbose=verbose)

            fname = 'word_trigrams.txt'
            obj = double_sorted(self.word_trigram_counter().items(),
                                key=lambda x: x[1], reverse=True)
            f_path = os.path.join(output_dir, fname)
            output_latex(obj, f_path,
                         title='Word trigrams',
                         headers=['Word trigram', 'Count'],
                         row_functions=[lambda x: ' '.join(x[0]),
                                        lambda x: x[1]],
                         column_widths=[75, 10],
                         lxa_parameters=self.parameters(),
                         test=test, encoding=self.encoding,
                         number_of_word_types=self.number_of_word_types(),
                         number_of_word_tokens=self.number_of_word_tokens(),
                         input_file_path=self.file_abspath)
            vprint('\t' + fname, verbose=verbose)

        # ----------------------------------------------------------------------
        vprint('morphological signature objects', verbose=verbose)

        fname = 'stems_to_words.txt'
        obj = double_sorted(self.stems_to_words().items(),
                            key=lambda x: len(x[1]), reverse=True)
        f_path = os.path.join(output_dir, fname)
        output_latex(obj, f_path,
                     title='Stems to words '
                           '(descending order of word count)',
                     headers=['Stem', 'Word count', 'Words'],
                     row_functions=[lambda x: x[0],
                                    lambda x: len(x[1]),
                                    lambda x: ', '.join(sorted(x[1]))],
                     column_widths=[15, 15, 0],
                     lxa_parameters=self.parameters(),
                     test=test, encoding=self.encoding,
                     number_of_word_types=self.number_of_word_types(),
                     number_of_word_tokens=self.number_of_word_tokens(),
                     input_file_path=self.file_abspath)
        vprint('\t' + fname, verbose=verbose)

        fname = 'stems_to_words.txt'
        obj = double_sorted(self.stems_to_words().items(),
                            key=lambda x: x[0], reverse=False)
        f_path = os.path.join(output_dir, fname)
        output_latex(obj, f_path,
                     title='Stems to words '
                           '(alphabetical order of stems)',
                     headers=['Stem', 'Word count', '1st 10 words'],
                     row_functions=[lambda x: x[0],
                                    lambda x: len(x[1]),
                                    lambda x: ', '.join(sorted(x[1]))],
                     column_widths=[15, 15, 0],
                     lxa_parameters=self.parameters(),
                     test=test, encoding=self.encoding,
                     number_of_word_types=self.number_of_word_types(),
                     number_of_word_tokens=self.number_of_word_tokens(),
                     input_file_path=self.file_abspath)
        vprint('\t' + fname, verbose=verbose)

        fname = 'signatures_to_stems.txt'
        obj = double_sorted(self.signatures_to_stems().items(),
                            key=lambda x: len(x[1]), reverse=True)
        f_path = os.path.join(output_dir, fname)
        output_latex(obj, f_path,
                     title='Signatures to stems',
                     headers=['Signature', 'Stem count', 'Stems'],
                     row_functions=[lambda x: SEP_SIG.join(x[0]),
                                    lambda x: len(x[1]),
                                    lambda x: ', '.join(sorted(x[1]))],
                     column_widths=[30, 15, 0],
                     lxa_parameters=self.parameters(),
                     test=test, encoding=self.encoding,
                     number_of_word_types=self.number_of_word_types(),
                     number_of_word_tokens=self.number_of_word_tokens(),
                     input_file_path=self.file_abspath)
        vprint('\t' + fname, verbose=verbose)

        fname = 'signatures_to_stems_truncated.txt'
        obj = double_sorted(self.signatures_to_stems().items(),
                            key=lambda x: len(x[1]), reverse=True)
        f_path = os.path.join(output_dir, fname)
        output_latex(obj, f_path,
                     title='Signatures to stems '
                           '(first 10 stems for each sig)',
                     headers=['Signature', 'Stem count', '1st 10 stems'],
                     row_functions=[lambda x: SEP_SIG.join(x[0]),
                                    lambda x: len(x[1]),
                                    lambda x:
                                    ' '.join(sorted(x[1])[:10])],
                     column_widths=[30, 15, 0],
                     lxa_parameters=self.parameters(),
                     test=test, encoding=self.encoding,
                     number_of_word_types=self.number_of_word_types(),
                     number_of_word_tokens=self.number_of_word_tokens(),
                     input_file_path=self.file_abspath)
        vprint('\t' + fname, verbose=verbose)

        fname = 'stems_to_signatures.txt'
        obj = double_sorted(self.stems_to_signatures().items(),
                            key=lambda x: len(x[1]), reverse=True)
        f_path = os.path.join(output_dir, fname)
        output_latex(obj, f_path,
                     title='Stems to signatures',
                     headers=['Stems', 'Signatures'],
                     row_functions=[lambda x: x[0],
                                    lambda x:
                                    ', '.join(SEP_SIG.join(sig)
                                              for sig in sorted(x[1]))],
                     column_widths=[15, 0],
                     lxa_parameters=self.parameters(),
                     test=test, encoding=self.encoding,
                     number_of_word_types=self.number_of_word_types(),
                     number_of_word_tokens=self.number_of_word_tokens(),
                     input_file_path=self.file_abspath)
        vprint('\t' + fname, verbose=verbose)

        fname = 'words_to_signatures.txt'
        obj = double_sorted(self.words_to_signatures().items(),
                            key=lambda x: len(x[1]), reverse=True)
        f_path = os.path.join(output_dir, fname)
        output_latex(obj, f_path,
                     title='Words to signatures',
                     headers=['Word', 'Sig count', 'Signatures'],
                     row_functions=[lambda x: x[0],
                                    lambda x: len(x[1]),
                                    lambda x:
                                    ', '.join(SEP_SIG.join(sig)
                                              for sig in sorted(x[1]))],
                     column_widths=[25, 15, 0],
                     lxa_parameters=self.parameters(),
                     test=test, encoding=self.encoding,
                     number_of_word_types=self.number_of_word_types(),
                     number_of_word_tokens=self.number_of_word_tokens(),
                     input_file_path=self.file_abspath)
        vprint('\t' + fname, verbose=verbose)

        fname = 'signatures_to_words.txt'
        obj = double_sorted(self.signatures_to_words().items(),
                            key=lambda x: len(x[1]), reverse=True)
        f_path = os.path.join(output_dir, fname)
        output_latex(obj, f_path,
                     title='Signatures to words',
                     headers=['Signature', 'Word count', 'Words'],
                     row_functions=[lambda x: SEP_SIG.join(x[0]),
                                    lambda x: len(x[1]),
                                    lambda x: ', '.join(sorted(x[1]))],
                     column_widths=[20, 15, 0],
                     lxa_parameters=self.parameters(),
                     test=test, encoding=self.encoding,
                     number_of_word_types=self.number_of_word_types(),
                     number_of_word_tokens=self.number_of_word_tokens(),
                     input_file_path=self.file_abspath)
        vprint('\t' + fname, verbose=verbose)

        fname = 'signatures_to_words_truncated.txt'
        obj = double_sorted(self.signatures_to_words().items(),
                            key=lambda x: len(x[1]), reverse=True)
        f_path = os.path.join(output_dir, fname)
        output_latex(obj, f_path,
                     title='Signatures to words '
                           '(first 10 words for each sig)',
                     headers=['Signature', 'Word count', '1st 10 words'],
                     row_functions=[lambda x: SEP_SIG.join(x[0]),
                                    lambda x: len(x[1]),
                                    lambda x:
                                    ', '.join(sorted(x[1])[:10])],
                     column_widths=[20, 15, 0],
                     lxa_parameters=self.parameters(),
                     test=test, encoding=self.encoding,
                     number_of_word_types=self.number_of_word_types(),
                     number_of_word_tokens=self.number_of_word_tokens(),
                     input_file_path=self.file_abspath)
        vprint('\t' + fname, verbose=verbose)

        fname = 'words_to_sigtransforms.txt'
        obj = double_sorted(self.words_to_sigtransforms().items(),
                            key=lambda x: len(x[1]), reverse=True)
        f_path = os.path.join(output_dir, fname)
        output_latex(obj, f_path,
                     title='Words to sigtransforms',
                     headers=['Word', 'Signature transforms'],
                     row_functions=[lambda x: x[0],
                                    lambda x:
                                    ', '.join(SEP_SIG.join(sig) +
                                              SEP_SIGTRANSFORM + affix
                                              for sig, affix in sorted(x[1]))],
                     column_widths=[20, 0],
                     lxa_parameters=self.parameters(),
                     test=test, encoding=self.encoding,
                     number_of_word_types=self.number_of_word_types(),
                     number_of_word_tokens=self.number_of_word_tokens(),
                     input_file_path=self.file_abspath)
        vprint('\t' + fname, verbose=verbose)

        fname = 'affixes_to_signatures.txt'
        obj = double_sorted(self.affixes_to_signatures().items(),
                            key=lambda x: len(x[1]), reverse=True)
        f_path = os.path.join(output_dir, fname)
        output_latex(obj, f_path,
                     title='Affixes to signatures',
                     headers=['Affix', 'Sig count', 'Signatures'],
                     row_functions=[lambda x: x[0],
                                    lambda x: len(x[1]),
                                    lambda x:
                                    ', '.join(SEP_SIG.join(sig)
                                              for sig in sorted(x[1]))],
                     column_widths=[15, 15, 0],
                     lxa_parameters=self.parameters(),
                     test=test, encoding=self.encoding,
                     number_of_word_types=self.number_of_word_types(),
                     number_of_word_tokens=self.number_of_word_tokens(),
                     input_file_path=self.file_abspath)
        vprint('\t' + fname, verbose=verbose)

        # ----------------------------------------------------------------------
        if self.corpus_file_object:
            vprint('manifold objects', verbose=verbose)

            fname = 'words_to_neighbors.txt'
            obj = list()  # list of tuple(word, list of neighbor words)
            for word in self.wordlist()[: self.parameters()['max_word_types']]:
                obj.append((word, self.words_to_neighbors()[word]))
            f_path = os.path.join(output_dir, fname)
            output_latex(obj, f_path,
                         title='Words to neighbors',
                         headers=['Word', 'Neighbors'],
                         row_functions=[lambda x: x[0],
                                        lambda x: ' '.join(x[1])],
                         column_widths=[25, 0],
                         lxa_parameters=self.parameters(),
                         test=test, encoding=self.encoding,
                         number_of_word_types=self.number_of_word_types(),
                         number_of_word_tokens=self.number_of_word_tokens(),
                         input_file_path=self.file_abspath)
            vprint('\t' + fname, verbose=verbose)

        # ----------------------------------------------------------------------
        vprint('phon objects', verbose=verbose)

        def output_latex_for_phon_words(obj_, f_path_, title_, lxa_parameters_,
                                        test_, encoding_, number_of_word_types_,
                                        number_of_word_tokens_,
                                        input_file_path_):
            output_latex(obj_, f_path_,
                         title=title_,
                         headers=['Word', 'Count', 'Frequency', 'Phones',
                                  'Unigram plog', 'Avg unigram plog',
                                  'Bigram plog', 'Avg bigram plog'],
                         row_functions=[lambda x: x[0],
                                        lambda x: x[1].count,
                                        lambda x:
                                        '%.6f' % x[1].frequency,
                                        lambda x:
                                        ' '.join(x[1].phones),
                                        lambda x:
                                        '%8.3f' % x[1].unigram_plog,
                                        lambda x:
                                        '%8.3f' % x[1].avg_unigram_plog,
                                        lambda x:
                                        '%8.3f' % x[1].bigram_plog,
                                        lambda x:
                                        '%8.3f' % x[1].avg_bigram_plog,
                                        ],
                         column_widths=[35, 10, 15, 60, 15, 15, 15, 15],
                         lxa_parameters=lxa_parameters_,
                         test=test_, encoding=encoding_,
                         number_of_word_types=number_of_word_types_,
                         number_of_word_tokens=number_of_word_tokens_,
                         input_file_path=input_file_path_)

        fname = 'wordlist.txt'
        obj_word_phon = list()  # list of tuple(word, list of neighbor words)
        for word in self.wordlist():
            obj_word_phon.append((word, self.word_phonology_dict()[word]))
        f_path = os.path.join(output_dir, 'wordlist.txt')
        output_latex_for_phon_words(obj_word_phon, f_path,
                                    'Wordlist sorted by word count',
                                    self.parameters(), test, self.encoding,
                                    self.number_of_word_types(),
                                    self.number_of_word_tokens(),
                                    self.file_abspath)
        vprint('\t' + fname, verbose=verbose)

        fname = 'wordlist_by_avg_unigram_plog.txt'
        obj_unigram_plog = double_sorted(obj_word_phon,
                                         key=lambda x: x[1].avg_unigram_plog,
                                         reverse=False)
        f_path = os.path.join(output_dir, fname)
        output_latex_for_phon_words(obj_unigram_plog, f_path,
                                    'Wordlist sorted by avg unigram plog',
                                    self.parameters(), test, self.encoding,
                                    self.number_of_word_types(),
                                    self.number_of_word_tokens(),
                                    self.file_abspath)
        vprint('\t' + fname, verbose=verbose)

        fname = 'wordlist_by_avg_bigram_plog.txt'
        obj_bigram_plog = double_sorted(obj_word_phon,
                                        key=lambda x: x[1].avg_bigram_plog,
                                        reverse=False)
        f_path = os.path.join(output_dir, fname)
        output_latex_for_phon_words(obj_bigram_plog, f_path,
                                    'Wordlist sorted by avg bigram plog',
                                    self.parameters(), test, self.encoding,
                                    self.number_of_word_types(),
                                    self.number_of_word_tokens(),
                                    self.file_abspath)
        vprint('\t' + fname, verbose=verbose)

        fname = 'phones.txt'
        obj = double_sorted(self.phone_dict().items(),
                            key=lambda x: x[1].count, reverse=True)
        f_path = os.path.join(output_dir, fname)
        output_latex(obj, f_path,
                     title='Phones',
                     headers=['Phone', 'Count', 'Frequency', 'Plog'],
                     row_functions=[lambda x: x[0],
                                    lambda x: x[1].count,
                                    lambda x: '%.6f' % x[1].frequency,
                                    lambda x: '%8.3f' % x[1].plog,
                                    ],
                     column_widths=[10, 10, 15, 15],
                     lxa_parameters=self.parameters(),
                     test=test, encoding=self.encoding,
                     number_of_word_types=self.number_of_word_types(),
                     number_of_word_tokens=self.number_of_word_tokens(),
                     input_file_path=self.file_abspath)
        vprint('\t' + fname, verbose=verbose)

        fname = 'biphones.txt'
        obj = double_sorted(self.biphone_dict().items(),
                            key=lambda x: x[1].count, reverse=True)
        f_path = os.path.join(output_dir, fname)
        output_latex(obj, f_path,
                     title='Biphones',
                     headers=['Biphone', 'Count', 'Frequency',
                              'MI', 'Weighted MI'],
                     row_functions=[lambda x: ' '.join(x[0]),
                                    lambda x: x[1].count,
                                    lambda x:
                                    '%.6f' % x[1].frequency,
                                    lambda x:
                                    '%8.3f' % x[1].MI,
                                    lambda x:
                                    '%8.3f' % x[1].weighted_MI,
                                    ],
                     column_widths=[10, 10, 15, 15, 15],
                     lxa_parameters=self.parameters(),
                     test=test, encoding=self.encoding,
                     number_of_word_types=self.number_of_word_types(),
                     number_of_word_tokens=self.number_of_word_tokens(),
                     input_file_path=self.file_abspath)
        vprint('\t' + fname, verbose=verbose)

        fname = 'triphones.txt'
        obj = double_sorted(self.phone_trigram_counter().items(),
                            key=lambda x: x[1], reverse=True)
        f_path = os.path.join(output_dir, fname)
        output_latex(obj, f_path,
                     title='Triphones',
                     headers=['Triphone', 'Count'],
                     row_functions=[lambda x: ' '.join(x[0]),
                                    lambda x: x[1],
                                    ],
                     column_widths=[15, 10],
                     lxa_parameters=self.parameters(),
                     test=test, encoding=self.encoding,
                     number_of_word_types=self.number_of_word_types(),
                     number_of_word_tokens=self.number_of_word_tokens(),
                     input_file_path=self.file_abspath)
        vprint('\t' + fname, verbose=verbose)

        # ----------------------------------------------------------------------
        vprint('trie objects', verbose=verbose)

        fname = 'words_as_tries.txt'
        obj = list()
        for word in self.wordlist():
            obj.append((word,
                        self.broken_words_left_to_right()[word],
                        self.broken_words_right_to_left()[word]))
        f_path = os.path.join(output_dir, fname)
        output_latex(obj, f_path,
                     title='Words as tries',
                     headers=['Word', 'Left-to-right trie',
                              'Right-to-left trie'],
                     row_functions=[lambda x: x[0],
                                    lambda x: ' '.join(x[1]),
                                    lambda x: ' '.join(x[2]),
                                    ],
                     column_widths=[35, 50, 50],
                     lxa_parameters=self.parameters(),
                     test=test, encoding=self.encoding,
                     number_of_word_types=self.number_of_word_types(),
                     number_of_word_tokens=self.number_of_word_tokens(),
                     input_file_path=self.file_abspath)
        vprint('\t' + fname, verbose=verbose)

        fname = 'successors.txt'
        obj = double_sorted(self.successors().items(),
                            key=lambda x: len(x[1]), reverse=False)
        f_path = os.path.join(output_dir, fname)
        output_latex(obj, f_path,
                     title='Successors',
                     headers=['String', 'Successors'],
                     row_functions=[lambda x: x[0],
                                    lambda x: ' '.join(sorted(x[1])),
                                    ],
                     column_widths=[35, 0],
                     lxa_parameters=self.parameters(),
                     test=test, encoding=self.encoding,
                     number_of_word_types=self.number_of_word_types(),
                     number_of_word_tokens=self.number_of_word_tokens(),
                     input_file_path=self.file_abspath)
        vprint('\t' + fname, verbose=verbose)

        fname = 'predecessors.txt'
        obj = double_sorted(self.predecessors().items(),
                            key=lambda x: len(x[1]), reverse=False)
        f_path = os.path.join(output_dir, fname)
        output_latex(obj, f_path,
                     title='Predecessors',
                     headers=['String', 'Predecessors'],
                     row_functions=[lambda x: x[0],
                                    lambda x: ' '.join(sorted(x[1])),
                                    ],
                     column_widths=[35, 0],
                     lxa_parameters=self.parameters(),
                     test=test, encoding=self.encoding,
                     number_of_word_types=self.number_of_word_types(),
                     number_of_word_tokens=self.number_of_word_tokens(),
                     input_file_path=self.file_abspath)
        vprint('\t' + fname, verbose=verbose)

    # --------------------------------------------------------------------------
    # for number of word types and tokens

    def number_of_word_types(self):
        """
        Return the number of word types.

        :rtype: int
        """
        if self._number_of_word_types is None:
            self._number_of_word_types = len(self.word_unigram_counter())
        return self._number_of_word_types

    def number_of_word_tokens(self):
        """
        Return the number of word tokens.

        :rtype: int
        """
        if self._number_of_word_tokens is None:
            self._number_of_word_tokens = sum(self.word_unigram_counter()
                                              .values())
        return self._number_of_word_tokens

    # --------------------------------------------------------------------------
    # for the "ngram" module

    def word_unigram_counter(self):
        """
        Return a dict of words with their counts.

        :rtype: dict(str: in)
        """
        if self._word_unigram_counter is None:
            if self.corpus_file_object:
                self._make_word_ngrams_from_corpus_file_object()
            elif self.wordlist_file_object:
                self._read_from_wordlist_file_object()

        return self._word_unigram_counter

    def word_bigram_counter(self):
        """
        Return a dict of word bigrams with their counts.

        :rtype: dict(tuple(str): int)
        """
        if self._word_bigram_counter is None:
            self._make_word_ngrams_from_corpus_file_object()
        return self._word_bigram_counter

    def word_trigram_counter(self):
        """
        Return a dict of word trigrams with their counts.

        :rtype: dict(tuple(str): int)
        """
        if self._word_trigram_counter is None:
            self._make_word_ngrams_from_corpus_file_object()
        return self._word_trigram_counter

    def _make_wordlist(self):
        """
        Return a wordlist sorted by word frequency in descending order.
        (So "the" will most likely be the first word for written English.)
        """
        word_counter = self.word_unigram_counter()
        word_counter_sorted = double_sorted(word_counter.items(),
                                            key=lambda x: x[1], reverse=True)
        self._wordlist = [word for word, _ in word_counter_sorted]

    def wordlist(self):
        """
        Return a wordlist sorted by word frequency in descending order.
        (So "the" will most likely be the first word for written English.)

        :rtype: list(str)
        """
        if self._wordlist is None:
            self._make_wordlist()
        return self._wordlist

    def _read_from_wordlist_file_object(self):
        word_freq_dict = dict()
        words_to_phones = dict()

        for line in self.wordlist_file_object:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            word, *rest = line.split()

            if not self.parameters_['keep_case']:
                word = word.lower()

            try:
                freq = int(rest[0])
            except (ValueError, IndexError):
                freq = 1

            phones = rest[1:]
            if not phones:
                phones = list(word)

            word_freq_dict[word] = freq
            words_to_phones[word] = phones

        self._word_unigram_counter = word_freq_dict
        self._words_to_phones = words_to_phones

    def _make_word_ngrams_from_corpus_file_object(self):
        if self.corpus_file_object is None:
            self._word_bigram_counter = dict()
            self._word_trigram_counter = dict()
            return

        unigrams, bigrams, trigrams = ngram.run(
            corpus_file_object=self.corpus_file_object,
            keep_case=self.parameters_['keep_case'],
            max_word_tokens=self.parameters_['max_word_tokens'])

        self._word_unigram_counter = unigrams
        self._word_bigram_counter = bigrams
        self._word_trigram_counter = trigrams

    def run_ngram_module(self, verbose=False):
        """
        Run the ngram module.
        """
        vprint('Extracting word ngrams...', verbose=verbose)
        if self._wordlist is None:
            self._make_wordlist()

    # --------------------------------------------------------------------------
    # for the "signature" module

    def stems_to_words(self):
        """
        Return a dict of stems to words.

        :rtype: dict(str: set(str))
        """
        if self._stems_to_words is None:
            self._make_all_signature_objects()
        return self._stems_to_words

    def signatures_to_stems(self):
        """
        Return a dict of morphological signatures to stems.

        :rtype: dict(tuple(str): set(str))
        """
        if self._signatures_to_stems is None:
            self._make_all_signature_objects()
        return self._signatures_to_stems

    def stems_to_signatures(self):
        """
        Return a dict of stems to morphological signatures.

        :rtype: dict(str: set(tuple(str)))
        """
        if self._stems_to_signatures is None:
            self._make_all_signature_objects()
        return self._stems_to_signatures

    def words_to_signatures(self):
        """
        Return a dict of words to morphological signatures.

        :rtype: dict(str: set(tuple(str)))
        """
        if self._words_to_signatures is None:
            self._make_all_signature_objects()
        return self._words_to_signatures

    def signatures_to_words(self):
        """
        Return a dict of morphological signatures to words.

        :rtype: dict(tuple(str): set(str))
        """
        if self._signatures_to_words is None:
            self._make_all_signature_objects()
        return self._signatures_to_words

    def words_to_sigtransforms(self):
        """
        Return a dict of words to signature transforms.

        :rtype: dict(str: set(tuple(tuple(str), str))
        """
        if self._words_to_sigtransforms is None:
            self._make_all_signature_objects()
        return self._words_to_sigtransforms

    def signatures(self):
        """
        Return a set of morphological signatures.

        :rtype: set(tuple(str))
        """
        if self._signatures is None:
            self._make_all_signature_objects()
        return self._signatures

    def affixes_to_signatures(self):
        """
        Return a dict of affixes to morphological signatures.

        :rtype: dict(str: set(tuple(str)))
        """
        if self._affixes_to_signatures is None:
            self._make_all_signature_objects()
        return self._affixes_to_signatures

    def words_in_signatures(self):
        """
        Return a set of words that are in at least one morphological signature.

        :rtype: set(str)
        """
        if self._words_in_signatures is None:
            self._make_all_signature_objects()
        return self._words_in_signatures

    def affixes(self):
        """
        Return a set of affixes.

        :rtype: set(str)
        """
        if self._affixes is None:
            self._make_all_signature_objects()
        return self._affixes

    def stems(self):
        """
        Return a set of stems.

        :rtype: set(str)
        """
        if self._stems is None:
            self._make_all_signature_objects()
        return self._stems

    def _make_all_signature_objects(self):
        self._stems_to_words = signature.make_stems_to_words(
            self.wordlist(), self.parameters_['min_stem_length'],
            self.parameters_['max_affix_length'], self.parameters_['suffixing'],
            self.parameters_['min_sig_count'])

        self._signatures_to_stems = signature.make_signatures_to_stems(
            self._stems_to_words, self.parameters_['max_affix_length'],
            self.parameters_['min_sig_count'], self.parameters_['suffixing'])

        self._stems_to_signatures = signature.make_stems_to_signatures(
            self._signatures_to_stems)

        self._words_to_signatures = signature.make_words_to_signatures(
            self._stems_to_words, self._stems_to_signatures)

        self._signatures_to_words = signature.make_signatures_to_words(
            self._words_to_signatures)

        self._words_to_sigtransforms = signature.make_words_to_sigtransforms(
            self._words_to_signatures, self.parameters_['suffixing'])

        self._signatures = set(self._signatures_to_stems.keys())

        self._affixes_to_signatures = signature.make_affixes_to_signatures(
            self._signatures)

        self._words_in_signatures = set(self._words_to_signatures.keys())
        self._affixes = set(self._affixes_to_signatures.keys())
        self._stems = set(self._stems_to_words.keys())

    def run_signature_module(self, verbose=False):
        """
        Run the signature module.
        """
        vprint('Morphological signatures...', verbose=verbose)
        self._make_all_signature_objects()

    # --------------------------------------------------------------------------
    # for the "manifold" module

    def words_to_neighbors(self):
        """
        Return a dict of words to syntactic neighbors.

        :rtype: dict(word: list(str))
        """
        if self._words_to_neighbors is None:
            self._make_all_manifold_objects()
        return self._words_to_neighbors

    def words_to_contexts(self):
        """
        Return a dict of words to contexts with counts.

        :rtype: dict(str: dict(tuple(str): int))
        """
        if self._words_to_contexts is None:
            self._make_all_manifold_objects()
        return self._words_to_contexts

    def contexts_to_words(self):
        """
        Return a dict of contexts to words with counts.

        :rtype: dict(tuple(str): dict(str: int))
        """
        if self._contexts_to_words is None:
            self._make_all_manifold_objects()
        return self._contexts_to_words

    def neighbor_graph(self):
        """
        Return the syntactic word neighborhood graph.

        :rtype: networkx undirected graph
        """
        if self._neighbor_graph is None:
            self._make_all_manifold_objects()
        return self._neighbor_graph

    def _make_all_manifold_objects(self):
        self._words_to_neighbors, self._words_to_contexts, \
        self._contexts_to_words = manifold.run(
            self.word_unigram_counter(),
            self.word_bigram_counter(),
            self.word_trigram_counter(),
            self.parameters_['max_word_types'],
            self.parameters_['n_neighbors'],
            self.parameters_['n_eigenvectors'],
            self.parameters_['min_context_count'])
        self._neighbor_graph = manifold.compute_graph(self._words_to_neighbors)

    def run_manifold_module(self, verbose=False):
        """
        Run the phon module.
        """
        vprint('Syntactic word neighbors...', verbose=verbose)
        if self.corpus_file_object:
            self._make_all_manifold_objects()

    # --------------------------------------------------------------------------
    # for the "phon" module

    def phone_unigram_counter(self):
        """
        Return a dict of phone unigrams with counts.

        :rtype: dict(str: int)
        """
        if self._phone_unigram_counter is None:
            self._make_all_phon_objects()
        return self._phone_unigram_counter

    def phone_bigram_counter(self):
        """
        Return a dict of phone bigrams with counts.

        :rtype: dict(tuple(str): int)
        """
        if self._phone_bigram_counter is None:
            self._make_all_phon_objects()
        return self._phone_bigram_counter

    def phone_trigram_counter(self):
        """
        Return a dict of phone trigrams with counts.

        :rtype: dict(tuple(str): int)
        """
        if self._phone_trigram_counter is None:
            self._make_all_phon_objects()
        return self._phone_trigram_counter

    def phone_dict(self):
        """
        Return a dict of phone unigrams to Phone objects.
        A Phone instance has the methods
        ``spelling()``, ``count()``, ``frequency()``, and ``plog()``.

        :rtype: dict(str: Phone instance)
        """
        if self._phone_dict is None:
            self._make_all_phon_objects()
        return self._phone_dict

    def biphone_dict(self):
        """
        Return a dict of phone bigrams to Biphone objects.
        A Biphone instance has the methods
        ``spelling()``, ``count()``, ``frequency()``, ``MI()``, and
        ``weighted_MI()``.

        :rtype: dict((str, str): Biphone instance)
        """
        if self._phone_dict is None:
            self._make_all_phon_objects()
        return self._biphone_dict

    def word_phonology_dict(self):
        """
        Return a dict of words to Word objects.
        A Word instance has the methods
        ``spelling()``, ``phones()``, ``count()``, ``frequency()``,
        ``unigram_plog()``, ``avg_unigram_plog()``,
        ``bigram_plog()``, and ``avg_bigram_plog()``.

        :rtype: dict(str: Word instance)
        """
        if self._word_dict is None:
            self._make_all_phon_objects()
        return self._word_dict

    def words_to_phones(self):
        """
        Return a dict of words with their phones.

        :rtype: dict(str: list(str))
        """
        return self._words_to_phones

    def _make_all_phon_objects(self):
        word_unigram_counter = self.word_unigram_counter()
        words_to_phones = self.words_to_phones()

        self._phone_unigram_counter, self._phone_bigram_counter, \
        self._phone_trigram_counter = phon.make_word_ngrams(
            word_unigram_counter, words_to_phones)

        self._phone_dict = phon.make_phone_dict(self._phone_unigram_counter)
        self._biphone_dict = phon.make_biphone_dict(self._phone_bigram_counter,
                                                    self._phone_dict)
        self._word_dict = phon.make_word_dict(self.word_unigram_counter(),
                                              self.phone_dict(),
                                              self.biphone_dict(),
                                              self.words_to_phones())

    def run_phon_module(self, verbose=False):
        """
        Run the phon module.
        """
        vprint('Phonology...', verbose=verbose)
        self._make_all_phon_objects()

    # --------------------------------------------------------------------------
    # for the "trie" module

    def broken_words_left_to_right(self):
        """
        Return a dict of words to their left-to-right broken form.

        :rtype: dict(str: list(str))
        """
        if self._broken_words_left_to_right is None:
            self._make_all_trie_objects()
        return self._broken_words_left_to_right

    def broken_words_right_to_left(self):
        """
        Return a dict of words to their right-to-left broken form.

        :rtype: dict(str: list(str))
        """
        if self._broken_words_right_to_left is None:
            self._make_all_trie_objects()
        return self._broken_words_right_to_left

    def successors(self):
        """
        Return a dict of word (sub)strings to their successors.

        :rtype: dict(str: set(str))
        """
        if self._successors is None:
            self._make_all_trie_objects()
        return self._successors

    def predecessors(self):
        """
        Return a dict of word (sub)strings to their predecessors.

        :rtype: dict(str: set(str))
        """
        if self._predecessors is None:
            self._make_all_trie_objects()
        return self._predecessors

    def _make_all_trie_objects(self):
        self._broken_words_left_to_right, self._broken_words_right_to_left, \
        self._successors, self._predecessors = trie.run(
            self.wordlist(), self.parameters_['min_stem_length'])

    def run_trie_module(self, verbose=False):
        """
        Run the trie module.
        """
        vprint('Tries...', verbose=verbose)
        self._make_all_trie_objects()
