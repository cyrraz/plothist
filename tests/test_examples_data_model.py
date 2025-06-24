import pytest
from plothist_utils import get_dummy_data

from plothist import get_color_palette, make_hist

mpl_image_compare_kwargs = {
    "baseline_dir": "../docs/img",
    "savefig_kwargs": {"bbox_inches": "tight"},
    "style": "plothist.default_style",
    "deterministic": True,
}


@pytest.fixture
def histograms():
    df = get_dummy_data()

    # Define the histograms

    key = "variable_1"
    range = [-9, 12]
    category = "category"

    # Define masks
    signal_mask = df[category] == 7
    data_mask = df[category] == 8

    background_categories = [0, 1, 2]
    background_categories_labels = [f"c{i}" for i in background_categories]
    background_categories_colors = get_color_palette(
        "cubehelix", len(background_categories)
    )

    background_masks = [df[category] == p for p in background_categories]

    # Make histograms
    data_hist = make_hist(df[key][data_mask], bins=50, range=range, weights=1)
    background_hists = [
        make_hist(df[key][mask], bins=50, range=range, weights=1)
        for mask in background_masks
    ]
    signal_hist = make_hist(df[key][signal_mask], bins=50, range=range, weights=1)

    # Optional: scale to data
    background_scaling_factor = (
        data_hist.sum().value / sum(background_hists).sum().value
    )
    background_hists = [background_scaling_factor * h for h in background_hists]

    signal_scaling_factor = data_hist.sum().value / signal_hist.sum().value
    signal_hist *= signal_scaling_factor

    return (
        data_hist,
        signal_hist,
        background_hists,
        background_categories_labels,
        background_categories_colors,
    )


@pytest.mark.mpl_image_compare(
    filename="model_all_comparisons_no_model_unc.png",
    **mpl_image_compare_kwargs,
)
def test_model_all_comparisons_no_model_unc(histograms):
    from plothist.examples.model_ex.model_all_comparisons_no_model_unc import (
        make_figure,
    )

    (
        data_hist,
        _,
        background_hists,
        background_categories_labels,
        background_categories_colors,
    ) = histograms

    return make_figure(
        data_hist,
        background_hists,
        background_categories_labels,
        background_categories_colors,
    )


@pytest.mark.mpl_image_compare(
    filename="model_all_comparisons.png",
    **mpl_image_compare_kwargs,
)
def test_model_all_comparisons(histograms):
    from plothist.examples.model_ex.model_all_comparisons import make_figure

    (
        data_hist,
        _,
        background_hists,
        background_categories_labels,
        background_categories_colors,
    ) = histograms

    return make_figure(
        data_hist,
        background_hists,
        background_categories_labels,
        background_categories_colors,
    )


@pytest.mark.mpl_image_compare(
    filename="model_examples_pull_no_model_unc.png",
    **mpl_image_compare_kwargs,
)
def test_model_examples_pull_no_model_unc(histograms):
    from plothist.examples.model_ex.model_examples_pull_no_model_unc import make_figure

    (
        data_hist,
        _,
        background_hists,
        background_categories_labels,
        background_categories_colors,
    ) = histograms

    return make_figure(
        data_hist,
        background_hists,
        background_categories_labels,
        background_categories_colors,
    )


@pytest.mark.mpl_image_compare(
    filename="model_examples_pull.png",
    **mpl_image_compare_kwargs,
)
def test_model_examples_pull(histograms):
    from plothist.examples.model_ex.model_examples_pull import make_figure

    (
        data_hist,
        _,
        background_hists,
        background_categories_labels,
        background_categories_colors,
    ) = histograms

    return make_figure(
        data_hist,
        background_hists,
        background_categories_labels,
        background_categories_colors,
    )


@pytest.mark.mpl_image_compare(
    filename="model_examples_stacked.png",
    **mpl_image_compare_kwargs,
)
def test_example_model_stacked(histograms):
    from plothist.examples.model_ex.model_examples_stacked import make_figure

    (
        data_hist,
        signal_hist,
        background_hists,
        background_categories_labels,
        background_categories_colors,
    ) = histograms

    return make_figure(
        data_hist,
        signal_hist,
        background_hists,
        background_categories_labels,
        background_categories_colors,
    )


@pytest.mark.mpl_image_compare(
    filename="model_examples_stacked_unstacked.png",
    **mpl_image_compare_kwargs,
)
def test_example_model_stacked_unstacked(histograms):
    from plothist.examples.model_ex.model_examples_stacked_unstacked import make_figure

    (
        data_hist,
        _,
        background_hists,
        background_categories_labels,
        background_categories_colors,
    ) = histograms

    return make_figure(
        data_hist,
        background_hists,
        background_categories_labels,
        background_categories_colors,
    )


@pytest.mark.mpl_image_compare(
    filename="model_examples_unstacked.png",
    **mpl_image_compare_kwargs,
)
def test_example_model_unstacked(histograms):
    from plothist.examples.model_ex.model_examples_unstacked import make_figure

    (
        data_hist,
        _,
        background_hists,
        background_categories_labels,
        background_categories_colors,
    ) = histograms

    return make_figure(
        data_hist,
        background_hists,
        background_categories_labels,
        background_categories_colors,
    )
