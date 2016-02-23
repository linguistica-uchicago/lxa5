Linguistica 5: Unsupervised Learning of Linguistic Structure
==========================================================

Full documentation: http://linguistica-uchicago.github.io/lxa5/

This is the eventual new home of the *Linguistica 5* code.

Code for both the **Python library** and **graphical user interface**
is at this present repository.
Both interfaces are operational; see documentation.

Work by Jackson Lee and John Goldsmith

Download and install
--------------------

Linguistica 5 requires Python 3.4 or above.

Currently, Linguistica 5 is hosted on GitHub:

```
$ git clone https://github.com/linguistica-uchicago/lxa5.git
$ cd lxa5
$ python3 setup.py install
```

(`python3` is meant to point to your Python 3 interpreter.
Administrative privileges (such as `sudo` on Unix-like systems) may be required.)


Using Linguistica 5 as a Python library
---------------------------------------

Simply import `linguistica` in your Python programs:

```python
import linguistica as lxa
```

Using Linguistica 5 as a graphical user interface software
----------------------------------------------------------

[PyQt5](https://www.riverbankcomputing.com/software/pyqt/download5)
(including the WebKit module) is required.
Ubuntu users can obtain it by running this:

```
$ sudo apt-get install python3-sip python3-pyqt5 python3-pyqt5.qtwebkit
```

After PyQt5 is installed, launch the Linguistica GUI with this command:

```
$ python3 -m linguistica gui
```

Using Linguistica 5 as a command line tool
------------------------------------------

Run this:

```
$ python3 -m linguistica cmd
```
