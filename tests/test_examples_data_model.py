import pytest
from test_utils import run_script_and_get_fig

mpl_image_compare_kwargs = {
    "baseline_dir": "../docs/img",
    "savefig_kwargs": {"bbox_inches": "tight"},
    "style": "plothist.default_style",
    "deterministic": True,
}


@pytest.mark.mpl_image_compare(
    filename="model_all_comparisons_no_model_unc.png",
    **mpl_image_compare_kwargs,
)
def test_model_all_comparisons_no_model_unc():
    return run_script_and_get_fig(
        "plothist.examples.model_ex.model_all_comparisons_no_model_unc"
    )


@pytest.mark.mpl_image_compare(
    filename="model_all_comparisons.png",
    **mpl_image_compare_kwargs,
)
def test_model_all_comparisons():
    return run_script_and_get_fig("plothist.examples.model_ex.model_all_comparisons")


@pytest.mark.mpl_image_compare(
    filename="model_examples_pull_no_model_unc.png",
    **mpl_image_compare_kwargs,
)
def test_model_examples_pull_no_model_unc():
    return run_script_and_get_fig(
        "plothist.examples.model_ex.model_examples_pull_no_model_unc"
    )


@pytest.mark.mpl_image_compare(
    filename="model_examples_pull.png",
    **mpl_image_compare_kwargs,
)
def test_model_examples_pull():
    return run_script_and_get_fig("plothist.examples.model_ex.model_examples_pull")


@pytest.mark.mpl_image_compare(
    filename="model_examples_stacked_unstacked.png",
    **mpl_image_compare_kwargs,
)
def test_example_model_stacked_unstacked():
    return run_script_and_get_fig(
        "plothist.examples.model_ex.model_examples_stacked_unstacked"
    )


@pytest.mark.mpl_image_compare(
    filename="model_examples_stacked.png",
    **mpl_image_compare_kwargs,
)
def test_example_model_stacked():
    return run_script_and_get_fig("plothist.examples.model_ex.model_examples_stacked")


@pytest.mark.mpl_image_compare(
    filename="model_examples_unstacked.png",
    **mpl_image_compare_kwargs,
)
def test_example_model_unstacked():
    return run_script_and_get_fig("plothist.examples.model_ex.model_examples_unstacked")


@pytest.mark.mpl_image_compare(
    filename="model_with_stacked_and_unstacked_function_components.png",
    **mpl_image_compare_kwargs,
)
def test_example_model_with_stacked_and_unstacked_function_components():
    return run_script_and_get_fig(
        "plothist.examples.model_ex.model_with_stacked_and_unstacked_function_components"
    )


@pytest.mark.mpl_image_compare(
    filename="model_with_stacked_and_unstacked_histograms_components.png",
    **mpl_image_compare_kwargs,
)
def test_example_model_with_stacked_and_unstacked_histograms_components():
    return run_script_and_get_fig(
        "plothist.examples.model_ex.model_with_stacked_and_unstacked_histograms_components"
    )


@pytest.mark.mpl_image_compare(
    filename="ratio_data_vs_model_with_stacked_and_unstacked_function_components.png",
    **mpl_image_compare_kwargs,
)
def test_example_ratio_data_vs_model_with_stacked_and_unstacked_function_components():
    return run_script_and_get_fig(
        "plothist.examples.model_ex.ratio_data_vs_model_with_stacked_and_unstacked_function_components"
    )
