.. _advanced-model_examples-label:

=======================
Plotting model and data
=======================

The examples below make use of a numpy ndarray ``df`` containing dummy data (you may also use a pandas dataframe), that can be loaded with:

.. code-block:: python

    from plothist import get_dummy_data

    df = get_dummy_data()

.. note::
   This page presents functions of ``plothist`` step by step and gives information about how to use them.
   To reproduce the examples, please visit the `plot gallery <https://plothist.readthedocs.io/en/latest/example_gallery/>`_, because it contains a standalone script for each example, that you can run directly.


Creating the data and model
===========================

Below is the code that generates the data and model histograms used in all the examples of this section. The idea is to have a ``data_hist`` corresponding to any kind of data representing a count of entries for a variable, a ``signal_hist`` corresponding to the signal model, and a list of ``background_hists`` used to model everything that is not the signal. We also show an example of how to scale the model to the data. We also define three functions that will be used as model components.

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
    background_scaling_factor = data_hist.sum().value / sum(background_hists).sum().value
    background_hists = [background_scaling_factor * h for h in background_hists]

    signal_scaling_factor = data_hist.sum().value / signal_hist.sum().value
    signal_hist *= signal_scaling_factor


    # Define some random functions that will be used as model components with functions
    from scipy.stats import norm


    def f_signal(x):
        return 1000 * norm.pdf(x, loc=0.5, scale=3)


    def f_background1(x):
        return 1000 * norm.pdf(x, loc=-1.5, scale=4)


    def f_background2(x):
        return 3000 * norm.pdf(x, loc=-1.8, scale=1.8)



Simple model plots
==================

If you want to plot only the model, use :func:`plot_model() <plothist.plotters.plot_model>`. It supports models made of functions or histograms. Stacked and unstacked components can be combined. The sum will always be the sum of all the components, stacked and unstacked.

It can take a lot more arguments to customize the plot than shown in the examples below, see the :ref:`documentation-label` for more details.

Histograms
----------

Here is an example with a model made of histograms:

.. literalinclude:: ../examples/model_ex/model_with_stacked_and_unstacked_histograms_components.py
    :language: python
    :start-after: ###

.. image:: ../img/model_with_stacked_and_unstacked_histograms_components.svg
   :alt: Plot of a model with stacked and unstacked histograms components
   :width: 500


Functions
---------

Here is an example with a model made of functions:

.. literalinclude:: ../examples/model_ex/model_with_stacked_and_unstacked_function_components.py
    :language: python
    :start-after: ###

.. image:: ../img/model_with_stacked_and_unstacked_function_components.svg
   :alt: Plot of a model with stacked and unstacked function components
   :width: 500


.. _advanced-model_comparison-label:
Compare data and model
======================

A data histogram can be added to the plot with :func:`plot_data_model_comparison() <plothist.plotters.plot_data_model_comparison>`. It will then compare the sum of the components to the data, with the comparison of your choice. The default comparison is the ratio between the model and the data. It can take any comparison method available in :func:`plot_comparison() <plothist.plotters.plot_comparison>`.

Stacked histograms
------------------

An example with stacked histograms:

.. literalinclude:: ../examples/model_ex/model_examples_stacked.py
    :language: python
    :start-after: ###

.. image:: ../img/model_examples_stacked.svg
   :alt: Data/model comparison, stacked plot
   :width: 500

.. note::
    The function :func:`add_luminosity() <plothist.plothist_style.add_luminosity>` is used here to add information on the luminosity used for the data. This is common practice in high energy physics, and this function is provided to make it easy to add this information to the plot.


Unstacked histograms
--------------------

Unstacked histograms:

.. literalinclude:: ../examples/model_ex/model_examples_unstacked.py
    :language: python
    :start-after: ###

.. image:: ../img/model_examples_unstacked.svg
   :alt: Data/model comparison, stacked plot
   :width: 500


Stacked and unstacked histograms
---------------------------------

Stacked and unstacked histograms can be combined:

.. literalinclude:: ../examples/model_ex/model_examples_stacked_unstacked.py
    :language: python
    :start-after: ###

.. image:: ../img/model_examples_stacked_unstacked.svg
   :alt: Data/model comparison, stacked and unstacked plot with histograms
   :width: 500

.. _advanced-model-functions-comparison-label:
Models made of functions
------------------------

The function :func:`plot_data_model_comparison() <plothist.plotters.plot_data_model_comparison>` can also be used to compare data and functions:

.. literalinclude:: ../examples/model_ex/ratio_data_vs_model_with_stacked_and_unstacked_function_components.py
    :language: python
    :start-after: ###

.. image:: ../img/ratio_data_vs_model_with_stacked_and_unstacked_function_components.svg
   :alt: Data/Model comparison, model with stacked and unstacked function components
   :width: 500

.. note::
   :func:`plot_data_model_comparison() <plothist.plotters.plot_data_model_comparison>` can also be used with only one component as the model. To compare a function with a histogram, just put the function in a list in ``stacked_components`` (or ``unstacked_components``, it gives the same result in this case) argument and the histogram in the ``data_hist`` argument.


Model uncertainty
-----------------

As said earlier, the comparison function can take any comparison method available in :func:`plot_comparison() <plothist.plotters.plot_comparison>`. To use pulls instead of the ratio to compare the histograms:

.. literalinclude:: ../examples/model_ex/model_examples_pull.py
    :language: python
    :start-after: ###

.. image:: ../img/model_examples_pull.svg
   :alt: Data/model comparison with pull, stacked plot
   :width: 500


Now, if you do not want to show nor take into account the model uncertainties, setting ``model_uncertainty`` to ``False`` removes them and updates the definition of the pulls:

.. literalinclude:: ../examples/model_ex/model_examples_pull_no_model_unc.py
    :language: python
    :start-after: ###

.. image:: ../img/model_examples_pull_no_model_unc.svg
   :alt: Data/model comparison with pull, no model stat. unc., stacked plot
   :width: 500


.. warning::
   ``data_hist`` has by default asymmetrical error bars. If the provided histogram is weighted, an error is raised and you need to set ``data_uncertainty_type="symmetrical"``.

.. note::
    To plot the uncertainty of the model as a hashed area, as done in :func:`plot_model() <plothist.plotters.plot_model>`, you can use the standalone function :func:`plot_hist_uncertainties() <plothist.plotters.plot_hist_uncertainties>`.

.. note::
    In the two examples above, the bin width is hardcoded in the `ylabel`. For a 1D histogram with a regular binning, it is possible to get the bin width from the ``boost_histogram.Histogram`` object using ``h.axes[0].widths[0]``.

Comparison overview
===================

Here is a collection of examples showing complex plots showing all the possible comparisons between data and model. The idea is to show how to use :func:`plot_comparison() <plothist.plotters.plot_comparison>` and :func:`plot_data_model_comparison() <plothist.plotters.plot_data_model_comparison>` to make the plots shown in the examples below. The plots are a bit more complex than the ones shown above, but the code to produce them is still quite simple.


All the different comparisons
-----------------------------

Below is shown how to make a plot with all the possible comparisons between data and model. The idea is to use :func:`plot_data_model_comparison() <plothist.plotters.plot_data_model_comparison>` to make the plot with the ratio comparison, and then use :func:`plot_comparison() <plothist.plotters.plot_comparison>` to add the other comparisons. The :func:`plot_comparison() <plothist.plotters.plot_comparison>` function can take a ``fig`` and ``ax`` argument to add the comparison to an existing figure. The :func:`plot_data_model_comparison() <plothist.plotters.plot_data_model_comparison>` function returns the figure and axes used to make the plot, so we can use them to add the other comparisons.

.. literalinclude:: ../examples/model_ex/model_all_comparisons.py
    :language: python
    :start-after: ###

.. image:: ../img/model_all_comparisons.svg
   :alt: Data/model comparison with all comparisons, stacked plot
   :width: 500


No model uncertainties
----------------------


Same example as above, but we remove the statistical uncertainties of the model by adding ``model_uncertainty=False`` in :func:`plot_data_model_comparison() <plothist.plotters.plot_data_model_comparison>` and pass a model histogram without uncertainties to :func:`plot_comparison() <plothist.plotters.plot_comparison>`:

.. literalinclude:: ../examples/model_ex/model_all_comparisons_no_model_unc.py
    :language: python
    :start-after: ###

.. image:: ../img/model_all_comparisons_no_model_unc.svg
   :alt: Data/model comparison with all comparisons, no model uncertainties, stacked plot
   :width: 500
