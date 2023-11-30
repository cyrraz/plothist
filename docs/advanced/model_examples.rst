.. _advanced-model_examples-label:

========================
Plotting models and data
========================

The examples below make use of a pandas dataframe ``df`` containing dummy data, that can be generated with:

.. code-block:: python

    from plothist.generate_dummy_data import generate_dummy_data
    df = generate_dummy_data()


Creating the data and model
===========================

Below is the code that generates the data and model histograms used in all the examples below. The idea is to have a ``data_hist`` corresponding to any kind of data representing a count of events over a variable, a ``signal_hist`` corresponding to the signal model, and a list of ``background_hists`` used to model to everything that is not our signal. We also show an example of how to scale the model to the data. We also define three functions that will be used as model components.

.. code-block:: python

    from plothist import make_hist, get_color_palette

    # Define the histograms

    key = "variable_1"
    range = [-9, 12]
    category = "category"

    # Define masks
    signal_mask = df[category] == 7
    data_mask = df[category] == 8

    background_categories = [0, 1, 2]
    background_categories_labels = [f"c{i}" for i in background_categories]
    background_categories_colors = get_color_palette("cubehelix", len(background_categories))

    background_masks = [df[category] == p for p in background_categories]

    # Make histograms
    data_hist = make_hist(df[key][data_mask], bins=50, range=range, weights=1)
    background_hists = [
        make_hist(df[key][mask], bins=50, range=range, weights=1)
        for mask in background_masks
    ]
    signal_hist = make_hist(df[key][signal_mask], bins=50, range=range, weights=1)

    # Optional: scale to data
    background_scaling_factor = data_hist.sum().value / sum(background_hists).sum().value
    background_hists = [background_scaling_factor * h for h in background_hists]

    signal_scaling_factor = data_hist.sum().value / signal_hist.sum().value
    signal_hist *= signal_scaling_factor


    from scipy.stats import norm

    # Define some random functions that will be used as model components with functions
    def f_signal(x):
        return 1000*norm.pdf(x, loc=0.5, scale=3)
    def f_background1(x):
        return 1000*norm.pdf(x, loc=-1.5, scale=4)
    def f_background2(x):
        return 3000*norm.pdf(x, loc=-1.8, scale=1.8)



Simple model plots
==================

If you want to plot only the model, use ``plot_model()``. It supports models made of functions or histograms. Stacked and unstacked components can be combined. The sum will always be the sum of all the components, stacked and unstacked.

It can take a lot more arguments to customize the plot than shown in the examples below, see the documentation for more details.

Histograms
----------

Here is an example with a model above made of histograms:

.. code-block:: python

    from plothist import plot_model, add_luminosity, add_text

    fig, ax = plot_model(
        stacked_components=background_hists,
        stacked_labels=background_categories_labels,
        stacked_colors=background_categories_colors,
        unstacked_components=[signal_hist],
        unstacked_labels=["Signal"],
        unstacked_colors=["black"],
        unstacked_kwargs_list=[{"linestyle": "dotted"}],
        xlabel=key,
        ylabel="Entries",
        model_sum_kwargs={"show": True, "label": "Model", "color": "navy"},
        model_uncertainty_label="Stat. unc.",
    )

    add_text("Model made of histograms", ax=ax)

    add_luminosity(collaboration="Beast III", ax=ax, preliminary=True, is_data=False)

    fig.savefig("model_with_stacked_and_unstacked_histograms_components.svg", bbox_inches='tight')

.. image:: ../img/model_with_stacked_and_unstacked_histograms_components.svg
   :alt: Plot of a model with stacked and unstacked histograms components
   :width: 500


Functions
---------

Here is an example with a model above made of functions:

.. code-block:: python

    from plothist import plot_model, add_luminosity, add_text

    fig, ax = plot_model(
        stacked_components=[f_background1, f_background2],
        stacked_labels=background_categories_labels[:2],
        unstacked_components=[f_signal],
        unstacked_labels=["Signal"],
        unstacked_colors=["black"],
        xlabel=key,
        ylabel=f"f({key})",
        model_sum_kwargs={"show": True, "label": "Model", "color": "navy"},
        function_range=[-9,12],
    )

    add_text("Model made of functions", ax=ax)

    add_luminosity(collaboration="Beast III", ax=ax, is_data=False)

    fig.savefig("model_with_stacked_and_unstacked_function_component.svg", bbox_inches='tight')

.. image:: ../img/model_with_stacked_and_unstacked_function_components.svg
   :alt: Plot of a model with stacked and unstacked function components
   :width: 500



Compare data and model
======================

A data histogram can be added to the plot with ``plot_data_model_comparison()``. It will then compare the sum of the components to the data, witht the comparison of your choice. The default comparison is the ratio between the model and the data. It can take any comparison method available in ``plot_comparison()``. If the events are unweighted, data uncertainties will always be asymmetrical.

Stacked histograms
------------------

An example with stacked histograms:

.. code-block:: python

    from plothist import plot_data_model_comparison, plot_hist, add_luminosity

    fig, ax_main, ax_comparison = plot_data_model_comparison(
        data_hist=data_hist,
        stacked_components=background_hists,
        stacked_labels=background_categories_labels,
        stacked_colors=background_categories_colors,

        xlabel=key,
        ylabel="Entries",
    )

    # Signal histogram not part of the model and therefore not included in the comparison
    plot_hist(
        signal_hist,
        ax=ax_main,
        color="red",
        label="Signal",
        histtype="step",
    )

    ax_main.legend()

    add_luminosity(collaboration="Beast III", ax=ax_main, lumi=200, preliminary=True)

    fig.savefig("hep_examples_dataMC_stacked.svg", bbox_inches='tight')


.. image:: ../img/hep_examples_dataMC_stacked.svg
   :alt: Data/model comparison, stacked plot
   :width: 500


Unstacked histograms
--------------------

Unstacked histogram:

.. code-block:: python

    from plothist import plot_data_model_comparison, plot_hist, add_luminosity

    fig, ax_main, ax_comparison = plot_data_model_comparison(
        data_hist=data_hist,
        unstacked_components=background_hists,
        unstacked_labels=background_categories_labels,
        unstacked_colors=background_categories_colors,
        xlabel=key,
        ylabel="Entries",
        model_sum_kwargs={"label":"Sum(MC)", "color": "navy"},
        comparison_ylim=[0.5, 1.5],
    )

    ax_main.legend()

    add_luminosity(collaboration="Beast III", ax=ax_main, lumi=50, lumi_unit="zb")

    fig.savefig("hep_examples_dataMC_unstacked.svg", bbox_inches='tight')


.. image:: ../img/hep_examples_dataMC_unstacked.svg
   :alt: Data/model comparison, stacked plot
   :width: 500


Stacked and unnstacked histograms
---------------------------------

Stacked and unstacked histograms can be combined:

.. code-block:: python

    from plothist import plot_data_model_comparison, add_luminosity

    fig, ax_main, ax_comparison = plot_data_model_comparison(
        data_hist=data_hist,
        stacked_components=background_hists[:2],
        stacked_labels=background_categories_labels[:2],
        stacked_colors=background_categories_colors[:2],
        unstacked_components=background_hists[2:],
        unstacked_labels=background_categories_labels[2:],
        unstacked_colors=background_categories_colors[2:],
        xlabel=key,
        ylabel="Entries",
        model_sum_kwargs={"show": True, "label": "Sum(MC)", "color": "navy"},
        comparison_ylim=(0.5, 1.5),
    )

    add_luminosity(collaboration="Beast III", ax=ax_main, lumi=50, lumi_unit="zb")

    fig.savefig("hep_examples_dataMC_stacked_unstacked.svg", bbox_inches='tight')

.. image:: ../img/hep_examples_dataMC_stacked_unstacked.svg
   :alt: Data/model comparison, stacked and unstacked plot with histograms
   :width: 500

Models made of functions
------------------------

The function ``plot_data_model_comparison()`` can also be used to compare data and functions:

.. code-block:: python

    from plothist import plot_data_model_comparison

    fig, ax_main, ax_comparison = plot_data_model_comparison(
        data_hist=data_hist,
        stacked_components=[f_background1, f_background2],
        stacked_labels=["c0", "c1"],
        unstacked_components=[f_signal],
        unstacked_labels=["Signal"],
        unstacked_colors=["#8EBA42"],
        xlabel=key,
        ylabel="Entries",
        model_sum_kwargs={"show": True, "label": "Model", "color": "navy"},
        comparison="pull"
    )

    add_luminosity(collaboration="Beast III", ax=ax_main, lumi=50, lumi_unit="zb")

    fig.savefig("ratio_data_vs_model_with_stacked_and_unstacked_function_components.svg", bbox_inches='tight')

.. image:: ../img/ratio_data_vs_model_with_stacked_and_unstacked_function_components.svg
   :alt: Data/Model comparison, model with stacked and unstacked function components
   :width: 500


Model uncertainty
-----------------

As said ealier, the comparison function can take any comparison method available in ``plot_comparison()``. To use pulls instead of the ratio to compare the histograms:

.. code-block:: python

    from plothist import plot_data_model_comparison, add_luminosity

    fig, ax_main, ax_comparison = plot_data_model_comparison(
        data_hist=data_hist,
        stacked_components=background_hists,
        stacked_labels=background_categories_labels,
        stacked_colors=background_categories_colors,
        xlabel=f"${key}\,\,[TeV/c^2]$",
        ylabel="Candidates per 0.42 $TeV/c^2$",
        comparison="pull",
    )

    add_luminosity(collaboration="Beast III", ax=ax_main, lumi="(1 + 0.74)", lumi_unit="ab")

    fig.savefig("hep_examples_dataMC_pull.svg", bbox_inches='tight')


.. image:: ../img/hep_examples_dataMC_pull.svg
   :alt: Data/model comparison with pull, stacked plot
   :width: 500


Now, if you do not want to show and take into account the model uncertainties, setting ``model_uncertainty`` to ``False`` remove them and updates the definition of the pulls:

.. code-block:: python

    from plothist import plot_data_model_comparison, add_luminosity

    fig, ax_main, ax_comparison = plot_data_model_comparison(
        data_hist=data_hist,
        stacked_components=background_hists,
        stacked_labels=background_categories_labels,
        stacked_colors=background_categories_colors,
        xlabel=f"${key}\,\,[eV/c^2]$",
        ylabel="Hits in the LMN per $4.2\\times 10^{-1}\,\,eV/c^2$",
        comparison="pull",
        model_uncertainty=False # <--
    )
    add_luminosity(collaboration="Beast III", ax=ax_main, lumi=8.2, lumi_unit="zb", preliminary=True)

    fig.savefig("hep_examples_dataMC_pull_no_MC_stat_unc.svg", bbox_inches='tight')


.. image:: ../img/hep_examples_dataMC_pull_no_MC_stat_unc.svg
   :alt: Data/model comparison with pull, no model stat. unc., stacked plot
   :width: 500



Comparison overview
===================

Here are a series of examples showing complex plots resuming all the possible comparisons between data and model. The idea is to show how to use ``plot_comparison()`` and ``plot_data_model_comparison()`` to make the plots shown in the examples below. The plots are a bit more complex than the ones shown above, but the code to produce them is still quite simple.


All the different comparisons
-----------------------------

Below is shown how to make a plot with all the possible comparisons between data and model. The idea is to use ``plot_data_model_comparison()`` to make the plot with the ratio comparison, and then use ``plot_comparison()`` to add the other comparisons. The ``plot_comparison()`` function can take a ``fig`` and ``ax`` argument to add the comparison to an existing figure. The ``plot_data_model_comparison()`` function returns the figure and axes used to make the plot, so we can use them to add the other comparisons.

.. code-block:: python

    from plothist import (
        create_comparison_figure,
        plot_data_model_comparison,
        add_text,
        set_fitting_ylabel_fontsize,
        plot_comparison
    )
    import matplotlib.pyplot as plt

    fig, axes = create_comparison_figure(
        figsize=(6, 11),
        nrows=5,
        gridspec_kw={"height_ratios": [3.3, 1, 1, 1, 1]},
        hspace=0.3,
    )
    background_sum = sum(background_hists)

    fig, ax_main, ax_comparison = plot_data_model_comparison(
            data_hist=data_hist,
            stacked_components=background_hists,
            stacked_labels=background_categories_labels,
            stacked_colors=background_categories_colors,
            xlabel="",
            ylabel="Entries",
            comparison="ratio",
            fig=fig,
            ax_main=axes[0],
            ax_comparison=axes[1],
        )

    add_text(f'  $\mathbf{{→}}$ comparison = "ratio"', ax=ax_comparison, fontsize=13)

    for k_comp, comparison in enumerate(["pull", "relative_difference", "difference"], start=2):

        ax_comparison = axes[k_comp]

        plot_comparison(
            data_hist,
            background_sum,
            ax=ax_comparison,
            comparison=comparison,
            xlabel="",
            h1_label="Data",
            h2_label="Pred.",
            ratio_uncertainty="split",
            hist_1_uncertainty="asymmetrical",
        )
        add_text(f'  $\mathbf{{→}}$ comparison = "{comparison}"', ax=ax_comparison, fontsize=13)
        set_fitting_ylabel_fontsize(ax_comparison)

    axes[-1].set_xlabel(key)

    fig.savefig("hep_all_comparisons.svg", bbox_inches="tight")


.. image:: ../img/hep_all_comparisons.svg
   :alt: Data/model comparison with all comparisons, stacked plot
   :width: 500


No model uncertainties
----------------------


Same example plot but we remove the statistical uncertainties of the model by adding ``model_uncertainty=False`` in ``plot_data_model_comparison()`` and pass a model histogram without uncertainties to ``plot_comparison()``:

.. code-block:: python

    from plothist import (
        create_comparison_figure,
        plot_data_model_comparison,
        add_text,
        set_fitting_ylabel_fontsize,
        plot_comparison
    )
    import matplotlib.pyplot as plt
    import numpy as np

    fig, axes = create_comparison_figure(
        figsize=(6, 11),
        nrows=5,
        gridspec_kw={"height_ratios": [3.3, 1, 1, 1, 1]},
        hspace=0.3,
    )
    background_sum = sum(background_hists)

    fig, ax_main, ax_comparison = plot_data_model_comparison(
            data_hist=data_hist,
            stacked_components=background_hists,
            stacked_labels=background_categories_labels,
            stacked_colors=background_categories_colors,
            xlabel="",
            ylabel="Entries",
            model_uncertainty=False, # <--
            comparison="ratio",
            fig=fig,
            ax_main=axes[0],
            ax_comparison=axes[1],
        )

    add_text(f'  $\mathbf{{→}}$ comparison = "ratio"', ax=ax_comparison, fontsize=13)

    for k_comp, comparison in enumerate(["pull", "relative_difference", "difference"], start=2):

        ax_comparison = axes[k_comp]

        # Copy the original histogram and set the uncertainties of the copy to 0.
        background_sum_copy = background_sum.copy()
        background_sum_copy[:] = np.c_[
        background_sum_copy.values(), np.zeros_like(background_sum_copy.values())
        ]

        plot_comparison(
            data_hist,
            background_sum_copy,
            ax=ax_comparison,
            comparison=comparison,
            xlabel="",
            h1_label="Data",
            h2_label="Pred.",
            ratio_uncertainty="split",
            hist_1_uncertainty="asymmetrical",
        )
        if comparison == "pull":
            # Since the uncertainties of the model are neglected, the pull label is "(Data - Pred.)/sigma_Data"
            ax_comparison.set_ylabel(r"$\frac{Data-Pred.}{\sigma_{Data}}$")
        add_text(f'  $\mathbf{{→}}$ comparison = "{comparison}"', ax=ax_comparison, fontsize=13)
        set_fitting_ylabel_fontsize(ax_comparison)

    axes[-1].set_xlabel(key)

    fig.savefig("hep_all_comparisons_no_stat_MC_unc.svg", bbox_inches="tight")



.. image:: ../img/hep_all_comparisons_no_stat_MC_unc.svg
   :alt: Data/model comparison with all comparisons, no model uncertainties, stacked plot
   :width: 500


Ratio options
-------------

For ``ratio`` or ``relative_difference``, the uncertainties can be split between model and data (default option) or both can be added to the ratio uncertainty (``ratio_uncertainty="uncorrelated"``). Here are all the possible options:

.. code-block:: python

    from plothist import (
        create_comparison_figure,
        plot_data_model_comparison,
        add_text,
        set_fitting_ylabel_fontsize,
        plot_comparison
    )
    import numpy as np
    import matplotlib.pyplot as plt

    fig, axes = create_comparison_figure(
        figsize=(6, 11),
        nrows=5,
        gridspec_kw={"height_ratios": [3.3, 1, 1, 1, 1]},
        hspace=0.3,
    )

    background_sum = sum(background_hists)

    fig, ax_main, ax_comparison = plot_data_model_comparison(
            data_hist=data_hist,
            stacked_components=background_hists,
            stacked_labels=background_categories_labels,
            stacked_colors=background_categories_colors,
            xlabel="",
            ylabel="Entries",
            comparison="ratio",
            ratio_uncertainty="split",
            fig=fig,
            ax_main=axes[0],
            ax_comparison=axes[1],
        )

    add_text(
        f'  $\mathbf{{→}}$ comparison = "ratio", \n  $\mathbf{{→}}$ ratio_uncertainty="split", model_uncertainty = True',
        ax=ax_comparison,
        fontsize=10,
    )

    for k_comp, (ratio_uncertainty, model_uncertainty) in enumerate([
        ("uncorrelated", True),
        ("split", False),
        ("uncorrelated", False),
        ], start=2):

        ax_comparison = axes[k_comp]

        # When the uncertainties on the model are neglected, copy the original histogram and set the uncertainties of the copy to 0.
        background_sum_copy = background_sum.copy()
        if not model_uncertainty:
            background_sum_copy[:] = np.c_[
            background_sum_copy.values(), np.zeros_like(background_sum_copy.values())
        ]

        plot_comparison(
            data_hist,
            background_sum_copy,
            ax=ax_comparison,
            comparison="ratio",
            xlabel="",
            h1_label="Data",
            h2_label="Pred.",
            ratio_uncertainty=ratio_uncertainty,
            hist_1_uncertainty="asymmetrical",
        )
        add_text(
            f'  $\mathbf{{→}}$ comparison = "ratio", \n  $\mathbf{{→}}$ ratio_uncertainty="{ratio_uncertainty}", model_uncertainty = {model_uncertainty}',
            ax=ax_comparison,
            fontsize=10,
        )
        set_fitting_ylabel_fontsize(ax_comparison)

    axes[-1].set_xlabel(key)

    fig.savefig("hep_comparisons_ratio_options.svg", bbox_inches="tight")



.. image:: ../img/hep_comparisons_ratio_options.svg
   :alt: Data/model comparison with all comparisons option for ratio
   :width: 500


Advanced
========

Flatten 2D variable
-------------------

Compare data and stacked histogram for a flatten 2D variable:

.. code-block:: python

    from plothist import (
        make_2d_hist,
        get_color_palette,
        plot_data_model_comparison,
        add_luminosity,
        flatten_2d_hist,
        plot_hist
    )

    # Define the histograms

    key1 = "variable_1"
    key2 = "variable_2"
    # Bins [-10,0], [0,10] for variable 1,
    # and bins [-10,-5], [-5,0], [0,5], [5,10] for variable 2
    bins = [[-10, 0, 10], [-10, -5, 0, 5, 10]]
    category = "category"

    # Define datasets

    signal_mask = df[category] == 7
    data_mask = df[category] == 8

    background_categories = [0, 1, 2, 3, 4, 5, 6]
    background_categories_labels = [f"c{i}" for i in background_categories]
    background_categories_colors = get_color_palette("cubehelix", len(background_categories))

    background_masks = [df[category] == p for p in background_categories]

    # Make histograms

    data_hist = make_2d_hist(
        [df[key][data_mask] for key in [key1, key2]], bins=bins, weights=1
    )
    background_hists = [
        make_2d_hist([df[key][mask] for key in [key1, key2]], bins=bins, weights=1)
        for mask in background_masks
    ]
    signal_hist = make_2d_hist(
        [df[key][signal_mask] for key in [key1, key2]], bins=bins, weights=1
    )

    # Flatten the 2D histograms
    data_hist = flatten_2d_hist(data_hist)
    background_hists = [flatten_2d_hist(h) for h in background_hists]
    signal_hist = flatten_2d_hist(signal_hist)

    # Compare data and stacked histogram
    fig, ax_main, ax_comparison = plot_data_model_comparison(
        data_hist=data_hist,
        stacked_components=background_hists,
        stacked_labels=background_categories_labels,
        stacked_colors=background_categories_colors,
        xlabel=rf"({key1} $\times$ {key2}) bin",
        ylabel="Entries",
    )

    plot_hist(
        signal_hist,
        ax=ax_main,
        color="red",
        label="Signal",
        histtype="step",
    )

    add_luminosity(collaboration="Beast III", ax=ax_main, lumi=50, lumi_unit="zb")
    ax_main.legend(ncol=3, fontsize=10, loc="upper left")

    fig.savefig("hep_examples_dataMC_flatten2D.svg", bbox_inches='tight')


.. image:: ../img/hep_examples_dataMC_flatten2D.svg
   :alt: Data/model comparison, flatten variable
   :width: 500

