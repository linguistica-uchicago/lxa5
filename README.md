# Linguistica 5

[![PyPI version](https://badge.fury.io/py/linguistica.svg)](https://pypi.org/project/linguistica/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/linguistica.svg)](https://pypi.org/project/linguistica/)
[![Paper](https://img.shields.io/badge/paper-NAACL_2016-blue.svg)](https://aclanthology.org/N16-3005/)


Linguistica 5 is a Python library for unsupervised learning
of linguistic structure.

Full documentation: https://linguistica.readthedocs.io/

Apart from being a Python library, Linguistica 5 provides two additional
interfaces: (i) graphical user interface; (ii) command line interface.

## Download and install

Note: If you are a developer of the Linguistica project group, you should ignore
this section and set up your environment by following
[CONTRIBUTING.md](CONTRIBUTING.md).

Linguistica 5 is available through `pip`:

```bash
pip install linguistica
```

Linguistica 5 works with Python 3.12+.

The graphical user interface requires `PyQt5` and `PyQtWebEngine` (the latter
powers the word-neighbor manifold visualization). Install them together with the
`gui` extra:

```bash
pip install "linguistica[gui]"
```

These install as binary wheels on x86_64 Linux, Windows, and macOS (including Apple
Silicon).
On aarch64 Linux or Alpine/musl, where wheels are not published, `pip` may build
from source instead.

## Using Linguistica 5

To use Linguistica 5 as a Python library, simply import `linguistica`
in your Python programs:

```python
import linguistica as lxa
```

Quick library demo [here](https://linguistica.readthedocs.io/latest/demo.html).

To launch the Linguistica 5 graphical user interface
(with the `gui` extra installed):

```bash
linguistica gui
```

To launch the Linguistica 5 command line interface:

```bash
linguistica cli
```

## Citation

If you use Linguistica 5, please cite this paper:

Jackson L. Lee and John A. Goldsmith. 2016.
[Linguistica 5: Unsupervised Learning of Linguistic Structure](https://aclanthology.org/N16-3005/).
In *Proceedings of the 2016 Conference of the North American Chapter of the Association for Computational Linguistics: Demonstrations*, pages 22–26, San Diego, California. Association for Computational Linguistics.

```bibtex
@InProceedings{lee-goldsmith:2016:lxa5,
  title = "Linguistica 5: Unsupervised Learning of Linguistic Structure",
  author = "Lee, Jackson L.  and
      Goldsmith, John A.",
  editor = "DeNero, John  and
      Finlayson, Mark  and
      Reddy, Sravana",
  booktitle = "Proceedings of the 2016 Conference of the North {A}merican Chapter of the Association for Computational Linguistics: Demonstrations",
  month = jun,
  year = "2016",
  address = "San Diego, California",
  publisher = "Association for Computational Linguistics",
  url = "https://aclanthology.org/N16-3005/",
  doi = "10.18653/v1/N16-3005",
  pages = "22--26"
}
```

## Technical support

Please [open issues](https://github.com/linguistica-uchicago/lxa5/issues/new)
for questions and bug reports.
Alternatively, please feel free to contact
[Jackson Lee](http://jacksonllee.com/) and
[John Goldsmith](http://people.cs.uchicago.edu/~jagoldsm/).

## License

MIT License

See `LICENSE.txt` on the [GitHub repository](https://github.com/linguistica-uchicago/lxa5).
