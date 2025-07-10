import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pytest

import plothist
from plothist.test_helpers import run_script_and_get_object

mpl_image_compare_kwargs = {
    "baseline_dir": "../docs/img",
    "savefig_kwargs": {"bbox_inches": "tight"},
    "style": "plothist.default_style",
    "deterministic": True,
}


script_dir = Path(plothist.__file__).parent / "examples" / "advanced"

current_module = sys.modules[__name__]


@pytest.fixture(autouse=True)
def close_all_figures():
    """Automatically close all figures after each test."""
    yield
    plt.close("all")


for script_path in script_dir.glob("*.py"):
    filename = f"{script_path.stem}.png"
    test_name = f"test_{script_path.stem}"

    @pytest.mark.mpl_image_compare(filename=filename, **mpl_image_compare_kwargs)
    def func_test(script=script_path):
        return run_script_and_get_object(script, "fig")

    func_test.__name__ = test_name
    setattr(current_module, test_name, func_test)
