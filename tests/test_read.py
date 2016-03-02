# -*- encoding: utf8 -*-

import os

from nose.tools import assert_raises

import linguistica as lxa
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


def test_run_all_modules():
    lxa_object = lxa.read_corpus(corpus_path, max_word_tokens=50000)
    lxa_object.run_all_modules()
    assert True  # test if there are errors


def test_run_ngram_module():
    lxa_object = lxa.read_corpus(corpus_path, max_word_tokens=50000)
    lxa_object.run_ngram_module()
    assert True  # test if there are errors


def test_run_signature_module():
    lxa_object = lxa.read_corpus(corpus_path, max_word_tokens=50000)
    lxa_object.run_signature_module()
    assert True  # test if there are errors


def test_run_phon_module():
    lxa_object = lxa.read_corpus(corpus_path, max_word_tokens=50000)
    lxa_object.run_phon_module()
    assert True  # test if there are errors


def test_run_trie_module():
    lxa_object = lxa.read_corpus(corpus_path, max_word_tokens=50000)
    lxa_object.run_trie_module()
    assert True  # test if there are errors


def test_run_manifold_module():
    lxa_object = lxa.read_corpus(corpus_path, max_word_tokens=50000)
    lxa_object.run_manifold_module()
    assert True  # test if there are errors


def test_output_all_results():
    lxa_object = lxa.read_corpus(corpus_path, max_word_tokens=50000)
    lxa_object.run_all_modules()
    lxa_object.output_all_results(test=True)
    assert True  # test if there are errors
