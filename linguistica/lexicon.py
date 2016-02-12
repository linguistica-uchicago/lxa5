# -*- encoding: utf-8 -*-

"""
Once a Linguistica object (such as ``lxa_object`` below with the Brown corpus)
is initialized, various methods and attributes are available for automatic
linguistic analysis:

.. code-block:: python

   >>> import linguistica as lxa
   >>> lxa_object = lxa.read_corpus('path/to/english-brown.txt')
   >>> words = lxa_object.wordlist()  # using wordlist()

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

"""

import os
import json
from io import StringIO

from linguistica import (ngram, signature, manifold, phon, trie)
from linguistica.util import (ENCODING, CONFIG_FILENAME, CONFIG,
                              double_sorted, fix_punctuations)


class Lexicon:
    """
    A class for a Linguistica object. It is called "Lexicon" for the historical
    reason that the same element in the C++ version of Linguistica 4 is also
    called as such.
    """
    def __init__(self, file_path=None, wordlist_file=False,
                 corpus_object=None, wordlist_object=None, encoding=ENCODING,
                 configfile=CONFIG_FILENAME, keep_case=False, **kwargs):
        self.file_abspath = self._check_file_path(file_path)

        if self.file_abspath is None:
            self.directory = None
        else:
            self.directory = os.path.dirname(self.file_abspath)

        self.file_is_wordlist = wordlist_file
        self.encoding = encoding
        self.corpus_object = corpus_object
        self.wordlist_object = wordlist_object
        self.configfile = configfile
        self.config = self._determine_config(**kwargs)
        self.keep_case = keep_case

        self._initialize()

    @staticmethod
    def _check_file_path(file_path):
        """
        Return the absolute path of *file_path*.
        """
        if file_path is None:
            return None

        file_abspath = os.path.abspath(file_path)
        if not os.path.isfile(file_abspath):
            raise ValueError('invalid file path -- ' + file_path)
        else:
            return file_abspath

    def _determine_config(self, **kwargs):
        """
        Determine the configuration dict.
        """
        temp_config = CONFIG
        if os.path.isfile(self.configfile):
            temp_config.update(json.load(open(self.configfile)))

        for parameter in kwargs.keys():
            if parameter not in CONFIG:
                raise ValueError('unknown config parameter -- ' + parameter)
            else:
                temp_config[parameter] = kwargs[parameter]

        return temp_config

    def _initialize(self):
        # word ngrams
        self._word_unigram_counter = None
        self._word_bigram_counter = None
        self._word_trigram_counter = None

        # wordlist
        self._wordlist = None
        if self.wordlist_object is not None:
            self._wordlist = list(set(self.wordlist_object))

        # signature-related objects
        self._stems_to_words = None
        self._signatures_to_stems = None
        self._stems_to_signatures = None
        self._words_to_signatures = None
        self._words_to_sigtransforms = None

        self._signatures = None
        self._affixes_to_signatures = None
        self._words_in_signatures = None
        self._affixes = None
        self._stems = None

        # corpus file object
        if self.corpus_object is not None:
            corpus_str = fix_punctuations(str(self.corpus_object))
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

        # trie objects
        self._broken_words_left_to_right = None
        self._broken_words_right_to_left = None
        self._successors = None
        self._predecessors = None

    def reset(self):
        """
        Reset all attributes to be ``None``.
        """
        self._initialize()

    # --------------------------------------------------------------------------
    # for the "ngrams" module

    def word_unigram_counter(self):
        """
        Return a dict of words with their counts.

        :rtype: dict(str: in)
        """
        if self._word_unigram_counter is None:
            if self.corpus_file_object:
                self._make_word_ngrams_from_corpus_file_object()
            elif self.wordlist_file_object:
                self._make_word_unigram_counter_from_wordlist_file_object()
            else:
                raise ValueError('no corpus/wordlist file object '
                                 'or wordlist object')
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

    def _make_word_unigram_counter_from_wordlist_file_object(self):
        word_freq_dict = dict()

        if self.wordlist_file_object is None:
            self._word_unigram_counter = dict()
            return

        for line in self.wordlist_file_object:
            line = line.strip()
            if not line:
                continue

            if not self.keep_case:
                line = line.lower()

            word, *rest = line.split()

            try:
                freq = int(rest[0])
            except (ValueError, IndexError):
                freq = 1

            word_freq_dict[word] = freq

        self._word_unigram_counter = word_freq_dict

    def _make_word_ngrams_from_corpus_file_object(self):
        if self.corpus_file_object is None:
            raise ValueError('No corpus available. The ngram module cannot '
                             'be run to get word ngrams.')

        unigrams, bigrams, trigrams = ngram.run(
            corpus_file_object=self.corpus_file_object,
            keep_case=self.keep_case,
            max_word_tokens=self.config['max_word_tokens'])

        self._word_unigram_counter = unigrams
        self._word_bigram_counter = bigrams
        self._word_trigram_counter = trigrams

    # --------------------------------------------------------------------------
    # for the "signatures" module

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

    def words_to_sigtransforms(self):
        """
        Return a dict of words to signature transforms.

        :rtype: dict(str: set(tuple))
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
            self.wordlist(), self.config['min_stem_length'],
            self.config['max_affix_length'], self.config['suffixing'],
            self.config['min_sig_count'])

        self._signatures_to_stems = signature.make_signatures_to_stems(
            self._stems_to_words, self.config['max_affix_length'],
            self.config['min_sig_count'], self.config['suffixing'])

        self._stems_to_signatures = signature.make_stems_to_signatures(
            self._signatures_to_stems)

        self._words_to_signatures = signature.make_words_to_signatures(
            self._stems_to_words, self._stems_to_signatures)

        self._words_to_sigtransforms = signature.make_words_to_sigtransforms(
            self._words_to_signatures, self.config['suffixing'])

        self._signatures = set(self._signatures_to_stems.keys())

        self._affixes_to_signatures = signature.make_affixes_to_signatures(
            self._signatures)

        self._words_in_signatures = set(self._words_to_signatures.keys())
        self._affixes = set(self._affixes_to_signatures.keys())
        self._stems = set(self._stems_to_words.keys())

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
                self.word_unigram_counter(), self.word_bigram_counter(),
                self.word_trigram_counter(), self.config['max_word_types'],
                self.config['n_neighbors'], self.config['n_eigenvectors'],
                self.config['min_context_count'])
        self._neighbor_graph = manifold.compute_graph(self._words_to_neighbors)

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

    def _make_all_phon_objects(self):
        self._phone_unigram_counter, self._phone_bigram_counter,\
            self._phone_trigram_counter = phon.run(self.word_unigram_counter())

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
        self._broken_words_left_to_right, self._broken_words_right_to_left,\
            self._successors, self._predecessors = trie.run(
                self.wordlist(), self.config['min_stem_length'])
