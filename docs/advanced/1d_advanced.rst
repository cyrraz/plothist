.. _advanced-1d_hist-label:

===========
Advanced 1D
===========

The examples below make use of a pandas dataframe ``df`` containing dummy data, that can be generated with:

.. code-block:: python

    from plothist.generate_dummy_data import generate_dummy_data
    df = generate_dummy_data()


Comparing two histograms
========================

In this example, we will compare two tuples of histograms and use pull and ratio comparisons.

First, we make the histograms and scale them. Then, we plot the histograms and the comparison plots on different axes:

.. literalinclude:: ../../examples/advanced_1d/1d_hist_comparison.py
   :language: python
   :start-after: ###

.. image:: ../img/1d_comparison_advanced.svg
   :alt: Advanced hist comparison
   :width: 500