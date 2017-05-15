# -*- encoding: utf8 -*-

from itertools import combinations, groupby

from linguistica.util import NULL, vprint


class LexiconSignature:
    def __init__(self, wordlist, min_stem_length, max_affix_length,
                 min_sig_count, suffixing_flag):
        self._wordlist = wordlist
        self._min_stem_length = min_stem_length
        self._max_affix_length = max_affix_length
        self._min_sig_count = min_sig_count
        self._suffixing_flag = suffixing_flag

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

    def run_signature_module(self, verbose=False):
        """
        Run the signature module.
        """
        vprint(verbose, 'Morphological signatures...')
        self._make_all_signature_objects()

    def _make_all_signature_objects(self):
        self._stems_to_words = make_stems_to_words(
            self._wordlist, self._min_stem_length,
            self._max_affix_length,
            self._suffixing_flag, self._min_sig_count)

        self._signatures_to_stems = make_signatures_to_stems(
            self._stems_to_words, self._max_affix_length,
            self._min_sig_count, self._suffixing_flag)

        self._stems_to_signatures = make_stems_to_signatures(
            self._signatures_to_stems)

        self._words_to_signatures = make_words_to_signatures(
            self._stems_to_words, self._stems_to_signatures)

        self._signatures_to_words = make_signatures_to_words(
            self._words_to_signatures)

        self._words_to_sigtransforms = make_words_to_sigtransforms(
            self._words_to_signatures, self._suffixing_flag)

        self._signatures = set(self._signatures_to_stems.keys())

        self._affixes_to_signatures = make_affixes_to_signatures(
            self._signatures)

        self._words_in_signatures = set(self._words_to_signatures.keys())
        self._affixes = set(self._affixes_to_signatures.keys())
        self._stems = set(self._stems_to_words.keys())


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


def make_stems_to_signatures(sigs_to_stems):
    stems_to_sigs = dict()

    for sig in sigs_to_stems.keys():
        for stem in sigs_to_stems[sig]:
            if stem not in stems_to_sigs:
                stems_to_sigs[stem] = set()
            stems_to_sigs[stem].add(sig)

    return stems_to_sigs


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


def make_words_to_sigtransforms(words_to_sigs, suffixing):
    words_to_sigtransforms = dict()

    for word in words_to_sigs.keys():
        sigs = words_to_sigs[word]
        sigtransforms = set()

        for sig in sigs:
            for affix in sig:
                if check_affix(word, affix, suffixing):
                    sigtransforms.add((sig, affix))
                    break

        words_to_sigtransforms[word] = sigtransforms

    return words_to_sigtransforms


def make_words_to_signatures(stems_to_words, stems_to_sigs):
    words_to_sigs = dict()

    for stem in stems_to_sigs.keys():
        words = stems_to_words[stem]

        for word in words:
            if word not in words_to_sigs:
                words_to_sigs[word] = set()
            words_to_sigs[word].update(stems_to_sigs[stem])

    return words_to_sigs


def make_signatures_to_words(words_to_signatures):
    sigs_to_words = dict()

    for word in words_to_signatures.keys():
        sigs = words_to_signatures[word]

        for sig in sigs:
            if sig not in sigs_to_words:
                sigs_to_words[sig] = set()

            sigs_to_words[sig].add(word)

    return sigs_to_words


def make_signatures_to_stems(stems_to_words, max_affix_length, min_sig_count,
                             suffixing):
    signatures_to_stems = dict()

    for stem in stems_to_words.keys():
        affix_set = set()
        len_stem = len(stem)

        for word in stems_to_words[stem]:
            if word == stem:
                affix_set.add(NULL)
            else:
                len_affix = len(word) - len_stem
                if max_affix_length and len_affix > max_affix_length:
                    continue
                if suffixing:
                    affix = word[len_stem:]
                else:
                    affix = word[: len_affix]
                affix_set.add(affix)

        affix_tuple = tuple(sorted(affix_set))

        if affix_tuple not in signatures_to_stems:
            signatures_to_stems[affix_tuple] = set()

        signatures_to_stems[affix_tuple].add(stem)

    for sig in dict(signatures_to_stems):
        if len(signatures_to_stems[sig]) < min_sig_count:
            del signatures_to_stems[sig]

    return signatures_to_stems


def make_stems_to_words(wordlist, min_stem_length, max_affix_length, suffixing,
                        min_sig_count):
    bisigs_to_tuples = make_bisignatures(wordlist, min_stem_length,
                                         max_affix_length, suffixing)
    stems_to_words = dict()

    for bisig in bisigs_to_tuples.keys():  # bisig is a tuple
        if len(bisigs_to_tuples[bisig]) < min_sig_count:
            continue

        for stem, word1, word2 in bisigs_to_tuples[bisig]:
            if stem not in stems_to_words:
                stems_to_words[stem] = set()

            stems_to_words[stem].add(word1)
            stems_to_words[stem].add(word2)

    return stems_to_words


# noinspection PyPep8
def make_bisignatures(wordlist, min_stem_length, max_affix_length, suffixing):
    """
    This function finds pairs of words which make a valid signature,
    and makes Dictionary whose key is the signature and
    whose value is a tuple: stem, word1, word2.
    """
    bisigs_to_tuples = dict()

    if not suffixing:
        wordlist = sorted(wordlist, key=lambda x: x[::-1])
        group_key = lambda x: x[-min_stem_length:]  # noqa
    else:
        wordlist = sorted(wordlist)
        group_key = lambda x: x[: min_stem_length]  # noqa

    wordlist = filter(lambda x: len(x) >= min_stem_length, wordlist)

    for _, group in groupby(wordlist, key=group_key):  # groupby from itertools
        wordlist_for_analysis = list(group)  # must use list() here!
        # see python 3.4 documentation:
        # https://docs.python.org/3/library/itertools.html#itertools.groupby
        # "The returned group is itself an iterator that shares the underlying
        # iterable with groupby(). Because the source is shared, when the
        # groupby() object is advanced, the previous group is no longer
        # visible. So, if that data is needed later, it should be stored as a
        # list"

        for (word1, word2) in combinations(wordlist_for_analysis, 2):

            if suffixing:
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

            if len_affix1 > max_affix_length or \
               len_affix2 > max_affix_length:
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

    return bisigs_to_tuples


def make_affixes_to_signatures(signatures):
    affixes_to_sigs = dict()

    for sig in signatures:
        for affix in sig:
            if affix not in affixes_to_sigs:
                affixes_to_sigs[affix] = set()
            affixes_to_sigs[affix].add(sig)

    return affixes_to_sigs
