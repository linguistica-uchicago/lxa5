.. _cli:

Command line interface (CLI)
============================

To launch the Linguistica CLI:

.. code-block:: bash

    $ python3 -m linguistica cli

The command line interface works for either a corpus text file or a wordlist
file. Parameter changes are supported. Results are saved as text files.

A sample CLI session,
with a corpus text file as input and default settings for all parameters and
options::

    $ python3 -m linguistica cli

    ================================================================
    Welcome to Linguistica 5.1.0-dev!
    ================================================================

    Are you using a wordlist file? [N/y] n
    --------------------------------------------

    Path to your file: path/to/english-brown.txt

    Full file path:
    path/to/english-brown.txt
    --------------------------------------------

    Default output directory:
    path/to/lxa_outputs
    Change it? [N/y] n
    --------------------------------------------

    Default encoding for input and output files: utf8
    Change encoding? [N/y] n
    --------------------------------------------

    Parameters:
    {'keep_case': 0,
     'max_affix_length': 4,
     'max_word_tokens': 0,
     'max_word_types': 1000,
     'min_context_count': 3,
     'min_sig_count': 5,
     'min_stem_length': 4,
     'n_eigenvectors': 11,
     'n_neighbors': 9,
     'suffixing': 1}

    Change any parameters? [N/y] n
    --------------------------------------------

    Running all Linguistica modules on the given file:
    Extracting word ngrams...
    Phonology...
    Morphological signatures...
    Tries...
    Syntactic word neighbors...
    --------------------------------------------

    Generating output files...

    ngram objects
        word_bigrams.txt
        word_trigrams.txt
    morphological signature objects
        stems_to_words.txt
        stems_to_words.txt
        signatures_to_stems.txt
        signatures_to_stems_truncated.txt
        stems_to_signatures.txt
        words_to_signatures.txt
        signatures_to_words.txt
        signatures_to_words_truncated.txt
        words_to_sigtransforms.txt
        affixes_to_signatures.txt
    manifold objects
        words_to_neighbors.txt
    phon objects
        wordlist.txt
        wordlist_by_avg_unigram_plog.txt
        wordlist_by_avg_bigram_plog.txt
        phones.txt
        biphones.txt
        triphones.txt
    trie objects
        words_as_tries.txt
        successors.txt
        predecessors.txt

    Results are in path/to/lxa_outputs


