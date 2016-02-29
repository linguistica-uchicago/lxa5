# -*- encoding: utf8 -*-

import os

from nose.tools import assert_raises

from linguistica import (Lexicon,
                         read_corpus, read_wordlist, from_corpus, from_wordlist)


data_dir = os.path.join(os.path.dirname(__file__), 'data')
corpus_path = os.path.join(data_dir, 'english-brown.txt')
wordlist_path = os.path.join(data_dir, 'english.dx1')


def test_file_path_type_error():
    assert_raises(TypeError, read_corpus, 123)


def test_unfound_parameter_error():
    assert_raises(KeyError, read_corpus, corpus_path, non_existing_parameter=3)


def test_unfound_file_error():
    assert_raises(FileNotFoundError, read_corpus, 'blahblahblah')


def test_read_wordlist():
    assert isinstance(read_wordlist(wordlist_path), Lexicon)


def test_from_corpus():
    corpus_str = open(corpus_path, encoding='utf8').read()
    assert isinstance(from_corpus(corpus_str), Lexicon)


def test_from_wordlist():
    wordlist = open(wordlist_path, encoding='utf8').readlines()
    assert isinstance(from_wordlist(wordlist), Lexicon)


def test_change_parameters():
    test_object = read_corpus(corpus_path)
    assert test_object.change_parameters(min_stem_length=4) is None


def test_change_parameters_with_error():
    test_object = read_corpus(corpus_path)
    assert_raises(KeyError, test_object.change_parameters,
                  non_existing_parameter=4)


def test_reset():
    test_object = read_corpus(corpus_path)
    assert test_object.reset() is None

