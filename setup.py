from os import path
from setuptools import setup, find_packages

this_dir = path.dirname(__file__)

version_path = path.join(this_dir, 'linguistica', 'VERSION')
with open(version_path) as f:
    package_version = f.read().strip()

readme_path = path.join(this_dir, 'README.rst')
with open(readme_path) as f:
    long_description = f.read()

requirements_path = path.join(this_dir, 'requirements.txt')
with open(requirements_path) as f:
    requirements = [x.strip() for x in f.readlines()]

setup(name='linguistica',
      version=package_version,
      description='Linguistica 5: Unsupervised Learning of Linguistic Structure',
      long_description=long_description,
      url='http://linguistica.uchicago.edu/',
      author='Jackson Lee',
      author_email='jacksonlunlee@gmail.com',
      license='MIT License',
      packages=find_packages(),
      keywords=['computational linguistics', 'natural language processing',
                'NLP', 'linguistics', 'corpora', 'speech',
                'language', 'machine learning', 'unsupervised learning',
                'data visualization'],

      install_requires=requirements,

      package_data={
          'linguistica': ['VERSION', 'gui/d3.min.js',
                          'gui/lxa_splash_screen.png',
                          'datasets/*.txt', 'datasets/*.dx1'],
      },

      zip_safe=False,

      entry_points={
          'console_scripts': [
              'linguistica = linguistica.__main__:main'
          ]
      },

      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'Intended Audience :: Education',
          'Intended Audience :: Information Technology',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
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
