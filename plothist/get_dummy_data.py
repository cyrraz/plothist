import pandas as pd
from importlib.resources import path as resources_path


def get_dummy_data():
    with resources_path("plothist", "dummy_data.csv") as dummy_data:
        return pd.read_csv(dummy_data)
