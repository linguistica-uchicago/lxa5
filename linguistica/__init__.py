# -*- encoding: utf-8 -*-

import os

from linguistica.lexicon import Lexicon
from linguistica.util import (ENCODING, CONFIG_FILENAME)

# Version
version_filename = os.path.join(os.path.dirname(__file__), 'VERSION')
try:
    with open(version_filename) as f:
        __version__ = f.read().strip()
except FileNotFoundError:
    __version__ = 'unknown version; VERSION file not found'


def create_lexicon(file_path, wordlist=False, encoding=ENCODING,
                   configfile=CONFIG_FILENAME, keep_case=False,
                   **kwargs):
    """
    Create the Linguistica lexicon object.

    :param file_path: path of input data file
    :param wordlist: whether *file_path* points to a wordlist rather than
        a corpus text. Default: ``False``
    :param encoding: encoding of the file at *file_path*. Default: ``'utf8'``
    :param configfile: configuration filename. Default: ``config.json``
    :param keep_case: whether to keep case distinction (e.g., "the" vs "The").
        Default: ``False``
    :param kwargs: keyword arguments for configuration parameters.
    """
    return Lexicon(file_path, wordlist=wordlist, encoding=encoding,
                   configfile=configfile,
                   keep_case=keep_case, **kwargs)
