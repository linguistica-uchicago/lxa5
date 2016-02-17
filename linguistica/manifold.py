# -*- encoding: utf8 -*-

from collections import defaultdict

from scipy import (sparse, spatial)
from scipy.sparse import linalg
import numpy as np
import networkx as nx

from linguistica.util import double_sorted


def get_array(wordlist, bigram_to_freq, trigram_to_freq,
              min_context_count):
    worddict = {word: wordlist.index(word) for word in wordlist}

    # convert the bigram and trigram counter dicts into list and sort them
    # throw away bi/trigrams whose frequency is below min_context_count

    bigram_to_freq_sorted = [(bigram, freq) for bigram, freq in
                             double_sorted(bigram_to_freq.items(),
                                           key=lambda x: x[1],
                                           reverse=True) if
                             freq >= min_context_count]

    trigram_to_freq_sorted = [(trigram, freq) for trigram, freq in
                              double_sorted(trigram_to_freq.items(),
                                            key=lambda x: x[1],
                                            reverse=True) if
                              freq >= min_context_count]

    # This is necessary so we can reference variables from inner functions
    class Namespace:
        pass

    ns = Namespace()
    ns.n_contexts = 0

    # We use "n_contexts" to keep track of how many unique contexts there are.
    # Conveniently, n_contexts also serves to provide a unique context
    # index whenever the program encounters a new context. The dummy class
    # Namespace is to make it possible that we can refer to and update
    # n_contexts within inner functions
    # (both "contexts_increment" and "add_word")
    # inside this "GetContextArray" function.

    def contexts_increment():
        tmp = ns.n_contexts
        ns.n_contexts += 1
        return tmp

    contextdict = defaultdict(contexts_increment)
    # key: context (e.g., tuple ('of', '_', 'cat') as a 3-gram context for 'the'
    # value: context index (int)
    # This dict is analogous to worddict, where each key is a word (str)
    # and each value is a word index (int).

    # entries for sparse matrix
    rows = []  # row numbers are word indices
    cols = []  # column numbers are context indices
    values = []

    words_to_contexts = dict()
    contexts_to_words = dict()

    for word in worddict.keys():
        words_to_contexts[word] = dict()

    def add_word(current_word, current_context, occurrence_count):
        word_no = worddict[current_word]
        context_no = contextdict[current_context]
        rows.append(word_no)
        cols.append(context_no)

        # if we use 1, we assume "type" counts.
        # What if we use occurrence_count (--> "token" counts)?
        values.append(1)

        # update words_to_contexts and contexts_to_words
        if current_context not in words_to_contexts[current_word]:
            words_to_contexts[current_word][current_context] = 0

        if current_context not in contexts_to_words:
            contexts_to_words[current_context] = dict()
        if current_word not in contexts_to_words[current_context]:
            contexts_to_words[current_context][current_word] = 0

        words_to_contexts[current_word][current_context] += occurrence_count
        contexts_to_words[current_context][current_word] += occurrence_count

    for trigram, freq in trigram_to_freq_sorted:
        word1, word2, word3 = trigram

        context1 = ('_', word2, word3)
        context2 = (word1, '_', word3)
        context3 = (word1, word2, '_')

        if word1 in words_to_contexts:
            add_word(word1, context1, freq)
        if word2 in words_to_contexts:
            add_word(word2, context2, freq)
        if word3 in words_to_contexts:
            add_word(word3, context3, freq)

    for bigram, freq in bigram_to_freq_sorted:
        word1, word2 = bigram

        context1 = ('_', word2)
        context2 = (word1, '_')

        if word1 in words_to_contexts:
            add_word(word1, context1, freq)
        if word2 in words_to_contexts:
            add_word(word2, context2, freq)

    # csr_matrix in scipy.sparse means compressed matrix
    context_array = sparse.csr_matrix((values, (rows, cols)),
                                      shape=(len(worddict), ns.n_contexts + 1),
                                      dtype=np.int64)

    return context_array, words_to_contexts, contexts_to_words


def normalize(n_words, shared_context_matrix):
    arr = np.ones(n_words, dtype=np.int64)
    for word_no in range(n_words):
        arr[word_no] = np.sum(shared_context_matrix[word_no]) - \
                       shared_context_matrix[word_no, word_no]
    return arr


def compute_incidence_graph(n_words, diameter, shared_context_matrix):
    incidence_graph = np.asarray(shared_context_matrix, dtype=np.int64)
    for word_no in range(n_words):
        incidence_graph[word_no, word_no] = diameter[word_no]
    return incidence_graph


def compute_laplacian(diameter, incidence_graph):
    d = np.sqrt(np.outer(diameter, diameter))
    # we want to NOT have div-by-zero errors,
    # but if d[i,j] = 0 then incidence_graph[i,j] = 0 too.
    d[d == 0] = 1

    # broadcasts the multiplication, so A[i,j] = B[i,j] * C[i, j]
    laplacian = (1 / d) * incidence_graph
    return laplacian


def compute_eigenvectors(laplacian):
    # csr_matrix in scipy means compressed matrix
    laplacian_sparse = sparse.csr_matrix(laplacian)

    # linalg is the linear algebra module in scipy.sparse
    # eigs takes a matrix and
    # returns (array of eigenvalues, array of eigenvectors)
    return linalg.eigs(laplacian_sparse)


def compute_words_distance(coordinates):
    # the scipy pdist function is to compute pairwise distances
    return spatial.distance.squareform(
        spatial.distance.pdist(coordinates, 'euclidean'))


def compute_closest_neighbors(word_distances, n_neighbors):
    sorted_neighbors = word_distances.argsort()
    # indices of sorted rows, low to high

    # truncate columns at n_neighbors + 1
    nearest_neighbors = sorted_neighbors[:, :n_neighbors + 1]
    return nearest_neighbors


def compute_graph(words_to_neighbors):
    graph = nx.Graph()
    for word in words_to_neighbors.keys():
        neighbors = words_to_neighbors[word]
        for neighbor in neighbors:
            graph.add_edge(word, neighbor)
    return graph


def run(unigram_counter=None, bigram_counter=None, trigram_counter=None,
        max_word_types=1000, n_neighbors=9, n_eigenvectors=11,
        min_context_count=3):

    word_freq_pairs = double_sorted(unigram_counter.items(),
                                    key=lambda x: x[1], reverse=True)

    if len(word_freq_pairs) > max_word_types:
        wordlist = [word for word, _ in word_freq_pairs[: max_word_types]]
    else:
        wordlist = [word for word, _ in word_freq_pairs]

    n_words = len(wordlist)

    # computing the context array
    # also words_to_contexts and contexts_to_words dicts
    context_array, words_to_contexts, contexts_to_words = get_array(
        wordlist, bigram_counter, trigram_counter, min_context_count)

    # computing shared context master matrix
    shared_context_matrix = context_array.dot(context_array.T).todense()
    del context_array

    # computing diameter
    diameter = normalize(n_words, shared_context_matrix)

    # computing incidence graph
    incidence_graph = compute_incidence_graph(n_words, diameter,
                                              shared_context_matrix)
    del shared_context_matrix

    # computing laplacian matrix
    laplacian_matrix = compute_laplacian(diameter, incidence_graph)
    del diameter
    del incidence_graph

    # computing eigenvectors and eigenvalues
    eigenvalues, eigenvectors = compute_eigenvectors(laplacian_matrix)
    del laplacian_matrix

    # computing distances between words
    # take first N columns of eigenvector matrix
    coordinates = eigenvectors[:, : n_eigenvectors]
    word_distances = compute_words_distance(coordinates)
    del coordinates
    del eigenvalues

    # computing nearest neighbors now
    nearest_neighbors = compute_closest_neighbors(word_distances, n_neighbors)

    words_to_neighbors = dict()

    for i in range(len(wordlist)):
        line = nearest_neighbors[i]
        word_idx, neighbors_idx = line[0], line[1:]
        word = wordlist[word_idx]
        neighbors = [wordlist[idx] for idx in neighbors_idx]
        words_to_neighbors[word] = neighbors

    return words_to_neighbors, words_to_contexts, contexts_to_words
