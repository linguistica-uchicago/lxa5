# -*- encoding: utf8 -*-


from collections import Counter


def plog(x):
    import math
    return -1 * math.log2(x)


class Phone:
    def __init__(self, spelling, count, freq):
        self.spelling = spelling
        self.count = count
        self.frequency = freq
        self.plog = plog(self.frequency)


# noinspection PyPep8Naming
class Biphone:
    def __init__(self, phone1, phone2, count, freq):
        self.phone1 = phone1
        self.phone2 = phone2

        self.spelling = (self.phone1.spelling, self.phone2.spelling)
        self.count = count
        self.frequency = freq
        self.MI = self.phone1.plog + self.phone2.plog - plog(self.frequency)
        self.weighted_MI = self.MI * self.count


class Word:
    def __init__(self, spelling, phones, count, freq, phone_dict, biphone_dict):
        self.spelling = spelling
        self.phones = phones
        self.count = count
        self.frequency = freq

        self.unigram_plog = sum(phone_dict[phone].plog
                                for phone in self.phones[1:])
        self.avg_unigram_plog = self.unigram_plog / (len(self.phones) - 1)

        _bigram_plog = self.unigram_plog
        for biphone in zip(*[self.phones[i:] for i in range(2)]):
            _bigram_plog -= biphone_dict[biphone].MI
        self.bigram_plog = _bigram_plog

        self.avg_bigram_plog = self.bigram_plog / (len(self.phones) - 1)


def make_word_ngrams(word_unigram_counter, words_to_phones=None):
    uniphone_counter = Counter()
    biphone_counter = Counter()
    triphone_counter = Counter()

    for word, freq in word_unigram_counter.items():
        if not words_to_phones:
            word = '#' + word + '#'  # add word boundaries
            uniphones = list(word)
        else:
            uniphones = ['#'] + words_to_phones[word] + ['#']

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

        if not words_to_phones:
            phones = list(word)
        else:
            phones = words_to_phones[word]

        phones = ['#'] + phones + ['#']

        word_dict[word] = Word(word, phones, count_, freq,
                               phone_dict, biphone_dict)

    return word_dict
