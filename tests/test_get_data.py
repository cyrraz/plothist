from __future__ import annotations


def test_get_data():
    """
    Test get dummy data.
    """
    import numpy as np
    from plothist_utils import get_dummy_data

    data = get_dummy_data()

    assert data is not None
    assert len(data) == 100000
    assert all(len(row) == 4 for row in data)

    assert all(isinstance(value, float) for row in data for value in row)
    assert all(np.isfinite(value) for row in data for value in row)

    assert data.dtype.names == ("variable_0", "variable_1", "variable_2", "category")
    assert list(data[0]) == [
        np.float64(3.1610415998797303),
        np.float64(0.626420790702924),
        np.float64(-0.31548195431435616),
        np.float64(2.0),
    ]
    assert list(data[-1]) == [
        np.float64(5.00154509363355),
        np.float64(-1.8741787404723926),
        np.float64(-1.309310906826642),
        np.float64(2.0),
    ]
