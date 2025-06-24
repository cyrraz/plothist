import runpy
from pathlib import Path

import matplotlib.figure


def run_script_and_get_fig(script_path_str: str) -> matplotlib.figure.Figure | None:
    """
    Executes a Python script located at the specified filesystem path, suppresses any calls to
    'matplotlib.figure.Figure.savefig' during execution to prevent file output, and returns the
    'fig' object if it is defined in the script's global namespace.

    Parameters:
        script_path_str (str): Filesystem path to the Python script to be executed.

    Returns:
        matplotlib.figure.Figure or None: The 'fig' object created in the script if present;
                                           otherwise, None.
    """
    script_path = Path(script_path_str).resolve()

    if not script_path.is_file():
        raise FileNotFoundError(f"Script file not found: {script_path_str}")

    original_savefig = matplotlib.figure.Figure.savefig

    def suppressed_savefig(*args, **kwargs):
        pass

    matplotlib.figure.Figure.savefig = suppressed_savefig

    try:
        globals_dict = runpy.run_path(str(script_path))
    finally:
        matplotlib.figure.Figure.savefig = original_savefig

    return globals_dict.get("fig")
