import os

import linguistica as lxa

data_dir = os.path.join(os.path.dirname(__file__), 'data')
corpus_path = os.path.join(data_dir, 'english-brown.txt')

lxa_object = lxa.read_corpus(corpus_path, max_word_tokens=50000)


def test_stems_to_signatures():
    test_object = lxa_object.stems_to_signatures()

    expected_object_path = os.path.join(data_dir, 'stems_to_signatures.txt')
    expected_object = eval(open(expected_object_path).read())
    assert test_object == expected_object


def test_stems_to_words():
    test_object = lxa_object.stems_to_words()

    expected_object_path = os.path.join(data_dir, 'stems_to_words.txt')
    expected_object = eval(open(expected_object_path).read())
    assert test_object == expected_object


def test_signatures_to_stems():
    test_object = lxa_object.signatures_to_stems()

    expected_object_path = os.path.join(data_dir, 'signatures_to_stems.txt')
    expected_object = eval(open(expected_object_path).read())
    assert test_object == expected_object


def test_words_to_signatures():
    test_object = lxa_object.words_to_signatures()

    expected_object_path = os.path.join(data_dir, 'words_to_signatures.txt')
    expected_object = eval(open(expected_object_path).read())
    assert test_object == expected_object


def test_signatures_to_words():
    test_object = lxa_object.signatures_to_words()

    expected_object_path = os.path.join(data_dir, 'signatures_to_words.txt')
    expected_object = eval(open(expected_object_path).read())
    assert test_object == expected_object


def test_words_to_sigtransforms():
    test_object = lxa_object.words_to_sigtransforms()

    expected_object_path = os.path.join(data_dir, 'words_to_sigtransforms.txt')
    expected_object = eval(open(expected_object_path).read())
    assert test_object == expected_object


def test_affixes_to_signatures():
    test_object = lxa_object.affixes_to_signatures()

    expected_object_path = os.path.join(data_dir, 'affixes_to_signatures.txt')
    expected_object = eval(open(expected_object_path).read())
    assert test_object == expected_object
