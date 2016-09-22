.. _data:

Data
====

As the goal of Linguistica 5 is to perform automatic linguistic
analysis for some given data, it is important to understand what data
Linguistica 5 can handle.

Two types of data are recognized:

* raw corpus text
* wordlist

If you use Linguistica 5 via the :ref:`gui` or the :ref:`cli`, then your
data is a file on your local drive. However, if you use it as a Python library
instead, your data can either be a file from the local drive or an in-memory
Python object.

.. _rawtext:

Raw corpus text
---------------

A raw corpus text is simply a plain text file.
An example is the English Brown corpus (Kučera and Francis 1967) with
about one million word tokens (for about 50,000 word types) available
`here <https://github.com/linguistica-uchicago/lxa5/blob/master/linguistica/datasets/english-brown.txt>`_.
This corpus is a built-in dataset that comes with Linguistica 5 --
its file path is accessible as ``brown`` as follows:

.. code:: python

    import linguistica as lxa
    from linguistica.datasets import brown

    lxa_object = lxa.read_corpus(brown)

In lieu of ``brown``, you may pass the file path as argument to
``read_corpus()`` for your raw corpus text.
As long as your corpus is
one single text file encoded in Unicode UTF-8,
Linguistica 5 can handle it.

Alternatively, if you use Linguistica 5 as a Python library in your own
Python programs and would like to use an in-memory object as corpus data,
the function ``from_corpus()`` (see :ref:`source`) is probably what
you need.


.. _wordlist:

Wordlist
--------

A wordlist file is a plain text file in a specific format (more below)
that Linguistica 5 recognizes as a wordlist.
The Linguistica team has conventionally called this format ``.dx1``
(think: a dictionary file; that's "one" but not "L" at the end)
which is also the file extension name.
An example of a ``.dx1`` file is ``english-cmudict.dx1`` available
`here <https://github.com/linguistica-uchicago/lxa5/blob/master/linguistica/datasets/english-cmudict.dx1>`_.
(This file is essentially the
`CMU Pronouncing Dictionary <http://www.speech.cs.cmu.edu/cgi-bin/cmudict>`_
with English words represented phonemically by Arpabet,
with the addition of word token counts---if available---based on the English
Brown corpus.) This wordlist is also a built-in dataset:

.. code:: python

    import linguistica as lxa
    from linguistica.datasets import cmudict

    lxa_object = lxa.read_wordlist(cmudict)

``cmudict`` is the file path for the built-in ``english-cmudict.dx1``.
It can be replaced with the file path of a wordlist from your local drive.

As for the format of a wordlist file,
each line of the file contains three pieces of information for a
unique word type:

1. **The word itself**

   By default, case does not matter, as Linguistica 5 internally
   processes all words in lowercase.

2. **Token count of the word type**

   This is based on some corpus data. If unavailable, put down 1 here.

3. **Phonemic representation** (optional)

   A list of phonemes/phones (separated by spaces)
   for the pronunciation of the word.
   If unavailable, the word itself with its list of letters is taken to be
   phonemic representation.

To illustrate what the required format looks like, here are a few lines
from ``english-cmudict.dx1``::

   ABANDON 18 AH0 B AE1 N D AH0 N
   ABANDONED 26 AH0 B AE1 N D AH0 N D
   ABANDONING 8 AH0 B AE1 N D AH0 N IH0 NG

If phonemic representations were not available,
these lines would be as follows::

   ABANDON 18
   ABANDONED 26
   ABANDONING 8

Blank lines as well as those that begin with ``#`` (for comments, metadata etc)
are ignored by Linguistica 5.

To use Linguistica 5 as a Python library with an in-memory wordlist object,
the relevant function is ``from_wordlist()`` (see :ref:`source`).
