import matplotlib.pyplot as plt
import numpy as np
import pytest

from plothist import (
    create_comparison_figure,
    make_2d_hist,
    make_hist,
    plot_2d_hist,
    plot_data_model_comparison,
    plot_two_hist_comparison,
)


def test_create_comparison_figure_figsize_none() -> None:
    """
    Test that when figsize=None is passed, the function uses matplotlib's default figure size
    from rcParams["figure.figsize"].
    """
    default_figsize = plt.rcParams["figure.figsize"]
    fig, _ = create_comparison_figure(figsize=None)
    np.testing.assert_array_almost_equal(
        fig.get_size_inches(),
        default_figsize,
        decimal=5,
    )
    plt.close(fig)


def test_partial_fig_and_ax_input() -> None:
    """
    Test that the function can handle partial fig and ax.
    """
    fig, _ = plt.subplots()
    h_1d = make_hist(data=[], bins=10, range=(0, 10))
    h_2d = make_2d_hist(data=[[], []], bins=[10, 10], range=[[0, 10], [0, 10]])

    msg = r"Need to provide fig, ax"

    with pytest.raises(ValueError, match=msg):
        _ = plot_2d_hist(h_2d, fig=fig)

    with pytest.raises(ValueError, match=msg):
        _ = plot_two_hist_comparison(h_1d, h_1d, fig=fig)

    with pytest.raises(ValueError, match=msg):
        _ = plot_data_model_comparison(
            data_hist=h_1d, stacked_components=[h_1d], fig=fig
        )
