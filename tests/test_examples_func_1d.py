import pytest
from test_utils import run_script_and_get_fig

mpl_image_compare_kwargs = {
    "baseline_dir": "../docs/img",
    "savefig_kwargs": {"bbox_inches": "tight"},
    "style": "plothist.default_style",
    "deterministic": True,
}


@pytest.mark.mpl_image_compare(
    filename="fct_1d.png",
    **mpl_image_compare_kwargs,
)
def test_example_fct_1d():
    return run_script_and_get_fig("plothist.examples.func_1d.fct_1d")


@pytest.mark.mpl_image_compare(
    filename="fct_1d_stacked.png",
    **mpl_image_compare_kwargs,
)
def test_example_fct_1d_stacked():
    return run_script_and_get_fig("plothist.examples.func_1d.fct_1d_stacked")
