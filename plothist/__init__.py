__doc__ = """Plot histograms in a scalable way and a beautiful style."""
__version__ = "0.1"

from .plotters import (
    create_variable_registry,
    get_variable_from_registry,
    update_variable_registry_ranges,
    create_axis,
    make_hist,
    make_2d_hist,
    plot_hist,
    plot_2d_hist,
    plot_error_hist,
    plot_hist_difference,
    compare_two_hist,
    cubehelix_palette,
)

from .hep_plotters import compare_data_mc, plot_mc, plot_b2_logo

__all__ = [
    "__version__",
    "create_variable_registry",
    "get_variable_from_registry",
    "update_variable_registry_ranges",
    "create_axis",
    "make_hist",
    "make_2d_hist",
    "plot_hist",
    "plot_2d_hist",
    "plot_error_hist",
    "plot_hist_difference",
    "compare_two_hist",
    "cubehelix_palette",
    "compare_data_mc",
    "plot_mc",
    "plot_b2_logo",
]


# Get style file and use it
# Deprecated function to access style file, to be updated
# https://docs.python.org/3/library/importlib.resources.html
import matplotlib.pyplot as plt
from importlib.resources import path as resources_path

with resources_path("plothist", "style.mplstyle") as style_file:
    plt.style.use(style_file.as_posix())
