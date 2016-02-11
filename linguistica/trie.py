from linguistica.util import NULL


def find_breaks(wordlist, min_stem_length):
    prefixes_found = set()

    breaks = dict()
    for i in range(len(wordlist)):
        breaks[i] = set()

    previous_word = wordlist[0]

    for i in range(1, len(wordlist)):
        this_word = wordlist[i]
        m = common_prefix_length(previous_word, this_word)

        if m < min_stem_length:
            previous_word = this_word
            continue

        common_prefix = this_word[: m]

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


def break_words(wordlist, break_dict):
    broken_words = dict()

    for i, this_word in enumerate(wordlist):
        broken_words[this_word] = list()
        break_list = sorted(break_dict[i])

        if not break_list:
            broken_words[this_word].append(this_word)
        else:
            this_piece = ''
            for x in range(len(this_word)):
                this_piece += this_word[x]
                if x + 1 in break_list:
                    broken_words[this_word].append(this_piece)
                    this_piece = ''
            if this_piece:
                broken_words[this_word].append(this_piece)

    return broken_words


def get_successors(wordlist, broken_words):
    successors = dict()
    for i, this_word in enumerate(wordlist):
        this_word_parsed = broken_words[this_word]
        number_of_pieces = len(this_word_parsed)

        if not this_word_parsed:
            successors[this_word] = set()
            successors[this_word].add(NULL)
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

    for word_begin in successors:  # turn these into an alphabetized list
        successors[word_begin] = sorted(successors[word_begin])

    return successors


def common_prefix_length(s1, s2):
    # ensure that s1 is not longer than s2
    length = len(s1)
    if length > len(s2):
        common_prefix_length(s2, s1)

    for i in range(length):
        if s1[i] != s2[i]:
            return i
    return length


def run(wordlist=None, min_stem_length=4):
    reversed_wordlist = sorted([x[::-1] for x in wordlist])

    # --------------------------------------------------------------------------
    # Find breaks in words (left-to-right and right-to-left)

    breaks_left_to_right = find_breaks(wordlist, min_stem_length)
    breaks_right_to_left = find_breaks(reversed_wordlist, min_stem_length)

    # --------------------------------------------------------------------------
    # Break up each word (left-to-right and right-to-left)

    broken_words_left_to_right = break_words(wordlist, breaks_left_to_right)
    broken_words_right_to_left = break_words(reversed_wordlist,
                                             breaks_right_to_left)

    # --------------------------------------------------------------------------
    # Compute successors and predecessors

    successors = get_successors(wordlist, broken_words_left_to_right)
    predecessors = get_successors(reversed_wordlist, broken_words_right_to_left)

    return (broken_words_left_to_right, broken_words_right_to_left,
            successors, predecessors)
