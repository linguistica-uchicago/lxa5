# -*- encoding: utf8 -*-

from itertools import combinations, groupby

from linguistica.util import NULL, vprint


class Lexicon_BiSig:
    def __init__(self, wordlist, min_stem_length, max_affix_length,
                 min_sig_count, suffixing_flag):

        # ------------------------------------------------------------------- #
        # All signature-related objects are computed based on these (and only
        # these) objects:
        self._wordlist = wordlist
        self._min_stem_length = min_stem_length
        self._max_affix_length = max_affix_length
        self._min_sig_count = min_sig_count
        self._suffixing_flag = suffixing_flag

        # ------------------------------------------------------------------- #
        # All computed signature-related objects are cached at these
        # self._xyz attributes. These attributes are accessed by the end user
        # through the corresponding self.xyz() methods.
        # The computation of the self._xyz attributes is triggered by
        # the self._make_all_signature_objects() method.
        self._stems_to_words = None
        self._signatures_to_stems = None
        self._stems_to_signatures = None
        self._words_to_signatures = None
        self._signatures_to_words = None
        self._words_to_sigtransforms = None

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

    def run_signature_module(self, verbose=False):
        """
        Run the signature module.
        """
        vprint(verbose, 'Morphological signatures...')
        self._make_all_signature_objects()

    def _make_all_signature_objects(self):
        bisigs_to_tuples = {}

        if not self._suffixing_flag:
            wordlist = sorted(self._wordlist, key=lambda x: x[::-1])
            group_key = lambda x: x[-self._min_stem_length:]  # noqa
        else:
            wordlist = sorted(self._wordlist)
            group_key = lambda x: x[: self._min_stem_length]  # noqa

        wordlist = filter(lambda x: len(x) >= self._min_stem_length, wordlist)

        for _, group in groupby(wordlist,
                                key=group_key):  # groupby from itertools
            wordlist_for_analysis = list(group)  # must use list() here!
            # see python 3 documentation:
            # https://docs.python.org/3/library/itertools.html#itertools.groupby
            # "The returned group is itself an iterator that shares the
            # underlying iterable with groupby(). Because the source is shared,
            # when the groupby() object is advanced, the previous group is no
            # longer visible. So, if that data is needed later, it should be
            # stored as a list"

            for (word1, word2) in combinations(wordlist_for_analysis, 2):

                if self._suffixing_flag:
                    stem = max_common_prefix(word1, word2)
                    len_stem = len(stem)
                    affix1 = word1[len_stem:]
                    affix2 = word2[len_stem:]
                else:
                    stem = max_common_suffix(word1, word2)
                    len_stem = len(stem)
                    affix1 = word1[: -len_stem]
                    affix2 = word2[: -len_stem]

                len_affix1 = len(affix1)
                len_affix2 = len(affix2)

                if (len_affix1 > self._max_affix_length or
                        len_affix2 > self._max_affix_length):
                    continue

                if len_affix1 == 0:
                    affix1 = NULL
                if len_affix2 == 0:
                    affix2 = NULL

                bisig = tuple({affix1, affix2})

                if bisig not in bisigs_to_tuples:
                    bisigs_to_tuples[bisig] = set()
                chunk = (stem, word1, word2)
                bisigs_to_tuples[bisig].add(chunk)

        self._stems_to_words = {}

        for bisig in bisigs_to_tuples.keys():  # bisig is a tuple
            if len(bisigs_to_tuples[bisig]) < self._min_sig_count:
                continue

            for stem, word1, word2 in bisigs_to_tuples[bisig]:
                if stem not in self._stems_to_words:
                    self._stems_to_words[stem] = set()

                self._stems_to_words[stem].add(word1)
                self._stems_to_words[stem].add(word2)

        self._signatures_to_stems = {}

        for stem in self._stems_to_words.keys():
            affix_set = set()
            len_stem = len(stem)

            for word in self._stems_to_words[stem]:
                if word == stem:
                    affix_set.add(NULL)
                else:
                    len_affix = len(word) - len_stem
                    if (self._max_affix_length and
                            len_affix > self._max_affix_length):
                        continue
                    if self._suffixing_flag:
                        affix = word[len_stem:]
                    else:
                        affix = word[: len_affix]
                    affix_set.add(affix)

            affix_tuple = tuple(sorted(affix_set))

            if affix_tuple not in self._signatures_to_stems:
                self._signatures_to_stems[affix_tuple] = set()

            self._signatures_to_stems[affix_tuple].add(stem)

        for sig in dict(self._signatures_to_stems):
            if len(self._signatures_to_stems[sig]) < self._min_sig_count:
                del self._signatures_to_stems[sig]

        self._stems_to_signatures = {}
        for sig in self._signatures_to_stems.keys():
            for stem in self._signatures_to_stems[sig]:
                if stem not in self._stems_to_signatures:
                    self._stems_to_signatures[stem] = set()
                self._stems_to_signatures[stem].add(sig)

        self._words_to_signatures = {}
        for stem in self._stems_to_signatures.keys():
            words = self._stems_to_words[stem]
            for word in words:
                if word not in self._words_to_signatures:
                    self._words_to_signatures[word] = set()
                self._words_to_signatures[word].update(
                    self._stems_to_signatures[stem])

        self._signatures_to_words = {}
        for word in self._words_to_signatures.keys():
            sigs = self._words_to_signatures[word]
            for sig in sigs:
                if sig not in self._signatures_to_words:
                    self._signatures_to_words[sig] = set()
                self._signatures_to_words[sig].add(word)

        self._words_to_sigtransforms = {}
        for word in self._words_to_signatures.keys():
            sigs = self._words_to_signatures[word]
            sigtransforms = set()
            for sig in sigs:
                for affix in sig:
                    if check_affix(word, affix, self._suffixing_flag):
                        sigtransforms.add((sig, affix))
                        break
            self._words_to_sigtransforms[word] = sigtransforms


def max_common_prefix(a, b):
    if len(a) < len(b):
        return max_common_prefix(b, a)
    shorter_word_length = len(b)

    for i in range(shorter_word_length):
        if not a[i] == b[i]:
            return a[:i]
    return a[: shorter_word_length]


def max_common_suffix(a, b):
    return max_common_prefix(a[::-1], b[::-1])[::-1]


def check_affix(word, affix, suffixing):
    if suffixing:
        is_affix = lambda word_, affix_: word_.endswith(affix_)  # noqa
    else:
        is_affix = lambda word_, affix_: word_.startswith(affix_)  # noqa

    if affix == NULL:
        affix = ""
    if is_affix(word, affix):
        return True
    else:
        return False
