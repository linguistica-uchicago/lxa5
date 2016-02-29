# -*- encoding: utf8 -*-

import os

import linguistica as lxa

data_dir = os.path.join(os.path.dirname(__file__), 'data')
corpus_path = os.path.join(data_dir, 'english-brown.txt')

lxa_object = lxa.read_corpus(corpus_path, max_word_tokens=50000)


def test_wordlist():
    test_object = lxa_object.wordlist()

    expected_object_path = os.path.join(data_dir, 'wordlist.txt')
    expected_object = eval(open(expected_object_path).read())
    assert test_object == expected_object


def test_word_unigram_counter():
    test_object = lxa_object.word_unigram_counter()

    expected_object_path = os.path.join(data_dir, 'word_unigram_counter.txt')
    expected_object = eval(open(expected_object_path).read())
    assert test_object == expected_object


def test_word_bigram_counter():
    test_object = lxa_object.word_bigram_counter()

    expected_object_path = os.path.join(data_dir, 'word_bigram_counter.txt')
    expected_object = eval(open(expected_object_path).read())
    assert test_object == expected_object


def test_word_trigram_counter():
    test_object = lxa_object.word_trigram_counter()

    expected_object_path = os.path.join(data_dir, 'word_trigram_counter.txt')
    expected_object = eval(open(expected_object_path).read())
    assert test_object == expected_object
