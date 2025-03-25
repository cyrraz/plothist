# Contributing

## Building from source

Follow the instructions in [Install the development version](docs/usage/installation.rst#install-the-development-version) to install the development version of `plothist`.

## Setting up a development environment

### Nox

The fastest way to start with development is to use `nox`.

1.  If you don't have it already, install `pipx` following the instructions on their [website](https://pipx.pypa.io/stable/).
2.  Install `nox` with `pipx`: `pipx install nox`.

To use, run `nox`. This will lint and test using multiple Python versions.

You can also run specific jobs:

```console
$ nox -l # List all the defined sessions
$ nox -s lint  # Lint only
$ nox -s tests  # Tests only
```

`Nox` handles everything for you, including setting up a temporary virtual environment for each run.
