#!usr/bin/env python3
# -*- coding: utf-8 -*-

from os import path
import sys
from setuptools import (setup, find_packages)

required_py_version = (3, 4)
current_py_version = sys.version_info[:2]

if current_py_version < required_py_version:
    sys.exit('Error: Linguistica requires Python {}.{} or above.\n'
             .format(*required_py_version) +
             'You are using Python {}.{}.'.format(*current_py_version))

version_path = path.join(path.dirname(__file__), 'linguistica', 'VERSION')
with open(version_path) as f:
    package_version = f.read().strip()

setup(name='linguistica',
      version=package_version,
      description='Linguistica',
      long_description='Linguistica: '
                       'Unsupervised Learning of Linguistic Structure',
      url='http://linguistica.uchicago.edu/',
      author='Jackson Lee',
      author_email='jsllee.phon@gmail.com',
      # license='Apache License, Version 2.0',
      packages=find_packages(),
      keywords=['computational linguistics', 'natural language processing',
                'NLP', 'linguistics', 'corpora', 'speech',
                'language', 'machine learning', 'unsupervised learning',
                'data visualization'],

      install_requires=['scipy', 'numpy', 'networkx'],

      package_data={
          'linguistica': ['VERSION', 'gui/d3.min.js'],
      },

      zip_safe=False,

      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'Intended Audience :: Education',
          'Intended Audience :: Information Technology',
          'Intended Audience :: Science/Research',
          # 'License :: OSI Approved :: Apache Software License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Topic :: Scientific/Engineering',
          'Topic :: Scientific/Engineering :: Artificial Intelligence',
          'Topic :: Scientific/Engineering :: Human Machine Interfaces',
          'Topic :: Scientific/Engineering :: Information Analysis',
          'Topic :: Text Processing',
          'Topic :: Text Processing :: Filters',
          'Topic :: Text Processing :: General',
          'Topic :: Text Processing :: Indexing',
          'Topic :: Text Processing :: Linguistic',
          ],
      )
