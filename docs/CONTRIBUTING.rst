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

You can also run specific nox sessions:

.. code-block:: console

   # List all the defined sessions
   nox -l
   # Run the linter only
   nox -s lint
   # Run the tests only
   nox -s tests
   # Build the documentation and serve it locally (display the documentation in a web browser with live-reloading)
   nox -s docs
   # Build the documentation without serving it
   nox -s docs --non-interactive
   # Check for broken links in the documentation
   nox -s docs -- -b linkcheck

Linters and Formatters
----------------------

``plothist`` uses `pre-commit <https://pre-commit.com/>`_ to manage linters and formatters.

The tools are listed in ``.pre-commit-config.yaml``. Key among them is ``Ruff`` is used for linting and formatting, with its configuration in ``pyproject.toml``.

Use ``nox -s lint`` to run the linters and formatters.

To install the pre-commit hooks, run the following command (assuming you have installed  ``plothist`` via ``uv`` following the instructions in :ref:`install-dev-version`):

.. code-block:: console

   uv run pre-commit install
