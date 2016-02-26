# -*- encoding: utf8 -*-

import os

# Version
version_file_path = os.path.join(os.path.dirname(__file__), 'VERSION')
try:
    with open(version_file_path) as f:
        __version__ = f.read().strip()
except FileNotFoundError:
    __version__ = 'unknown version; VERSION file not found'
