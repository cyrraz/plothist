.. _contributing:

============
Contributing
============

Building from source
====================

Follow the instructions in :ref:`install-dev-version` to install the development version of ``plothist``.

Setting up a development environment
====================================

Nox
---

The fastest way to start with development is to use ``nox``.

``Nox`` is an automation tool that helps manage and run development tasks such as testing and linting.
It is especially useful for ensuring your code works across different Python versions and adheres to the project's quality standards.
``Nox`` handles everything for you, including setting up a temporary virtual environment for each run.

To set up ``nox``:

1. If you don't have it already, install ``pipx`` by following the instructions on their `website <https://pipx.pypa.io/stable/>`_.
2. Install ``nox`` using ``pipx``:

   .. code-block:: console

      pipx install nox

To use ``nox``, simply run:

.. code-block:: console

   nox

This will lint and test the project using multiple Python versions.

You can also run specific jobs:

.. code-block:: console

   nox -l        # List all the defined sessions
   nox -s lint   # Run the linter only
   nox -s tests  # Run the tests only
