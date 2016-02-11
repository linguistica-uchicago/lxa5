# -*- encoding: utf-8 -*-

import os
import json
from io import StringIO

from linguistica import (ngrams, signatures, manifold, phon)
from linguistica.util import (ENCODING, CONFIG_FILENAME, CONFIG,
                              double_sorted, fix_punctuations)


class Lexicon:
    def __init__(self, file_path=None, wordlist_file=False,
                 corpus_object=None, wordlist_object=None, encoding=ENCODING,
                 configfile=CONFIG_FILENAME, keep_case=False, **kwargs):
        self.file_abspath = self.check_file_path(file_path)

        if self.file_abspath is None:
            self.directory = None
        else:
            self.directory = os.path.dirname(self.file_abspath)

        self.file_is_wordlist = wordlist_file
        self.encoding = encoding
        self.corpus_object = corpus_object
        self.wordlist_object = wordlist_object
        self.configfile = configfile
        self.config = self.determine_config(**kwargs)
        self.keep_case = keep_case

        self._initialize()

    @staticmethod
    def check_file_path(file_path):
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

    def determine_config(self, **kwargs):
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
            self._wordlist = list(self.wordlist_object)

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

        # phon-related objects
        self._phone_unigram_counter = None
        self._phone_bigram_counter = None
        self._phone_trigram_counter = None

    def reset(self):
        """
        Reset all data objects.
        """
        self._initialize()

    # --------------------------------------------------------------------------
    # for the "ngrams" module

    def word_unigram_counter(self):
        """
        Return a dict of words with their counts.
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
        """
        if self._word_bigram_counter is None:
            self._make_word_ngrams_from_corpus_file_object()
        return self._word_bigram_counter

    def word_trigram_counter(self):
        """
        Return a dict of word trigrams with their counts.
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
        unigrams, bigrams, trigrams = ngrams.run(
            corpus_file_object=self.corpus_file_object,
            keep_case=self.keep_case,
            max_word_tokens=self.config['max_word_tokens'])

        self._word_unigram_counter = unigrams
        self._word_bigram_counter = bigrams
        self._word_trigram_counter = trigrams

    # --------------------------------------------------------------------------
    # for the "signatures" module

    def stems_to_words(self):
        if self._stems_to_words is None:
            self._make_all_signature_objects()
        return self._stems_to_words

    def signatures_to_stems(self):
        if self._signatures_to_stems is None:
            self._make_all_signature_objects()
        return self._signatures_to_stems

    def stems_to_signatures(self):
        if self._stems_to_signatures is None:
            self._make_all_signature_objects()
        return self._stems_to_signatures

    def words_to_signatures(self):
        if self._words_to_signatures is None:
            self._make_all_signature_objects()
        return self._words_to_signatures

    def words_to_sigtransforms(self):
        if self._words_to_sigtransforms is None:
            self._make_all_signature_objects()
        return self._words_to_sigtransforms

    def signatures(self):
        if self._signatures is None:
            self._make_all_signature_objects()
        return self._signatures

    def affixes_to_signatures(self):
        if self._affixes_to_signatures is None:
            self._make_all_signature_objects()
        return self._affixes_to_signatures

    def words_in_signatures(self):
        if self._words_in_signatures is None:
            self._make_all_signature_objects()
        return self._words_in_signatures

    def affixes(self):
        if self._affixes is None:
            self._make_all_signature_objects()
        return self._affixes

    def stems(self):
        if self._stems is None:
            self._make_all_signature_objects()
        return self._stems

    def _make_all_signature_objects(self):
        self._stems_to_words = signatures.make_stems_to_words(
            self.wordlist(), self.config['min_stem_length'],
            self.config['max_affix_length'], self.config['suffixing'],
            self.config['min_sig_count'])

        self._signatures_to_stems = signatures.make_signatures_to_stems(
            self._stems_to_words, self.config['max_affix_length'],
            self.config['min_sig_count'], self.config['suffixing'])

        self._stems_to_signatures = signatures.make_stems_to_signatures(
            self._signatures_to_stems)

        self._words_to_signatures = signatures.make_words_to_signatures(
            self._stems_to_words, self._stems_to_signatures)

        self._words_to_sigtransforms = signatures.make_words_to_sigtransforms(
            self._words_to_signatures, self.config['suffixing'])

        self._signatures = set(self._signatures_to_stems.keys())

        self._affixes_to_signatures = signatures.make_affixes_to_signatures(
            self._signatures)

        self._words_in_signatures = set(self._words_to_signatures.keys())
        self._affixes = set(self._affixes_to_signatures.keys())
        self._stems = set(self._stems_to_words.keys())

    # --------------------------------------------------------------------------
    # for the "manifold" module

    def words_to_neighbors(self):
        if self._words_to_neighbors is None:
            self._make_all_manifold_objects()
        return self._words_to_neighbors

    def words_to_contexts(self):
        if self._words_to_contexts is None:
            self._make_all_manifold_objects()
        return self._words_to_contexts

    def contexts_to_words(self):
        if self._contexts_to_words is None:
            self._make_all_manifold_objects()
        return self._contexts_to_words

    def neighbor_graph(self):
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
        if self._phone_unigram_counter is None:
            self._make_all_phon_objects()
        return self._phone_unigram_counter

    def phone_bigram_counter(self):
        if self._phone_bigram_counter is None:
            self._make_all_phon_objects()
        return self._phone_bigram_counter

    def phone_trigram_counter(self):
        if self._phone_trigram_counter is None:
            self._make_all_phon_objects()
        return self._phone_trigram_counter

    def _make_all_phon_objects(self):
        self._phone_unigram_counter, self._phone_bigram_counter,\
            self._phone_trigram_counter = phon.run(self.word_unigram_counter())
