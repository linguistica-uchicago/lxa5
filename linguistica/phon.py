# -*- encoding: utf8 -*-

import math
from collections import Counter


def plog(x):
    return -1 * math.log2(x)


class Phone:
    def __init__(self, spelling, count, freq):
        self._spelling = spelling
        self._count = count
        self._frequency = freq

    def spelling(self):
        return self._spelling

    def count(self):
        return self._count

    def frequency(self):
        return self._frequency

    def plog(self):
        return plog(self._frequency)


# noinspection PyPep8Naming
class Biphone:
    def __init__(self, phone1, phone2, count, freq):
        self.phone1 = phone1
        self.phone2 = phone2

        self._spelling = (self.phone1.spelling, self.phone2.spelling)
        self._count = count
        self._frequency = freq

    def spelling(self):
        return self._spelling

    def count(self):
        return self._count

    def frequency(self):
        return self._frequency

    def MI(self):
        return self.phone1.plog() + self.phone2.plog() - plog(self._frequency)

    def weighted_MI(self):
        return self.MI() * self._count


class Word:
    def __init__(self, spelling, phones, count, freq, phone_dict, biphone_dict):
        self._spelling = spelling
        self._phones = phones
        self._count = count
        self._frequency = freq

        self.phone_dict = phone_dict
        self.biphone_dict = biphone_dict

        if len(self._phones) < 3:
            print(spelling, phones)

    def spelling(self):
        return self._spelling

    def phones(self):
        return self._phones

    def count(self):
        return self._count

    def frequency(self):
        return self._frequency

    def unigram_plog(self):
        _unigram_plog = 0

        for phone in self._phones[1:]:
            _unigram_plog += self.phone_dict[phone].plog()

        return _unigram_plog

    def avg_unigram_plog(self):
        return self.unigram_plog() / (len(self._phones) - 1)

    def bigram_plog(self):
        _bigram_plog = self.unigram_plog()

        for biphone in zip(*[self._phones[i:] for i in range(2)]):
            _bigram_plog -= self.biphone_dict[biphone].MI()

        return _bigram_plog

    def avg_bigram_plog(self):
        return self.bigram_plog() / (len(self._phones) - 1)


def make_word_ngrams(word_unigram_counter=None):
    uniphone_counter = Counter()
    biphone_counter = Counter()
    triphone_counter = Counter()

    for word, freq in word_unigram_counter.items():
        word = '#' + word + '#'  # add word boundaries

        uniphones = list(word)
        biphones = zip(*[uniphones[i:] for i in range(2)])
        triphones = zip(*[uniphones[i:] for i in range(3)])

        for uniphone in uniphones:
            uniphone_counter[uniphone] += freq

        for biphone in biphones:
            biphone_counter[biphone] += freq

        for triphone in triphones:
            triphone_counter[triphone] += freq

    return dict(uniphone_counter), dict(biphone_counter), dict(triphone_counter)


def make_phone_dict(phone_unigram_counter=None):
    phone_dict = dict()
    total_count = sum(phone_unigram_counter.values())

    for phone, count_ in phone_unigram_counter.items():
        freq = count_ / total_count
        phone_dict[phone] = Phone(phone, count_, freq)

    return phone_dict


def make_biphone_dict(phone_bigram_counter, phone_dict):
    biphone_dict = dict()
    total_count = sum(phone_bigram_counter.values())

    for biphone, count_ in phone_bigram_counter.items():
        freq = count_ / total_count

        phone1_spelling, phone2_spelling = biphone
        phone1 = phone_dict[phone1_spelling]
        phone2 = phone_dict[phone2_spelling]

        biphone_dict[biphone] = Biphone(phone1, phone2, count_, freq)

    return biphone_dict


def make_word_dict(word_unigram_counter, phone_dict, biphone_dict,
                   words_to_phones=None):
    word_dict = dict()
    total_count = sum(word_unigram_counter.values())

    for word, count_ in word_unigram_counter.items():
        freq = count_ / total_count

        if words_to_phones is None:
            phones = list(word)
        else:
            phones = words_to_phones[word]

        phones = ['#'] + phones + ['#']

        word_dict[word] = Word(word, phones, count_, freq,
                               phone_dict, biphone_dict)

    return word_dict
