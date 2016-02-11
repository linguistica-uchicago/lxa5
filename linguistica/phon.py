from collections import Counter


def run(word_unigram_counter=None):
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
