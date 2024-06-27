.. _advanced-label:

=======================
Other advanced examples
=======================

This section shows how to use the ``plothist`` package to make more complex plots. The examples below take advantage of the flexibility of the package to produce more advanced plots with ease. For each example, the code is commented to explain the logic and steps taken to produce the plots.

The examples use of a numpy ndarray ``df`` containing dummy data (you may also use a pandas dataframe), that can be loaded with:

.. code-block:: python

    from plothist import get_dummy_data

    df = get_dummy_data()

Advanced example comparing two histograms
=========================================

In this example, we will compare two tuples of histograms and use pull and ratio comparisons. First, we make the histograms and scale them. Then, we plot the histograms and the comparison plots on different axes:

.. image:: ../img/1d_comparison_advanced.svg
   :alt: Advanced hist comparison
   :width: 500

.. literalinclude:: ../examples/advanced/1d_comparison_advanced.py
   :language: python
   :start-after: ###


.. _advanced-asymmetry-label:
Advanced example using asymmetry comparison
===========================================

This example shows how to plot an asymmetry plot between two histograms and two functions. Information on how to convert a function from an external fitting package to an object that can be used by ``plothist`` can be found in :ref:`plot-fit-result-label`.

.. image:: ../img/asymmetry_comparison_advanced.svg
   :alt: Advanced asymmetry comparison
   :width: 500

.. literalinclude:: ../examples/advanced/asymmetry_comparison_advanced.py
   :language: python
   :start-after: ###

Flatten 2D variable
===================

Compare data and stacked histogram for a flatten 2D variable:

.. image:: ../img/model_examples_flatten2D.svg
   :alt: Data/model comparison, flatten variable
   :width: 500

.. literalinclude:: ../examples/advanced/model_examples_flatten2D.py
    :language: python
    :start-after: ###



Side-by-side categorical histograms
===================================

Here is an example to put three histograms side by side with a categorical axis and boost-histogram. It shows a specificity of ``matplotlib`` when plotting a list of histograms:

.. image:: ../img/1d_side_by_side.svg
    :alt: Side by side histograms
    :width: 500

.. literalinclude:: ../examples/advanced/1d_side_by_side.py
    :language: python
    :start-after: ###

To also add the number of entries on top of each bar, you can use the following code:

.. code-block:: python

    # Get the correct shift in x-axis for each bar
    def calculate_shifts(width, n_bars):
       half_width = width / 2
       shift = np.linspace(-half_width, half_width, n_bars, endpoint=False)
       shift += width / (2 * n_bars)
       return shift


    bin_width = 0.8
    shift = calculate_shifts(bin_width, len(histos))

    # Loop over the histograms, add on top of each bar the number of entries
    for i, histo in enumerate(histos):
       for j, value in enumerate(histo.values()):
          ax.text(
                j + 0.5 + shift[i],
                value,
                int(value), # If weighted, f"{height:.1f}" can be used as a better representation of the bin content
                color="black",
                ha="center",
                va="bottom",
          )