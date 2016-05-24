# -*- encoding: utf8 -*-

import os

import linguistica as lxa
from linguistica.datasets import brown as corpus_path

data_dir = os.path.join(os.path.dirname(__file__), 'data')


def test_broken_words_left_to_right():
    lxa_object = lxa.read_corpus(corpus_path, max_word_tokens=50000)
    test_object = lxa_object.broken_words_left_to_right()

    expected_object_path = os.path.join(data_dir,
                                        'broken_words_left_to_right.txt')
    expected_object = eval(open(expected_object_path).read())
    assert test_object == expected_object


def test_broken_words_right_to_left():
    lxa_object = lxa.read_corpus(corpus_path, max_word_tokens=50000)
    test_object = lxa_object.broken_words_right_to_left()

    expected_object_path = os.path.join(data_dir,
                                        'broken_words_right_to_left.txt')
    expected_object = eval(open(expected_object_path).read())
    assert test_object == expected_object


def test_successors():
    lxa_object = lxa.read_corpus(corpus_path, max_word_tokens=50000)
    test_object = lxa_object.successors()

    expected_object_path = os.path.join(data_dir, 'successors.txt')
    expected_object = eval(open(expected_object_path).read())
    assert test_object == expected_object


def test_predecessors():
    lxa_object = lxa.read_corpus(corpus_path, max_word_tokens=50000)
    test_object = lxa_object.predecessors()

    expected_object_path = os.path.join(data_dir, 'predecessors.txt')
    expected_object = eval(open(expected_object_path).read())
    assert test_object == expected_object

