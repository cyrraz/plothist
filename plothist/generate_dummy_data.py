import pandas as pd
from sklearn.datasets import make_classification


def generate_dummy_data():
    """Generate dummy data and return a pandas dataframe containing these data.
    The dataframe columns contain:
    * 10 variables named variable_0, ..., variable_9
    * 1 categorical column with 9 categories: 0, ..., 8
    """
    n_features = 10
    X, y = make_classification(
        n_samples=100_000,
        n_features=n_features,
        n_informative=n_features - 2,
        n_classes=9,
        n_clusters_per_class=5,
        class_sep=2,
        random_state=42,
    )
    df = pd.DataFrame(X, columns=[f"variable_{i}" for i in range(n_features)])
    df["category"] = y

    return df
