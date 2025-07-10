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


script_dir = Path(plothist.__file__).parent / "examples" / "2d_hist"

current_module = sys.modules[__name__]

exclude_scripts = [
    "2d_hist_correlations",  # multiple figures
]


@pytest.fixture(autouse=True)
def close_all_figures():
    """Automatically close all figures after each test."""
    yield
    plt.close("all")


for script_path in script_dir.glob("*.py"):
    if script_path.stem in exclude_scripts:
        continue
    filename = f"{script_path.stem}.png"
    test_name = f"test_{script_path.stem}"

    @pytest.mark.mpl_image_compare(filename=filename, **mpl_image_compare_kwargs)
    def func_test(script=script_path):
        return run_script_and_get_object(script, "fig")

    func_test.__name__ = test_name
    setattr(current_module, test_name, func_test)


@pytest.mark.mpl_image_compare(
    filename="2d_hist_correlations_0.png", **mpl_image_compare_kwargs
)
def test_2d_hist_correlations_0():
    return run_script_and_get_object(script_dir / "2d_hist_correlations.py", "figs")[0]


@pytest.mark.mpl_image_compare(
    filename="2d_hist_correlations_1.png", **mpl_image_compare_kwargs
)
def test_2d_hist_correlations_1():
    return run_script_and_get_object(script_dir / "2d_hist_correlations.py", "figs")[1]


@pytest.mark.mpl_image_compare(
    filename="2d_hist_correlations_2.png", **mpl_image_compare_kwargs
)
def test_2d_hist_correlations_2():
    return run_script_and_get_object(script_dir / "2d_hist_correlations.py", "figs")[2]
