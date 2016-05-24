# -*- encoding: utf8 -*-

import os
import networkx as nx

import linguistica as lxa
from linguistica.datasets import brown as corpus_path

data_dir = os.path.join(os.path.dirname(__file__), 'data')


def test_words_to_neighbors():
    lxa_object = lxa.read_corpus(corpus_path, max_word_tokens=50000)
    number_of_neighbors = lxa_object.parameters()['n_neighbors']
    test_object = lxa_object.words_to_neighbors()
    number_of_words = len(test_object)
    correct_count = 0

    expected_object_path = os.path.join(data_dir, 'words_to_neighbors.txt')
    expected_object = eval(open(expected_object_path).read())

    # test if each word has a similar set of neighbor words
    # across test_object and expected_object

    for word in test_object.keys():
        word_set1 = set(test_object[word])
        word_set2 = set(expected_object[word])
        if len(word_set1 & word_set2) >= (number_of_neighbors - 4):
            correct_count += 1

    correct_ratio = correct_count / number_of_words

    # test if the ratio of words having a similar set of neighbor words is
    # high enough to pass the test

    assert correct_ratio >= 0.5


def test_words_to_contexts():
    lxa_object = lxa.read_corpus(corpus_path, max_word_tokens=50000)
    test_object = lxa_object.words_to_contexts()

    expected_object_path = os.path.join(data_dir, 'words_to_contexts.txt')
    expected_object = eval(open(expected_object_path).read())
    assert test_object == expected_object


def test_contexts_to_words():
    lxa_object = lxa.read_corpus(corpus_path, max_word_tokens=50000)
    test_object = lxa_object.contexts_to_words()

    expected_object_path = os.path.join(data_dir, 'contexts_to_words.txt')
    expected_object = eval(open(expected_object_path).read())
    assert test_object == expected_object


def test_neighbor_graph():
    lxa_object = lxa.read_corpus(corpus_path, max_word_tokens=50000)
    test_object = lxa_object.neighbor_graph()

    expected_object = nx.Graph()
    words_to_neighbors_path = os.path.join(data_dir, 'words_to_neighbors.txt')
    words_to_neighbors = eval(open(words_to_neighbors_path).read())

    for word in words_to_neighbors:
        neighbors = words_to_neighbors[word]

        for neighbor in neighbors:
            expected_object.add_edge(word, neighbor)

    test_edges = set(test_object.edges())
    expected_edges = set(expected_object.edges())

    number_of_hits = 0

    for test_edge in test_edges:
        if test_edge in expected_edges:
            number_of_hits += 1

    hit_ratio = number_of_hits / len(expected_edges)

    assert hit_ratio > 0.5
