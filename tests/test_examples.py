import subprocess
import pytest
import tempfile
import os

scripts = [
    "docs/examples/1d_func/1d_fct.py",
    "docs/examples/1d_func/1d_fct_stacked.py",
    "docs/examples/1d_hist/1d_comparison_asymmetry.py",
    "docs/examples/1d_hist/1d_comparison_difference.py",
    "docs/examples/1d_hist/1d_comparison_efficiency.py",
    "docs/examples/1d_hist/1d_comparison_only_efficiency.py",
    "docs/examples/1d_hist/1d_comparison_pull.py",
    "docs/examples/1d_hist/1d_comparison_ratio.py",
    "docs/examples/1d_hist/1d_comparison_relative_difference.py",
    "docs/examples/1d_hist/1d_comparison_split_ratio.py",
    "docs/examples/1d_hist/1d_elt1.py",
    "docs/examples/1d_hist/1d_elt1_stacked.py",
    "docs/examples/1d_hist/1d_elt2.py",
    "docs/examples/1d_hist/1d_hist_simple.py",
    "docs/examples/1d_hist/1d_int_category.py",
    "docs/examples/1d_hist/1d_profile.py",
    "docs/examples/1d_hist/1d_side_by_side.py",
    "docs/examples/1d_hist/1d_str_category.py",
    "docs/examples/2d_hist/2d_hist_correlations.py",
    "docs/examples/2d_hist/2d_hist_simple_discrete_colormap.py",
    "docs/examples/2d_hist/2d_hist_simple.py",
    "docs/examples/2d_hist/2d_hist_uneven.py",
    "docs/examples/2d_hist/2d_hist_with_projections.py",
    "docs/examples/advanced/1d_comparison_advanced.py",
    "docs/examples/advanced/1d_side_by_side_with_numbers.py",
    "docs/examples/advanced/asymmetry_comparison_advanced.py",
    "docs/examples/advanced/model_examples_flatten2D.py",
    "docs/examples/model_ex/model_all_comparisons_no_model_unc.py",
    "docs/examples/model_ex/model_all_comparisons.py",
    "docs/examples/model_ex/model_examples_pull_no_model_unc.py",
    "docs/examples/model_ex/model_examples_pull.py",
    "docs/examples/model_ex/model_examples_stacked.py",
    "docs/examples/model_ex/model_examples_stacked_unstacked.py",
    "docs/examples/model_ex/model_examples_unstacked.py",
    "docs/examples/model_ex/model_with_stacked_and_unstacked_function_components.py",
    "docs/examples/model_ex/model_with_stacked_and_unstacked_histograms_components.py",
    "docs/examples/model_ex/ratio_data_vs_model_with_stacked_and_unstacked_function_components.py",
    "docs/examples/utility/add_text_example.py",
    "docs/examples/utility/color_palette_hists.py",
    "docs/examples/utility/color_palette_squares.py",
    "docs/examples/utility/matplotlib_vs_plothist_style.py",
]

@pytest.mark.parametrize("script", scripts)
def test_examples(script):
    with tempfile.TemporaryDirectory() as tmpdirname:
        os.cd(tmpdirname)
        result = subprocess.run(["python", script], capture_output=True, text=True, env=env)
        assert result.returncode == 0, f"Script {script} failed with error: {result.stderr}"