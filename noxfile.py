from __future__ import annotations

import argparse

import nox

nox.options.sessions = ["lint", "tests"]
nox.needs_version = ">=2025.2.9"
nox.options.default_venv_backend = "uv|venv"

PYTHON_ALL_VERSIONS = ["3.9", "3.10", "3.11", "3.12", "3.13"]


@nox.session(reuse_venv=True)
def lint(session: nox.Session) -> None:
    """
    Run the linter.
    """
    session.install("pre-commit")
    session.run("pre-commit", "run", "--all-files", *session.posargs)


@nox.session(python=PYTHON_ALL_VERSIONS)
def tests(session: nox.Session) -> None:
    """
    Run the unit and regular tests.
    """
    pyproject = nox.project.load_toml("pyproject.toml")
    session.install("-e", ".")
    session.install(*nox.project.dependency_groups(pyproject, "test"))
    session.run("pytest", *session.posargs)


# run coverage
@nox.session(reuse_venv=True)
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


@nox.session(reuse_venv=True)
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
