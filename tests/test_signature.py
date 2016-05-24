# -*- encoding: utf8 -*-

import os

import linguistica as lxa
from linguistica.datasets import brown as corpus_path

data_dir = os.path.join(os.path.dirname(__file__), 'data')


def test_stems_to_signatures():
    lxa_object = lxa.read_corpus(corpus_path, max_word_tokens=50000)
    test_object = lxa_object.stems_to_signatures()

    expected_object_path = os.path.join(data_dir, 'stems_to_signatures.txt')
    expected_object = eval(open(expected_object_path).read())
    assert test_object == expected_object


def test_stems_to_words():
    lxa_object = lxa.read_corpus(corpus_path, max_word_tokens=50000)
    test_object = lxa_object.stems_to_words()

    expected_object_path = os.path.join(data_dir, 'stems_to_words.txt')
    expected_object = eval(open(expected_object_path).read())
    assert test_object == expected_object


def test_signatures_to_stems():
    lxa_object = lxa.read_corpus(corpus_path, max_word_tokens=50000)
    test_object = lxa_object.signatures_to_stems()

    expected_object_path = os.path.join(data_dir, 'signatures_to_stems.txt')
    expected_object = eval(open(expected_object_path).read())
    assert test_object == expected_object


def test_words_to_signatures():
    lxa_object = lxa.read_corpus(corpus_path, max_word_tokens=50000)
    test_object = lxa_object.words_to_signatures()

    expected_object_path = os.path.join(data_dir, 'words_to_signatures.txt')
    expected_object = eval(open(expected_object_path).read())
    assert test_object == expected_object


def test_signatures_to_words():
    lxa_object = lxa.read_corpus(corpus_path, max_word_tokens=50000)
    test_object = lxa_object.signatures_to_words()

    expected_object_path = os.path.join(data_dir, 'signatures_to_words.txt')
    expected_object = eval(open(expected_object_path).read())
    assert test_object == expected_object


def test_words_to_sigtransforms():
    lxa_object = lxa.read_corpus(corpus_path, max_word_tokens=50000)
    test_object = lxa_object.words_to_sigtransforms()

    expected_object_path = os.path.join(data_dir, 'words_to_sigtransforms.txt')
    expected_object = eval(open(expected_object_path).read())
    assert test_object == expected_object


def test_affixes_to_signatures():
    lxa_object = lxa.read_corpus(corpus_path, max_word_tokens=50000)
    test_object = lxa_object.affixes_to_signatures()

    expected_object_path = os.path.join(data_dir, 'affixes_to_signatures.txt')
    expected_object = eval(open(expected_object_path).read())
    assert test_object == expected_object


def test_signatures():
    lxa_object = lxa.read_corpus(corpus_path, max_word_tokens=50000)
    test_object = set(lxa_object.signatures())

    expected_object_path = os.path.join(data_dir, 'signatures_to_words.txt')
    expected_object = set(eval(open(expected_object_path).read()).keys())
    assert test_object == expected_object


def test_words_in_signatures():
    lxa_object = lxa.read_corpus(corpus_path, max_word_tokens=50000)
    test_object = set(lxa_object.words_in_signatures())

    expected_object_path = os.path.join(data_dir, 'words_to_signatures.txt')
    expected_object = set(eval(open(expected_object_path).read()).keys())
    assert test_object == expected_object


def test_affixes():
    lxa_object = lxa.read_corpus(corpus_path, max_word_tokens=50000)
    test_object = set(lxa_object.affixes())

    expected_object_path = os.path.join(data_dir, 'affixes_to_signatures.txt')
    expected_object = set(eval(open(expected_object_path).read()).keys())
    assert test_object == expected_object


def test_stems():
    lxa_object = lxa.read_corpus(corpus_path, max_word_tokens=50000)
    test_object = set(lxa_object.stems())

    expected_object_path = os.path.join(data_dir, 'stems_to_words.txt')
    expected_object = set(eval(open(expected_object_path).read()).keys())
    assert test_object == expected_object

