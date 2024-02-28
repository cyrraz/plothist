from importlib.resources import path as resources_path
import numpy as np


def get_dummy_data():
    """
    Get dummy data for plotting examples as a numpy ndarray.

    Returns
    -------
    data : numpy ndarray
        Dummy data.
    """
    with resources_path("plothist", "dummy_data.csv") as dummy_data:
        with open(dummy_data, "r") as f:
            data = np.genfromtxt(f, delimiter=",", names=True)
    return data
