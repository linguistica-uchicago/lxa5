from os import path
from setuptools import setup, find_packages

_THIS_DIR = path.dirname(__file__)


def main():
    version_path = path.join(_THIS_DIR, 'linguistica', 'VERSION')
    with open(version_path) as f:
        package_version = f.read().strip()

    readme_path = path.join(_THIS_DIR, 'README.rst')
    with open(readme_path) as f:
        long_description = f.read()

    requirements_path = path.join(_THIS_DIR, 'requirements.txt')
    with open(requirements_path) as f:
        requirements = [x.strip() for x in f.readlines()]

    setup(
        name='linguistica',
        version=package_version,
        description='Linguistica 5: Unsupervised Learning of Linguistic Structure',  # noqa
        long_description=long_description,
        url='http://linguistica.uchicago.edu/',
        author='Jackson Lee',
        author_email='jacksonlunlee@gmail.com',
        license='MIT License',
        packages=find_packages(),
        keywords=[
            'computational linguistics', 'natural language processing',
            'NLP', 'linguistics', 'corpora', 'speech',
            'language', 'machine learning', 'unsupervised learning',
            'data visualization'],

        install_requires=requirements,

        package_data={
          'linguistica': [
              'VERSION',
              'gui/*',
              'datasets/*',
              'tests/data/*',
          ],
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
          'Programming Language :: Python :: 3.7',
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


if __name__ == '__main__':
    main()
