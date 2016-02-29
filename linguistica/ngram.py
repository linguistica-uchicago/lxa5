# -*- encoding: utf8 -*-

from collections import Counter

from linguistica.util import fix_punctuations


def run(corpus_file_object=None, keep_case=False, max_word_tokens=0):

    unigrams_counter = Counter()
    bigrams_counter = Counter()
    trigrams_counter = Counter()

    current_word_token_count = 0

    for line in corpus_file_object:
        if max_word_tokens and current_word_token_count > max_word_tokens:
            break

        line = fix_punctuations(line).strip()

        if not keep_case:
            line = line.casefold()

        words = line.split()
        if not words:
            continue

        current_word_token_count += len(words)

        unigrams_of_line = words
        bigrams_of_line = zip(*[words[i:] for i in range(2)])
        trigrams_of_line = zip(*[words[i:] for i in range(3)])

        unigrams_counter.update(unigrams_of_line)
        bigrams_counter.update(bigrams_of_line)
        trigrams_counter.update(trigrams_of_line)

    return dict(unigrams_counter), dict(bigrams_counter), dict(trigrams_counter)
