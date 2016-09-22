.. _demo:

Quick demonstration
===================

This demonstration focuses on Linguistica 5 as a Python library.
There are two other use modes: :ref:`gui` and :ref:`cli`.

For the nature and format of datasets: :ref:`data`

For more details about Linguistica 5 as a Python library: :ref:`read` and :ref:`lexicon`

The Basics
----------

-  Importing the ``linguistica`` library
-  Using a built-in dataset (the English Brown corpus)
-  Creating a Linguistica object for a given dataset

.. code:: python

    import linguistica as lxa
    from linguistica.datasets import brown
    
    lxa_object = lxa.read_corpus(brown)


``brown`` (str) is the file path of the English Brown corpus text file
built in the Linguistica 5 library. If you would like to use a corpus
text from the local drive, the argument for ``read_corpus()`` should
take the file path (as a str) of your desired text file.

Methods with a Linguistica object
---------------------------------

Sample uses: (1) word trigrams, (2) signatures to stems

(1) Word trigrams
~~~~~~~~~~~~~~~~~

.. code:: python

    trigrams = lxa_object.word_trigram_counter()
``trigrams`` is a dict with word trigrams (each as a tuple) mapped to
their respective counts.

.. code:: python

    for trigram, count_ in sorted(trigrams.items(), key=lambda x: x[1], reverse=True):
        print(trigram, count_)
        
        if count_ < 100:
            break

.. parsed-literal::

    (',', 'and', 'the') 662
    ('one', 'of', 'the') 403
    ('the', 'united', 'states') 328
    (',', 'however', ',') 321
    (',', 'in', 'the') 266
    ('.', 's', '.') 266
    (',', 'he', 'said') 257
    ('as', 'well', 'as') 238
    ('u', '.', 's') 235
    (',', 'it', 'is') 234
    (',', 'and', 'he') 225
    ('of', 'course', ',') 220
    (',', 'of', 'course') 189
    ('some', 'of', 'the') 179
    ('the', 'u', '.') 176
    ('out', 'of', 'the') 174
    ('the', 'fact', 'that') 167
    (',', 'but', 'the') 161
    (',', 'mr', '.') 159
    (',', 'and', 'a') 158
    ('for', 'example', ',') 153
    ('.', 'm', '.') 153
    ('the', 'end', 'of') 149
    (',', 'but', 'he') 148
    ('part', 'of', 'the') 144
    ('he', 'said', ',') 143
    ('it', 'was', 'a') 143
    ('there', 'was', 'a') 142
    ('it', 'is', 'not') 136
    ('to', 'be', 'a') 133
    ('there', 'was', 'no') 132
    (',', 'and', 'i') 132
    (',', 'too', ',') 131
    (',', 'it', 'was') 129
    ('there', 'is', 'a') 128
    ('of', 'the', 'united') 127
    (',', 'with', 'the') 124
    ('a', 'number', 'of') 123
    (',', 'mrs', '.') 121
    ('in', 'order', 'to') 120
    (',', 'and', 'that') 120
    (',', 'but', 'it') 120
    (',', 'and', 'in') 119
    ('it', 'is', 'a') 114
    ('most', 'of', 'the') 114
    ('members', 'of', 'the') 110
    (',', 'and', 'it') 109
    (',', 'he', 'was') 109
    ('end', 'of', 'the') 108
    ('of', 'the', 'new') 107
    ('it', 'would', 'be') 107
    (',', 'for', 'the') 106
    ('the', 'number', 'of') 104
    ('there', 'is', 'no') 104
    ('he', 'did', 'not') 103
    ('at', 'the', 'same') 103
    ('.', 'c', '.') 102
    (',', 'and', 'then') 102
    (',', 'she', 'said') 102
    ('the', 'use', 'of') 102
    ('in', 'fact', ',') 101
    ('on', 'the', 'other') 100
    ('he', 'said', '.') 100
    (',', 'on', 'the') 99



Given ``trigrams`` is a dict that maps something to counts, it is
natural to convert it to a Counter instance (via the ``collections``
module in the standard library) and take advantage of the methods
available (e.g., ``most_common(k)`` for accessible the most common k
items).

(2) Signatures to stems
~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    sigs_to_stems = lxa_object.signatures_to_stems()
.. code:: python

    for sig, stems in sorted(sigs_to_stems.items(), key=lambda x: len(x[1]), reverse=True):
        print(sig, len(stems))

        if len(stems) < 50:
            break

.. parsed-literal::

    ('NULL', 's') 2327
    ("'s", 'NULL') 813
    ('NULL', 'ly') 587
    ('NULL', 'd', 's') 346
    ('NULL', 'd') 314
    ('ed', 'ing') 197
    ("'", 'NULL') 190
    ("'s", 'NULL', 's') 181
    ('d', 's') 175
    ('ies', 'y') 173
    ('NULL', 'ed', 'ing', 's') 151
    ('NULL', 'ed') 134
    ('NULL', 'ed', 'ing') 130
    ('e', 'ed', 'es', 'ing') 130
    ('NULL', 'ing') 105
    ('d', 'r') 98
    ('e', 'y') 95
    ('e', 'ed', 'ing') 88
    ('ng', 'on') 85
    ('NULL', 'ed', 's') 82
    ('NULL', 'ly', 'ness') 74
    ("'", 'g') 72
    ('d', 'r', 'rs') 66
    ('NULL', 'es') 63
    ('NULL', 'ness') 60
    ('ng', 'on', 'ons') 57
    ('NULL', 'e') 51
    ('NULL', 'ally') 47



For all methods available to a Linguistica
objects: :ref:`lexicon`

