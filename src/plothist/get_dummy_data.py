from importlib.resources import files

import numpy as np


def get_dummy_data():
    """
    Get dummy data for plotting examples as a numpy ndarray.

    Returns
    -------
    data : numpy ndarray
        Dummy data.
    """
    dummy_data_file = files("plothist").joinpath("dummy_data.csv")
    with open(dummy_data_file) as f:
        data = np.genfromtxt(f, delimiter=",", names=True)
    return data
