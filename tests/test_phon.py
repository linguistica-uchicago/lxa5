# -*- encoding: utf8 -*-

import os

import pytest

import linguistica as lxa
from linguistica.datasets import brown as corpus_path

data_dir = os.path.join(os.path.dirname(__file__), 'data')


def test_phone_unigram_counter():
    lxa_object = lxa.read_corpus(corpus_path, max_word_tokens=50000)
    test_object = lxa_object.phone_unigram_counter()

    expected_object_path = os.path.join(data_dir, 'phone_unigram_counter.txt')
    expected_object = eval(open(expected_object_path).read())
    assert test_object == expected_object


def test_phone_bigram_counter():
    lxa_object = lxa.read_corpus(corpus_path, max_word_tokens=50000)
    test_object = lxa_object.phone_bigram_counter()

    expected_object_path = os.path.join(data_dir, 'phone_bigram_counter.txt')
    expected_object = eval(open(expected_object_path).read())
    assert test_object == expected_object


def test_phone_trigram_counter():
    lxa_object = lxa.read_corpus(corpus_path, max_word_tokens=50000)
    test_object = lxa_object.phone_trigram_counter()

    expected_object_path = os.path.join(data_dir, 'phone_trigram_counter.txt')
    expected_object = eval(open(expected_object_path).read())
    assert test_object == expected_object


def test_plog():
    from linguistica.phon import plog
    assert plog(1) == 0
    assert plog(2) == -1.0
    assert plog(0.5) == 1.0
    assert plog(0.25) == 2.0
    with pytest.raises(ValueError):
        plog(0)


def test_phone_dict():
    lxa_object = lxa.read_corpus(corpus_path, max_word_tokens=50000)
    _ = lxa_object.phone_dict()
    assert True  # TODO: only testing if there are errors for now...


def test_biphone_dict():
    lxa_object = lxa.read_corpus(corpus_path, max_word_tokens=50000)
    _ = lxa_object.biphone_dict()
    assert True  # TODO: only testing if there are errors for now...


def test_word_phonology_dict():
    lxa_object = lxa.read_corpus(corpus_path, max_word_tokens=50000)
    _ = lxa_object.word_phonology_dict()
    assert True  # TODO: only testing if there are errors for now...
