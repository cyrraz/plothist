
========
plothist
========

**Visualize and compare data in a scalable way and a beautiful style.**

* Installation and documentation: `https://plothist.readthedocs.io/ <https://plothist.readthedocs.io/>`_
* Example gallery: `https://plothist.readthedocs.io/en/latest/example_gallery/ <https://plothist.readthedocs.io/en/latest/example_gallery/>`_

|img1| |img2|

.. |img1| image:: https://raw.githubusercontent.com/cyrraz/plothist/main/docs/img/1d_comparison_advanced.svg
   :alt: Example
   :width: 320

.. |img2| image:: https://raw.githubusercontent.com/cyrraz/plothist/main/docs/img/model_examples_stacked.svg
   :alt: Example
   :width: 320


|GitHub Project| |PyPI version| |conda version| |Docs from main| |Discussion| |DOI|

|GitHub Actions Status: CI| |GitHub Actions Status: CD| |Linter| |pre-commit.ci Status| |Code Coverage|

This package is a wrapper around `matplotlib <https://matplotlib.org/>`_.

**Advantages of the package**: scalability, style and user-friendly way of managing variables and a stunning `example gallery <https://plothist.readthedocs.io/en/latest/example_gallery/>`_.

1. **First idea**: default style is already presentation-ready and/or publication-ready (with no effort).

2. **Second idea**: separate the histogram creation from its plotting. This allows to easily manage histogram objects (defined in the ``boost_histogram`` `package <https://boost-histogram.readthedocs.io/>`_) and plot large amount of variables and data really fast.

3. **Third idea**: visualize a lot of variables easily with a variable manager. Really easy to modify the plotting information and make multiple plots of the same variable with different settings.

4. **Fourth idea**: detailed and user-friendly documentation including a marvelous `example gallery <https://plothist.readthedocs.io/en/latest/example_gallery/>`_.



.. image:: https://raw.githubusercontent.com/cyrraz/plothist/main/docs/img/2d_hist_with_projections.svg
   :alt: 2D histogram with projections
   :width: 500
   :align: center



.. |GitHub Project| image:: https://img.shields.io/badge/GitHub--blue?style=social&logo=GitHub
   :target: https://github.com/cyrraz/plothist
.. |PyPI version| image:: https://badge.fury.io/py/plothist.svg?style=flat-square
   :target: https://badge.fury.io/py/plothist
.. |conda version| image:: https://img.shields.io/conda/vn/conda-forge/plothist?style=flat-square
   :target: https://anaconda.org/conda-forge/plothist
.. |Docs from main| image:: https://img.shields.io/badge/docs-main-blue.svg?style=platic
   :target: https://plothist.readthedocs.io/en/main/
.. |Discussion| image:: https://img.shields.io/static/v1?label=Discussions&message=Ask&color=blue&logo=github?style=flat-square
   :target: https://github.com/cyrraz/plothist/discussions
.. |DOI| image:: https://zenodo.org/badge/647069945.svg?style=flat-square
   :target: https://zenodo.org/doi/10.5281/zenodo.10995667
.. |Linter| image:: https://img.shields.io/badge/Linter-Ruff-brightgreen?style=platic
   :target: https://github.com/charliermarsh/ruff
.. |GitHub Actions Status: CI| image:: https://github.com/cyrraz/plothist/actions/workflows/ci.yaml/badge.svg?style=flat-square
   :target: https://github.com/cyrraz/plothist/actions/workflows/ci.yaml?query=branch%3Amain
.. |GitHub Actions Status: CD| image:: https://github.com/cyrraz/plothist/actions/workflows/cd.yaml/badge.svg?style=flat-square
   :target: https://github.com/cyrraz/plothist/actions/workflows/cd.yaml?query=branch%3Amain
.. |pre-commit.ci Status| image:: https://results.pre-commit.ci/badge/github/cyrraz/plothist/main.svg?style=flat-square
   :target: https://results.pre-commit.ci/latest/github/cyrraz/plothist/main
.. |Code Coverage| image:: https://codecov.io/gh/cyrraz/plothist/branch/main/graph/badge.svg?style=flat-square
    :target: https://codecov.io/gh/cyrraz/plothist
