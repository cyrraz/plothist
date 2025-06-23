import pytest

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
def test_plot_ttt():
    from plothist.examples.func_1d.fct_1d import make_figure

    return make_figure()
