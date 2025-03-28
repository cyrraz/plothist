import nox

nox.options.sessions = ["lint", "tests"]
nox.options.default_venv_backend = "uv|venv"

PYTHON_ALL_VERSIONS = ["3.9", "3.10", "3.11", "3.12", "3.13"]


@nox.session(reuse_venv=True)
def lint(session):
    """
    Run the linter.
    """
    session.install("pre-commit")
    session.run("pre-commit", "run", "--all-files", *session.posargs)


@nox.session(python=PYTHON_ALL_VERSIONS)
def tests(session):
    """
    Run the unit and regular tests.
    """
    pyproject = nox.project.load_toml("pyproject.toml")
    session.install(*nox.project.dependency_groups(pyproject, "test"))
    session.install("-v", ".")
    session.run("pytest", *session.posargs)
