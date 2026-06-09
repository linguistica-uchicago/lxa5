from __future__ import annotations

from collections import Counter
from typing import Iterable

from linguistica.util import Bigram, Trigram, fix_punctuations


def run(
    corpus_file_object: Iterable[str],
    keep_case: bool = False,
    max_word_tokens: int = 0,
) -> tuple[dict[str, int], dict[Bigram, int], dict[Trigram, int]]:

    unigrams_counter: Counter[str] = Counter()
    bigrams_counter: Counter[Bigram] = Counter()
    trigrams_counter: Counter[Trigram] = Counter()

    current_word_token_count = 0

    for line in corpus_file_object:
        if max_word_tokens and current_word_token_count > max_word_tokens:
            break

        line = fix_punctuations(line).strip()

        if not keep_case:
            line = line.lower()

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

    return (dict(unigrams_counter), dict(bigrams_counter), dict(trigrams_counter))
