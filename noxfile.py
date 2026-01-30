#!/usr/bin/env -S uv run --script

# /// script
# dependencies = ["nox>=2025.11.12"]
# ///

"""Nox runner."""

from __future__ import annotations

import argparse

import nox

nox.needs_version = ">=2025.11.12"
nox.options.default_venv_backend = "uv|venv"

PYTHON_ALL_VERSIONS = ["3.10", "3.14"]


@nox.session(reuse_venv=True, default=True)
def lint(session: nox.Session) -> None:
    """
    Run the linter.
    """
    session.install("prek")
    session.run("prek", "run", "--all-files", *session.posargs)


@nox.session(python=PYTHON_ALL_VERSIONS, reuse_venv=True, default=True)
def tests(session: nox.Session) -> None:
    """
    Run the unit and regular tests.
    """
    pyproject = nox.project.load_toml("pyproject.toml")
    session.install("-e", ".")
    session.install(*nox.project.dependency_groups(pyproject, "test"))
    session.run("pytest", "--mpl", "-n", "auto", *session.posargs)


@nox.session(reuse_venv=True, default=False)
def generate_examples_figures(session: nox.Session) -> None:
    """
    Generate the example figures. Pass "-- tests/test_examples_*.py" to run only the relevant tests.
    """
    pyproject = nox.project.load_toml("pyproject.toml")
    session.install("-e", ".")
    session.install(*nox.project.dependency_groups(pyproject, "test"))
    session.run(
        "pytest",
        "--mpl-generate-path=docs/img",
        *session.posargs,
    )


# run coverage
@nox.session(reuse_venv=True, default=False)
def coverage(session: nox.Session) -> None:
    """
    Run the unit tests with coverage. Warning: takes a long time to run.
    """
    pyproject = nox.project.load_toml("pyproject.toml")
    session.install("-e", ".")
    session.install(*nox.project.dependency_groups(pyproject, "test"))
    session.run(
        "pytest",
        "--cov=plothist",
        *session.posargs,
    )


@nox.session(reuse_venv=True, default=False)
def docs(session: nox.Session) -> None:
    """
    Build the docs. Pass --non-interactive to avoid serving. Pass "-- -b linkcheck" to check links.
    """
    pyproject = nox.project.load_toml("pyproject.toml")

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-b", dest="builder", default="html", help="Build target (default: html)"
    )
    args, posargs = parser.parse_known_args(session.posargs)
    serve = args.builder == "html" and session.interactive

    extra_installs = ["sphinx-autobuild"] if serve else []
    session.install(
        ".", *nox.project.dependency_groups(pyproject, "docs"), *extra_installs
    )

    shared_args = (
        "-n",  # nitpicky mode
        "-T",  # full tracebacks
        f"-b={args.builder}",
        "docs",
        *(posargs or [f"docs/_build/{args.builder}"]),
    )

    if serve:
        session.run(
            "sphinx-autobuild", "--open-browser", "--ignore=docs/.build", *shared_args
        )
    else:
        session.run("sphinx-build", "--keep-going", *shared_args)


if __name__ == "__main__":
    nox.main()
