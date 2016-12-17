# Linguistica 5

These notes are for the core developers of the project only.

## Installing the library in development mode


First and foremost, you need to have Linguistica 5 installed *in development mode*.
If you have Linguistica 5 installed, be sure to uninstall:

```
$ pip uninstall linguistica
```

Then install it with the `develop` flag:

```
$ git clone https://github.com/linguistica-uchicago/lxa5.git
$ cd lxa5
$ python setup.py develop
```

## Install the dependencies for development and documentation

```
$ pip install Sphinx flake8 pytest pytest-cov sphinx_rtd_theme
```

## Run tests

At the root directory of the project:

```
$ pytest -v --cov
```

## Build documentation

At the root directory of the project:

```
$ sh build-doc.sh
```

## Package the library for PyPI release

Only for core developers with admin access to upload to https://pypi.python.org/pypi/linguistica

### Confirm the new version number

Be very sure that the version number (defined nowhere but in `linguistica/VERSION` from the project root directory)
is updated correctly and does not already appear on https://pypi.python.org/pypi/linguistica

### Prepare credentials for PyPI

You need an account at both https://pypi.python.org/pypi and https://testpypi.python.org/pypi
(a separate account for each site; just use the same username and password for both sites).

Then you need to prepare `$HOME/.pypirc` which contains the following (paste in your own username and password):

```
[distutils]
index-servers =
  pypi
  pypitest

[pypi]
repository=https://pypi.python.org/pypi
username=<USERNAME>
password=<PASSWORD>

[pypitest]
repository=https://testpypi.python.org/pypi
username=<USERNAME>
password=<PASSWORD>
```

### Test if everything looks good

Remember you have an account for https://testpypi.python.org/pypi ?
This is for testing purposes.

To register the package against PyPI's *test* server: 

```
$ python setup.py register -r pypitest
```

If you get the server response 200, then everything is set up correctly.


To see what the package would look like on PyPI:

```
$ python setup.py sdist bdist_wheel upload -r pypitest
```

Again, if you get the server response 200, then everything is set up correctly.
Also, check out how the actual PyPI release page would look like: https://testpypi.python.org/pypi/linguistica

Furthermore, under the directory `dist/`, you should now see a `.tar.gz` and `.whl` with the new version number.

### Release the library to PyPI for real!

If you don't have `twine` installed yet (it's for PyPI release):

```
$ pip install twine
```

Use the following command to upload the appropriate `.tar.gz` and `.whl` to PyPI:

```
$ twine upload dist/<filename ending in .tar.gz or .whl>
```
