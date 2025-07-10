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

mpl_image_compare_for_default_matplotlib_kwargs = mpl_image_compare_kwargs.copy()
mpl_image_compare_for_default_matplotlib_kwargs["style"] = {
    "font.size": 12,
}

script_dir = Path(plothist.__file__).parent / "examples" / "utility"

current_module = sys.modules[__name__]

exclude_scripts = [
    "color_palette_squares",  # multiple figures
    "matplotlib_vs_plothist_style",  # multiple figures
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
    filename="usage_style_cycle.png", **mpl_image_compare_kwargs
)
def test_color_palette_squares_0():
    return run_script_and_get_object(script_dir / "color_palette_squares.py", "figs")[0]


@pytest.mark.mpl_image_compare(
    filename="usage_cubehelix.png", **mpl_image_compare_kwargs
)
def test_color_palette_squares_1():
    return run_script_and_get_object(script_dir / "color_palette_squares.py", "figs")[1]


@pytest.mark.mpl_image_compare(
    filename="usage_viridis_palette.png", **mpl_image_compare_kwargs
)
def test_color_palette_squares_2():
    return run_script_and_get_object(script_dir / "color_palette_squares.py", "figs")[2]


@pytest.mark.mpl_image_compare(
    filename="usage_coolwarm_palette.png", **mpl_image_compare_kwargs
)
def test_color_palette_squares_3():
    return run_script_and_get_object(script_dir / "color_palette_squares.py", "figs")[3]


@pytest.mark.mpl_image_compare(
    filename="usage_YlGnBu_r_palette.png", **mpl_image_compare_kwargs
)
def test_color_palette_squares_4():
    return run_script_and_get_object(script_dir / "color_palette_squares.py", "figs")[4]


@pytest.mark.mpl_image_compare(
    filename="matplotlib_example.png",
    **mpl_image_compare_for_default_matplotlib_kwargs,
)
def test_matplotlib_vs_plothist_style_matplotlib():
    return run_script_and_get_object(
        script_dir / "matplotlib_vs_plothist_style.py", "figs"
    )[0]


@pytest.mark.mpl_image_compare(
    filename="plothist_example.png", **mpl_image_compare_kwargs
)
def test_matplotlib_vs_plothist_style_plothist():
    return run_script_and_get_object(
        script_dir / "matplotlib_vs_plothist_style.py", "figs"
    )[1]
