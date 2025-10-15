from __future__ import annotations

from ._version import version as __version__
from .comparison import (
    get_asymmetrical_uncertainties,
    get_comparison,
    get_difference,
    get_pull,
    get_ratio,
    get_ratio_variances,
)
from .histogramming import create_axis, flatten_2d_hist, make_2d_hist, make_hist
from .plothist_style import (
    add_luminosity,
    add_text,
    cubehelix_palette,
    get_color_palette,
    plot_reordered_legend,
    set_fitting_ylabel_fontsize,
    set_style,
)
from .plotters import (
    create_comparison_figure,
    plot_2d_hist,
    plot_2d_hist_with_projections,
    plot_comparison,
    plot_data_model_comparison,
    plot_error_hist,
    plot_function,
    plot_hist,
    plot_hist_uncertainties,
    plot_model,
    plot_two_hist_comparison,
    savefig,
)
from .variable_registry import (
    create_variable_registry,
    get_variable_from_registry,
    remove_variable_registry_parameters,
    update_variable_registry,
    update_variable_registry_binning,
    update_variable_registry_ranges,
)

__all__ = [
    "__version__",
    "add_luminosity",
    "add_text",
    "create_axis",
    "create_comparison_figure",
    "create_variable_registry",
    "cubehelix_palette",
    "flatten_2d_hist",
    "get_asymmetrical_uncertainties",
    "get_color_palette",
    "get_comparison",
    "get_difference",
    "get_pull",
    "get_ratio",
    "get_ratio_variances",
    "get_variable_from_registry",
    "make_2d_hist",
    "make_hist",
    "plot_2d_hist",
    "plot_2d_hist_with_projections",
    "plot_comparison",
    "plot_data_model_comparison",
    "plot_error_hist",
    "plot_function",
    "plot_hist",
    "plot_hist_uncertainties",
    "plot_model",
    "plot_reordered_legend",
    "plot_two_hist_comparison",
    "remove_variable_registry_parameters",
    "savefig",
    "set_fitting_ylabel_fontsize",
    "set_style",
    "update_variable_registry",
    "update_variable_registry_binning",
    "update_variable_registry_ranges",
]


from importlib import resources
from importlib.resources import files

import boost_histogram as bh
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt

# Get style file and use it

style_file = files("plothist").joinpath("default_style.mplstyle")
plt.style.use(style_file)

# Install fonts

with resources.as_file(resources.files("plothist_utils") / "fonts") as font_path:
    font_files = fm.findSystemFonts(fontpaths=[str(font_path)])
    for font in font_files:
        fm.fontManager.addfont(font)

# Check version of boost_histogram

if tuple(int(part) for part in bh.__version__.split(".")) < (1, 4, 0):
    raise ImportError(
        "The version of boost_histogram is lower than 1.4.0. Please update to the latest version to avoid issues (pip install --upgrade boost_histogram).",
    )
