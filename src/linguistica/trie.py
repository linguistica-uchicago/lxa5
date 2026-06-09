from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Callable, cast

from linguistica.util import NULL


def find_breaks(wordlist: list[str], min_stem_length: int) -> dict[int, set[int]]:
    prefixes_found: set[str] = set()

    breaks: dict[int, set[int]] = dict()
    for i in range(len(wordlist)):
        breaks[i] = set()

    previous_word = wordlist[0]

    for i in range(1, len(wordlist)):
        this_word = wordlist[i]
        m = common_prefix_length(previous_word, this_word)

        if m < min_stem_length:
            previous_word = this_word
            continue

        common_prefix = this_word[:m]

        if common_prefix in prefixes_found:
            previous_word = this_word
            continue

        for j in range(i - 1, -1, -1):
            if wordlist[j].startswith(common_prefix):
                breaks[j].add(m)
            else:
                break
        for j in range(i, len(wordlist)):
            if wordlist[j].startswith(common_prefix):
                breaks[j].add(m)
            else:
                break

        prefixes_found.add(common_prefix)
        previous_word = this_word

    return breaks


def break_words(
    wordlist: list[str], break_dict: dict[int, set[int]]
) -> dict[str, list[str]]:
    broken_words: dict[str, list[str]] = dict()

    for i, this_word in enumerate(wordlist):
        broken_words[this_word] = list()
        break_list = sorted(break_dict[i])

        if not break_list:
            broken_words[this_word].append(this_word)
        else:
            this_piece = ""
            for x in range(len(this_word)):
                this_piece += this_word[x]
                if x + 1 in break_list:
                    broken_words[this_word].append(this_piece)
                    this_piece = ""
            if this_piece:
                broken_words[this_word].append(this_piece)

    return broken_words


def get_successors(
    wordlist: list[str], broken_words: dict[str, list[str]]
) -> dict[str, set[str]]:
    successors: dict[str, set[str]] = dict()
    for this_word in wordlist:
        this_word_parsed = broken_words[this_word]

        number_of_pieces = len(this_word_parsed)

        if not this_word_parsed:
            successors[this_word] = {NULL}
            continue
        word_being_built = this_word_parsed[0]

        if word_being_built not in successors:
            successors[word_being_built] = set()

        for j in range(1, number_of_pieces):
            new_piece = this_word_parsed[j]
            if word_being_built not in successors:
                successors[word_being_built] = set()
            successors[word_being_built].add(new_piece)
            word_being_built += new_piece

        if word_being_built not in successors:  # whole word, now
            successors[word_being_built] = set()

        successors[word_being_built].add(NULL)

    return successors


def common_prefix_length(s1: str, s2: str) -> int:
    # ensure that s1 is not longer than s2
    length = len(s1)
    if length > len(s2):
        return common_prefix_length(s2, s1)

    for i in range(length):
        if s1[i] != s2[i]:
            return i
    return length


# noinspection PyPep8
def reverse_direction(
    str_to_sequences_of_strings: Mapping[str, set[str] | list[str]],
    is_list: bool = False,
) -> dict[str, set[str] | list[str]]:
    output_dict: dict[str, set[str] | list[str]] = dict()
    for s, sequence_of_strings in str_to_sequences_of_strings.items():
        new_sequence: Any
        grow: Callable[[Any, str], Any]
        if type(sequence_of_strings) is set:
            new_sequence = set()
            grow = lambda sequence_, new_item: sequence_.add(new_item)  # noqa
        else:  # sequences_of_strings is a list
            new_sequence = list()
            grow = lambda sequence_, new_item: sequence_.append(new_item)  # noqa

        for item in sequence_of_strings:
            if item != NULL:
                item = item[::-1]

            grow(new_sequence, item)

        if is_list:
            new_sequence = new_sequence[::-1]

        if s != NULL:
            s = s[::-1]

        output_dict[s] = new_sequence

    return output_dict


def run(wordlist: list[str], min_stem_length: int = 4) -> tuple[
    dict[str, list[str]],
    dict[str, list[str]],
    dict[str, set[str]],
    dict[str, set[str]],
]:
    reversed_wordlist = sorted([x[::-1] for x in wordlist])

    # --------------------------------------------------------------------------
    # Find breaks in words (left-to-right and right-to-left)

    breaks_left_to_right = find_breaks(wordlist, min_stem_length)
    breaks_right_to_left = find_breaks(reversed_wordlist, min_stem_length)

    # --------------------------------------------------------------------------
    # Break up each word (left-to-right and right-to-left)

    broken_words_left_to_right = break_words(wordlist, breaks_left_to_right)
    broken_words_right_to_left = break_words(reversed_wordlist, breaks_right_to_left)

    # --------------------------------------------------------------------------
    # Compute successors and predecessors

    successors = get_successors(wordlist, broken_words_left_to_right)
    predecessors = get_successors(reversed_wordlist, broken_words_right_to_left)

    # --------------------------------------------------------------------------
    # Reverse direction to right-to-left

    broken_words_right_to_left = cast(
        "dict[str, list[str]]",
        reverse_direction(broken_words_right_to_left, is_list=True),
    )
    predecessors = cast("dict[str, set[str]]", reverse_direction(predecessors))

    return (
        broken_words_left_to_right,
        broken_words_right_to_left,
        successors,
        predecessors,
    )
