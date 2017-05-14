.. _lexicon:

Full API documentation
======================

Once a Linguistica object (such as ``lxa_object`` below with the Brown corpus)
is initialized, various methods and attributes are available for automatic
linguistic analysis:

.. code-block:: python

   >>> import linguistica as lxa
   >>> lxa_object = lxa.read_corpus('path/to/english-brown.txt')
   >>> words = lxa_object.wordlist()  # using wordlist()

Basic information
-----------------

.. currentmodule:: linguistica.lexicon.Lexicon

.. autosummary::

   number_of_word_tokens
   number_of_word_types

Word ngrams
-----------

Parameter: ``max_word_tokens``

.. currentmodule:: linguistica.lexicon.Lexicon

.. autosummary::

   wordlist
   word_unigram_counter
   word_bigram_counter
   word_trigram_counter

Morphological signatures
------------------------

Parameters: ``min_stem_length``, ``max_affix_length``, ``min_sig_count``, ``suffixing``

.. currentmodule:: linguistica.lexicon.Lexicon

.. autosummary::

   signatures
   stems
   affixes

   signatures_to_stems
   signatures_to_words
   affixes_to_signatures
   stems_to_signatures
   stems_to_words
   words_in_signatures
   words_to_signatures
   words_to_sigtransforms

Word manifolds and syntactic word neighborhood
----------------------------------------------

Parameters: ``max_word_types``, ``min_context_count``, ``n_neighbors``, ``n_eigenvectors``

.. currentmodule:: linguistica.lexicon.Lexicon

.. autosummary::

   words_to_neighbors
   neighbor_graph
   words_to_contexts
   contexts_to_words

Phonology
---------

.. currentmodule:: linguistica.lexicon.Lexicon

.. autosummary::

   phone_unigram_counter
   phone_bigram_counter
   phone_trigram_counter

Tries
-----

Parameter: ``min_stem_length``

.. currentmodule:: linguistica.lexicon.Lexicon

.. autosummary::

   broken_words_left_to_right
   broken_words_right_to_left
   successors
   predecessors

Other methods and attributes
----------------------------

.. currentmodule:: linguistica.lexicon.Lexicon

.. autosummary::

   parameters
   change_parameters
   use_default_parameters

.. automodule:: linguistica.lexicon
   :members:
