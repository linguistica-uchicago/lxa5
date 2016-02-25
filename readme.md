Linguistica 5
=============

Linguistica 5 is a Python library for unsupervised learning
of linguistic structure, based on Goldsmith (2001, 2006) and all subsequent
developments.

Full documentation: http://linguistica-uchicago.github.io/lxa5/

Apart from being a Python library, Linguistica 5 provides two additional
interfaces: (i) graphical user interface; (ii) command line interface.

Work by Jackson Lee and John Goldsmith


Download and install
--------------------

Linguistica 5 requires Python 3.4 or above.

Dependencies:

* NumPy
* SciPy
* NetworkX
* [PyQt5](https://www.riverbankcomputing.com/software/pyqt/download5)
  (for the graphical user interface; including the WebKit module)

Linux users -- SciPy has its own dependencies. If you are on Ubuntu,
run this before installing SciPy:
`sudo apt-get install libblas-dev liblapack-dev libatlas-base-dev gfortran`

PyQt5 -- Ubuntu users can install it by running this:
`sudo apt-get install python3-sip python3-pyqt5 python3-pyqt5.qtwebkit`

NumPy, SciPy, and NetworkX are conveniently available via `pip`
(and will be automatically installed when Linguistica 5 is installed,
if they are absent on your system).

Currently, Linguistica 5 is hosted on GitHub:

```
$ git clone https://github.com/linguistica-uchicago/lxa5.git
$ cd lxa5
$ python3 setup.py install
```

`python3` is meant to point to your Python 3 interpreter.
Administrative privileges (such as `sudo` on Unix-like systems) may be required.


Using Linguistica 5
-------------------

To use Linguistica 5 as a Python library, simply import `linguistica`
in your Python programs:

```python
import linguistica as lxa
```

To launch the Linguistica 5 graphical user interface:

```
$ python3 -m linguistica gui
```

To use Linguistica 5 as a command line tool:

```
$ python3 -m linguistica cmd
```
