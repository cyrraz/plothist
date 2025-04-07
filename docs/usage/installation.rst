.. _installation-label:

=======================
Installation and update
=======================

Prerequisite
============

You need version 3.9 (or a more recent version) of Python 3. You can check your version of Python 3 with:

.. code-block:: bash

   python3 --version

Using PyPI (stable version)
===========================

Install ``plothist``
--------------------

1.  (Optional) Setup and activate a virtual environment:

    .. code-block:: bash

       python3 -m venv .venv

       source .venv/bin/activate


2. Install ``plothist`` from ``PyPI`` into your environment.

   a.  If you have a local installation, you can use the normal setup command:

   .. code-block:: bash

       python3 -m pip install plothist


   b.  If this fails because you do not have write access to where your virtual environment lives, you can also install ``plothist`` locally:

   .. code-block:: bash

       python3 -m pip install --user plothist

This will automatically also install ``plothist`` into your current environment.
Please make sure to always setup your environment correctly before using ``plothist``.

The ``plothist`` package can now be imported in any of your scripts. Now you can go on with the step by step tutorial starting with :ref:`basics-1d_hist-label` or directly to the `example gallery <https://plothist.readthedocs.io/en/latest/example_gallery/>`_.


Update ``plothist``
-------------------

To update ``plothist`` to its latest stable version, follow the instructions above, adding the argument ``--upgrade`` right after ``pip3 install``:

.. code-block:: bash

    python3 -m pip install --upgrade [--user] plothist


.. _install-dev-version:

Install the development version
===============================

1. Clone the plothist repository and go to the package folder:

    .. code-block:: bash

       git clone git@github.com:cyrraz/plothist.git

       cd plothist

Option 1 (recommended) - Using ``uv``
-------------------------------------

2. Install ``uv`` following the instructions in the `uv documentation <https://docs.astral.sh/uv/getting-started/installation/>`_.

3. Run the following commands to setup a virtual environment and install the package:

    .. code-block:: bash

       uv sync --group dev --group test

The previous command creates a virtual environment ``.venv`` and installs the package in editable mode with the development and test dependencies.

4. To activate the virtual environment, run:

    .. code-block:: bash

       source .venv/bin/activate

Option 2 - Not using ``uv``
---------------------------

2.  Setup and activate a virtual environment:

    .. code-block:: bash

       python3 -m venv .venv

       source .venv/bin/activate

3. Run the following command to install the package in editable mode with the development and test dependencies:

    .. code-block:: bash

       python3 -m pip install --editable ".[dev,test]"

To update ``plothist`` to its latest development version, go to the package folder and run:

.. code-block:: bash

    git pull
