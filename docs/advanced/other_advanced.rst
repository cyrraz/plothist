.. _advanced-label:

======================
Other complex examples
======================

This section shows how to use the ``plothist`` package to make more complex plots. The examples below use a lot of the functionnality of the package to produce the plots, but the code is still quite simple and easy to read.

They make use of a pandas dataframe ``df`` containing dummy data, that can be loaded with:

.. code-block:: python

    from plothist import get_dummy_data
    df = get_dummy_data()

Advanced example comparing two histograms
=========================================

In this example, we will compare two tuples of histograms and use pull and ratio comparisons.

First, we make the histograms and scale them. Then, we plot the histograms and the comparison plots on different axes:

.. literalinclude:: ../examples/advanced/1d_comparison_advanced.py
   :language: python
   :start-after: ###

.. image:: ../img/1d_comparison_advanced.svg
   :alt: Advanced hist comparison
   :width: 500


.. _advanced-asymmetry-label:
Advanced example using asymmetry comparison
===========================================

This example shows how to plot an asymmetry plot between two histograms and two functions. Information on how to convert a function from an external fitting package to an object that can be used by ``plothist`` can be found in :ref:`plot-fit-result-label`.

.. literalinclude:: ../examples/advanced/asymmetry_comparison_advanced.py
   :language: python
   :start-after: ###

.. image:: ../img/asymmetry_comparison_advanced.svg
   :alt: Advanced asymmetry comparison
   :width: 500


Flatten 2D variable
===================

Compare data and stacked histogram for a flatten 2D variable:

.. literalinclude:: ../examples/advanced/model_examples_flatten2D.py
    :language: python
    :start-after: ###

.. image:: ../img/model_examples_flatten2D.svg
   :alt: Data/model comparison, flatten variable
   :width: 500

