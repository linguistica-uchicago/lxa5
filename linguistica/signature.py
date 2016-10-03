# -*- encoding: utf8 -*-

"""
Representation of signatures: Ideally they are sets, but they are tuples instead
because many return objects are dictionaries with signatures as keys, and
sets cannot be keys.
"""

from itertools import (combinations, groupby)

from linguistica.util import NULL


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


# noinspection PyPep8
def check_affix(word, affix, suffixing):
    if suffixing:
        is_affix = lambda word_, affix_: word_.endswith(affix_)
    else:
        is_affix = lambda word_, affix_: word_.startswith(affix_)

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


#def make_stems_to_words(wordlist, min_stem_length, max_affix_length, suffixing,
#                        min_sig_count):
# removed JG 

# noinspection PyPep8
#def make_bisignatures(wordlist, min_stem_length, max_affix_length, suffixing):
#    
# removed JG
def make_affixes_to_signatures(signatures):
    affixes_to_sigs = dict()

    for sig in signatures:
        for affix in sig:
            if affix not in affixes_to_sigs:
                affixes_to_sigs[affix] = set()
            affixes_to_sigs[affix].add(sig)

    return affixes_to_sigs

