from .plotters import (
    create_comparison_figure,
    plot_hist,
    plot_2d_hist,
    plot_2d_hist_with_projections,
    plot_error_hist,
    plot_hist_uncertainties,
    plot_two_hist_comparison,
    plot_comparison,
    savefig,
    plot_data_model_comparison,
    plot_model,
    plot_function,
)

from .histogramming import (
    create_axis,
    make_hist,
    make_2d_hist,
    flatten_2d_hist,
)

from .variable_registry import (
    create_variable_registry,
    get_variable_from_registry,
    update_variable_registry,
    remove_variable_registry_parameters,
    update_variable_registry_ranges,
)

from .comparison import (
    get_asymmetrical_uncertainties,
    get_comparison,
    get_pull,
    get_difference,
    get_ratio,
    get_ratio_variances,
)

from .plothist_style import (
    set_style,
    cubehelix_palette,
    get_color_palette,
    set_fitting_ylabel_fontsize,
    add_text,
    add_luminosity,
    plot_reordered_legend,
)

from .get_dummy_data import get_dummy_data

__all__ = [
    "__version__",
    "create_variable_registry",
    "get_variable_from_registry",
    "update_variable_registry",
    "remove_variable_registry_parameters",
    "update_variable_registry_ranges",
    "create_comparison_figure",
    "create_axis",
    "make_hist",
    "make_2d_hist",
    "plot_hist",
    "plot_2d_hist",
    "plot_2d_hist_with_projections",
    "plot_error_hist",
    "plot_hist_uncertainties",
    "plot_two_hist_comparison",
    "plot_comparison",
    "savefig",
    "plot_data_model_comparison",
    "plot_model",
    "plot_function",
    "add_luminosity",
    "get_asymmetrical_uncertainties",
    "set_style",
    "cubehelix_palette",
    "get_color_palette",
    "set_fitting_ylabel_fontsize",
    "add_text",
    "get_asymmetrical_uncertainties",
    "get_comparison",
    "get_pull",
    "get_difference",
    "get_ratio",
    "get_ratio_variances",
    "flatten_2d_hist",
    "plot_reordered_legend",
    "get_dummy_data",
]


# Get style file and use it
import matplotlib.pyplot as plt
from importlib.resources import files

style_file = files("plothist").joinpath("default_style.mplstyle")
plt.style.use(style_file)

# Check the fonts
from matplotlib.font_manager import findfont
import warnings

for font_type in ["Math", "Sans", "Roman"]:
    try:
        findfont(f"Latin Modern {font_type}", fallback_to_default=False)
    except:
        warnings.warn(
            "The recommended fonts to use plothist were not found. You can install them by typing 'install_latin_modern_fonts' in your terminal. If it still does not work, please check the documentation at https://plothist.readthedocs.io/en/latest/usage/font_installation.html",
            stacklevel=3,
        )
        break

# Check version of boost_histogram
import boost_histogram as bh

if tuple(int(part) for part in bh.__version__.split(".")) < (1, 4, 0):
    raise ImportError(
        "The version of boost_histogram is lower than 1.4.0. Please update to the latest version to avoid issues (pip install --upgrade boost_histogram).",
    )
