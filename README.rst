
========
plothist
========

**Plot histograms in a scalable way and a beautiful style.**

Installation and documentation: `https://plothist.readthedocs.io/ <https://plothist.readthedocs.io/>`_

|img1| |img2|

.. |img1| image:: https://raw.githubusercontent.com/cyrraz/plothist/main/docs/img/hep_examples_dataMC_stacked.svg
   :alt: Hep example
   :width: 320

.. |img2| image:: https://raw.githubusercontent.com/cyrraz/plothist/main/docs/img/hep_examples_dataMC_flatten2D.svg
   :alt: Hep example
   :width: 320


|GitHub Project| |PyPI version| |Docs from latest| |Docs from main| |Code style: black|


**Major advantages over other plotting libraries**: scalability, style and user friendly way of managing variables.

1. **First idea**: Default style is already presentation-ready and/or paper-ready (with no effort).

2. **Second idea**: separate the histogram creation from its plotting. Then you can easily manage histogram objects (``boost_histogram`` library) and plot large amount of variables and data really fast.

3. **Third idea**: plot a lot of variable easily with a variable manager. Really easy to modify the plotting information and do multiple plots with same variable but different settings.


.. image:: https://raw.githubusercontent.com/cyrraz/plothist/main/docs/img/intro_2dhist_complexe.svg
   :alt: Complexe hep example
   :width: 500
   :align: center



.. |GitHub Project| image:: https://img.shields.io/badge/GitHub--blue?style=social&logo=GitHub
   :target: https://github.com/cyrraz/plothist
.. |PyPI version| image:: https://badge.fury.io/py/plothist.svg
   :target: https://badge.fury.io/py/plothist
.. |Code style: black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
.. |Docs from latest| image:: https://img.shields.io/badge/docs-v0.5.7-blue.svg
   :target: https://plothist.readthedocs.io/en/latest/
.. |Docs from main| image:: https://img.shields.io/badge/docs-main-blue.svg
   :target: https://plothist.readthedocs.io/en/main/