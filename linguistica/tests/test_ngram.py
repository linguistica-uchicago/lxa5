# -*- encoding: utf8 -*-

import os

import linguistica as lxa
from linguistica.datasets import brown as corpus_path
from linguistica.datasets import cmudict as wordlist_path

data_dir = os.path.join(os.path.dirname(__file__), 'data')


def test_wordlist_from_corpus_file():
    lxa_object = lxa.read_corpus(corpus_path, max_word_tokens=50000)
    test_object = lxa_object.wordlist()

    expected_object_path = os.path.join(data_dir, 'wordlist.txt')
    expected_object = eval(open(expected_object_path).read())
    assert test_object == expected_object


def test_wordlist_from_wordlist_file():
    lxa_object = lxa.read_wordlist(wordlist_path)
    test_object = lxa_object.wordlist()

    assert type(test_object) == list  # TODO: not actually testing contents...


def test_word_unigram_counter():
    lxa_object = lxa.read_corpus(corpus_path, max_word_tokens=50000)
    test_object = lxa_object.word_unigram_counter()

    expected_object_path = os.path.join(data_dir, 'word_unigram_counter.txt')
    expected_object = eval(open(expected_object_path).read())
    assert test_object == expected_object


def test_word_bigram_counter():
    lxa_object = lxa.read_corpus(corpus_path, max_word_tokens=50000)
    test_object = lxa_object.word_bigram_counter()

    expected_object_path = os.path.join(data_dir, 'word_bigram_counter.txt')
    expected_object = eval(open(expected_object_path).read())
    assert test_object == expected_object


def test_word_trigram_counter():
    lxa_object = lxa.read_corpus(corpus_path, max_word_tokens=50000)
    test_object = lxa_object.word_trigram_counter()

    expected_object_path = os.path.join(data_dir, 'word_trigram_counter.txt')
    expected_object = eval(open(expected_object_path).read())
    assert test_object == expected_object
