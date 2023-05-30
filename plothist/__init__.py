"""Plot histograms in a scalable way and a beautiful style."""
import matplotlib.pyplot as plt
from importlib.resources import path as resources_path

__version__ = "0.0"

# Get style file and use it
# Deprecated function to access style file, to be updated
# https://docs.python.org/3/library/importlib.resources.html
with resources_path("plothist", "style.mplstyle") as style_file:
    plt.style.use(style_file.as_posix())
