import os

import linguistica as lxa

data_dir = os.path.join(os.path.dirname(__file__), 'data')
corpus_path = os.path.join(data_dir, 'english-brown.txt')

lxa_object = lxa.read_corpus(corpus_path, max_word_tokens=50000)


def test_words_to_neighbors():
    number_of_neighbors = lxa_object.parameters()['n_neighbors']
    test_object = lxa_object.words_to_neighbors()
    number_of_words = len(test_object)
    correct_count = 0

    expected_object_path = os.path.join(data_dir, 'words_to_neighbors.txt')
    expected_object = eval(open(expected_object_path).read())

    # test if each word has a similar set of neighbor words
    # across test_object and expected_object

    for word in test_object.keys():
        word_set1 = set(test_object[word])
        word_set2 = set(expected_object[word])
        if len(word_set1 & word_set2) >= (number_of_neighbors - 4):
            correct_count += 1

    correct_ratio = correct_count / number_of_words

    # test if the ratio of words having a similar set of neighbor words is
    # high enough to pass the test

    assert correct_ratio >= 0.65


def test_words_to_contexts():
    test_object = lxa_object.words_to_contexts()

    expected_object_path = os.path.join(data_dir, 'words_to_contexts.txt')
    expected_object = eval(open(expected_object_path).read())
    assert test_object == expected_object


def test_contexts_to_words():
    test_object = lxa_object.contexts_to_words()

    expected_object_path = os.path.join(data_dir, 'contexts_to_words.txt')
    expected_object = eval(open(expected_object_path).read())
    assert test_object == expected_object
