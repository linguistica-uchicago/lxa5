from __future__ import annotations

from typing import TypedDict

# ------------------------------------------------------------------------------
# parameters, with the "factory settings"

# What programs use what parameters:
#
# ngram:     max_word_tokens
# signature: min_stem_length, max_affix_length, min_sig_count
# phon:      (no parameters so far)
# trie:      min_stem_length, min_affix_length, min_sf_pf_count
# manifold:  max_word_types, n_neighbors, n_eigenvectors, min_context_count
# (See the individual programs for what these parameters mean.)

PARAMETERS: dict[str, int] = {
    "max_word_tokens": 0,  # zero means all word tokens
    "min_stem_length": 4,
    "max_affix_length": 4,
    "min_sig_count": 5,
    # 'min_affix_length': 1,
    # 'min_sf_pf_count': 3,
    "n_neighbors": 9,
    "n_eigenvectors": 11,
    "min_context_count": 3,
    "max_word_types": 1000,
    "suffixing": 1,  # 1 means yes, 0 means no
    "keep_case": 0,  # 1 means yes, 0 means no
}

PARAMETERS_RANGES: dict[str, tuple[int, int]] = {
    "max_word_tokens": (0, 1_000_000_000),
    "min_stem_length": (1, 10),
    "max_affix_length": (1, 10),
    "min_sig_count": (5, 50),
    "n_neighbors": (5, 20),
    "n_eigenvectors": (5, 20),
    "min_context_count": (1, 10),
    "max_word_types": (0, 1_000_000_000),
    "suffixing": (0, 1),  # 1 means yes, 0 means no
    "keep_case": (0, 1),  # 1 means yes, 0 means no
}

PARAMETERS_HINTS: dict[str, str] = {
    "max_word_tokens": "0 = all word tokens",
    "min_stem_length": "",
    "max_affix_length": "",
    "min_sig_count": "",
    "n_neighbors": "",
    "n_eigenvectors": "",
    "min_context_count": "",
    "max_word_types": "",
    "suffixing": "1 = yes; 0 = no",
    "keep_case": "1 = yes; 0 = no",
}


class ParametersKwargs(TypedDict, total=False):
    """Accepted keyword parameters for the ``Lexicon`` constructors and
    ``change_parameters()``.

    The keys mirror :data:`PARAMETERS` exactly; ``total=False`` marks them all
    optional. Both this TypedDict and ``PARAMETERS`` are frozen (no more
    Linguistica 5 feature work) and must stay in sync.
    """

    max_word_tokens: int
    min_stem_length: int
    max_affix_length: int
    min_sig_count: int
    n_neighbors: int
    n_eigenvectors: int
    min_context_count: int
    max_word_types: int
    suffixing: int
    keep_case: int
