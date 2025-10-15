import tempfile
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pytest

from plothist import (
    create_comparison_figure,
    make_2d_hist,
    make_hist,
    plot_2d_hist,
    plot_2d_hist_with_projections,
    plot_data_model_comparison,
    plot_function,
    plot_model,
    plot_two_hist_comparison,
    savefig,
)
from plothist.plotters import _get_model_type


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
    h_2d = make_2d_hist(data=[[], []], bins=[10, 10], range=((0, 10), (0, 10)))

    msg = r"Need to provide fig, ax"

    with pytest.raises(ValueError, match=msg):
        plot_2d_hist(h_2d, fig=fig)

    with pytest.raises(ValueError, match=msg):
        plot_two_hist_comparison(h_1d, h_1d, fig=fig)

    with pytest.raises(ValueError, match=msg):
        plot_data_model_comparison(data_hist=h_1d, stacked_components=[h_1d], fig=fig)

    with pytest.raises(
        ValueError, match=r"Need to provide both fig and ax \(or none\)."
    ):
        plot_model(unstacked_components=[h_1d], fig=fig)


def test_plot_function_cases() -> None:
    """
    Test that plot_function can handle different cases that are not covered by the examples.
    """

    def f1(x):
        return x**2

    def f2(x):
        return x + 1

    # Case 1: Plotting multiple functions without stacking
    fig, ax = plt.subplots()
    plot_function(
        [
            f1,
            f2,
        ],
        range=(0, 10),
        ax=ax,
        stacked=False,
    )
    assert len(ax.lines) == 2
    plt.close(fig)

    # Case 2: Plotting a single function with stacking
    fig, ax = plt.subplots()
    plot_function(
        f1,
        range=(0, 10),
        ax=ax,
        stacked=True,
    )
    assert len(ax.collections) == 1
    plt.close(fig)


def test_plot_2d_hist_with_projections_cases() -> None:
    """
    Test that plot_2d_hist_with_projections can handle empty data and no input figure.
    """
    h_2d = make_2d_hist(data=[[], []], bins=[10, 10], range=((0, 10), (0, 10)))
    fig, _, _, _, _ = plot_2d_hist_with_projections(
        h_2d,
    )
    assert len(fig.axes) == 4  # Main plot + 2 projections + colorbar
    plt.close(fig)


def test_savefig_with_default_size() -> None:
    """Test that savefig works correctly without resizing the figure (new_figsize=None)."""
    fig, ax = plt.subplots()
    ax.plot([0, 1], [1, 0])

    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "default_size.png"
        savefig(fig, str(output_path))
        assert output_path.exists()
        # Confirm figure size is unchanged
        width, height = fig.get_size_inches()
        assert pytest.approx(width) == plt.rcParams["figure.figsize"][0]
        assert pytest.approx(height) == plt.rcParams["figure.figsize"][1]

    plt.close(fig)


def test_savefig_with_custom_size():
    """Test that savefig correctly rescales the figure when new_figsize is provided."""
    fig, ax = plt.subplots()
    ax.plot([0, 1], [1, 0])

    new_size = (10.0, 5.0)

    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "custom_size.png"
        savefig(fig, str(output_path), new_figsize=new_size)
        assert output_path.exists()
        assert output_path.stat().st_size > 0

        # Confirm figure was resized
        width, height = fig.get_size_inches()
        assert round(width, 2) == new_size[0]
        assert round(height, 2) == new_size[1]

    plt.close(fig)


def test_get_model_type() -> None:
    """
    Test the _get_model_type function with different model inputs.
    """

    def func(x):
        return x

    hist = make_hist(data=[1, 2, 3], bins=3, range=(0, 3))

    assert _get_model_type([func]) == "functions"

    assert _get_model_type([hist]) == "histograms"

    with pytest.raises(
        ValueError,
        match=r"All model components must be either histograms or functions.",
    ):
        _get_model_type([func, hist])


def test_plot_model_cases() -> None:
    """
    Test that plot_model can handle different cases that are not covered by the examples.
    """

    def f1(x):
        return x**2

    h_1d = make_hist(data=[1, 2, 3], bins=3, range=(0, 3))

    # Case 1: Plotting functions without labels
    fig, ax = plt.subplots()
    with pytest.warns(
        UserWarning, match=r"No artists with labels found to put in legend."
    ):
        fig, ax = plot_model(
            unstacked_components=[f1],
            function_range=(0, 10),
            fig=fig,
            ax=ax,
        )
    plt.close(fig)

    # Case 2: Plotting a model with  single unstacked histogram
    fig, ax = plt.subplots()
    fig, ax = plot_model(
        unstacked_components=[h_1d],
        fig=fig,
        ax=ax,
    )
    assert len(ax.patches) == 4
    plt.close(fig)

    # Case 3: Plotting a model without any components
    fig, ax = plt.subplots()
    with pytest.raises(
        ValueError, match=r"Need to provide at least one model component."
    ):
        plot_model(
            fig=fig,
            ax=ax,
        )
    plt.close(fig)

    # Case 4
    fig, ax = plt.subplots()
    with pytest.raises(
        ValueError, match=r"Need to provide function_range for model made of functions."
    ):
        plot_model(
            stacked_components=[f1],
            fig=fig,
            ax=ax,
        )
    plt.close(fig)


def test_plot_data_model_comparison_cases() -> None:
    """
    Test that plot_data_model_comparison can handle different cases that are not covered by the examples.
    """

    def func(x):
        return x

    h_1d = make_hist(data=[1, 2, 3], bins=3, range=(0, 3))

    # Case 1: No model components provided
    fig, ax = plt.subplots()
    with pytest.raises(
        ValueError, match=r"Need to provide at least one model component."
    ):
        plot_data_model_comparison(
            data_hist=h_1d,
            fig=fig,
            ax=ax,
        )
    plt.close(fig)

    # Case 2: Providing fig and ax_main or ax_comparison with plot_only
    fig, ax = plt.subplots()
    with pytest.raises(
        ValueError,
        match=r"Cannot provide fig, ax_main or ax_comparison with plot_only.",
    ):
        fig, (ax_main, ax_comparison) = create_comparison_figure()
        plot_data_model_comparison(
            data_hist=h_1d,
            stacked_components=[h_1d],
            fig=fig,
            ax_main=ax_main,
            ax_comparison=ax_comparison,
            plot_only="ax_main",
        )
    plt.close(fig)

    # Case 3: Not providing labels for model components in ax_main
    with pytest.warns(
        UserWarning, match=r"No artists with labels found to put in legend."
    ):
        fig, ax_main, _ = plot_data_model_comparison(
            data_hist=h_1d, stacked_components=[func], plot_only="ax_main"
        )
    plt.close(fig)

    # Case 4: Not providing labels for model components in ax_comparison
    with pytest.warns(
        UserWarning, match=r"No artists with labels found to put in legend."
    ):
        fig, _, ax_comparison = plot_data_model_comparison(
            data_hist=h_1d, stacked_components=[func], plot_only="ax_comparison"
        )
    plt.close(fig)

    # Case 5: Providing an invalid plot_only value
    with pytest.raises(
        ValueError, match=r"plot_only must be 'ax_main', 'ax_comparison' or None."
    ):
        plot_data_model_comparison(
            data_hist=h_1d, stacked_components=[func], plot_only="invalid"
        )
