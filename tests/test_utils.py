import runpy
from importlib.util import find_spec
from pathlib import Path

import matplotlib.figure


def run_script_and_get_fig(module_path: str) -> matplotlib.figure.Figure | None:
    """
    Execute a script given by its module path string (e.g., 'pkg.subpkg.script'),
    suppress any 'fig.savefig' calls inside it, and return the 'fig' object.

    Parameters:
        module_path (str): Dotted module path to the script (e.g., 'plothist.examples.func_1d.fct_1d')

    Returns:
        matplotlib.figure.Figure or None: The figure created in the script, or None if not found.
    """

    spec = find_spec(module_path)

    if spec is None or spec.origin is None:
        raise ImportError(f"Cannot find module '{module_path}'")

    script_path = Path(spec.origin).resolve()

    original_savefig = matplotlib.figure.Figure.savefig

    def suppressed_savefig(*args, **kwargs):
        pass

    matplotlib.figure.Figure.savefig = suppressed_savefig

    try:
        globals_dict = runpy.run_path(str(script_path))
    finally:
        matplotlib.figure.Figure.savefig = original_savefig

    return globals_dict.get("fig")
