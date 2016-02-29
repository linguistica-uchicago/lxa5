# -*- encoding: utf8 -*-

import os

import linguistica as lxa

data_dir = os.path.join(os.path.dirname(__file__), 'data')
corpus_path = os.path.join(data_dir, 'english-brown.txt')

lxa_object = lxa.read_corpus(corpus_path, max_word_tokens=50000)


def test_broken_words_left_to_right():
    test_object = lxa_object.broken_words_left_to_right()

    expected_object_path = os.path.join(data_dir,
                                        'broken_words_left_to_right.txt')
    expected_object = eval(open(expected_object_path).read())
    assert test_object == expected_object


def test_broken_words_right_to_left():
    test_object = lxa_object.broken_words_right_to_left()

    expected_object_path = os.path.join(data_dir,
                                        'broken_words_right_to_left.txt')
    expected_object = eval(open(expected_object_path).read())
    assert test_object == expected_object


def test_successors():
    test_object = lxa_object.successors()

    expected_object_path = os.path.join(data_dir, 'successors.txt')
    expected_object = eval(open(expected_object_path).read())
    assert test_object == expected_object


def test_predecessors():
    test_object = lxa_object.predecessors()

    expected_object_path = os.path.join(data_dir, 'predecessors.txt')
    expected_object = eval(open(expected_object_path).read())
    assert test_object == expected_object

