import os

import linguistica as lxa

data_dir = os.path.join(os.path.dirname(__file__), 'data')
corpus_path = os.path.join(data_dir, 'english-brown.txt')

lxa_object = lxa.read_corpus(corpus_path, max_word_tokens=50000)


def test_phone_unigram_counter():
    test_object = lxa_object.phone_unigram_counter()

    expected_object_path = os.path.join(data_dir, 'phone_unigram_counter.txt')
    expected_object = eval(open(expected_object_path).read())
    assert test_object == expected_object


def test_phone_bigram_counter():
    test_object = lxa_object.phone_bigram_counter()

    expected_object_path = os.path.join(data_dir, 'phone_bigram_counter.txt')
    expected_object = eval(open(expected_object_path).read())
    assert test_object == expected_object


def test_phone_trigram_counter():
    test_object = lxa_object.phone_trigram_counter()

    expected_object_path = os.path.join(data_dir, 'phone_trigram_counter.txt')
    expected_object = eval(open(expected_object_path).read())
    assert test_object == expected_object
