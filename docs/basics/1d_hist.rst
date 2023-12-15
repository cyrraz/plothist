.. _basics-1d_hist-label:

==================
Plot 1D histograms
==================

The examples below make use of a pandas dataframe ``df`` containing dummy data, that can be loaded with:

.. code-block:: python

    from plothist import get_dummy_data
    df = get_dummy_data()

.. note::
   It is not recommended to copy and paste code from this page to reproduce the shown examples.
   Instead, please visit the `plot gallery <https://plothist.readthedocs.io/en/latest/example_gallery/>`_, because it contains a standalone script for each example, that you can run directly to produce the plot.

Simple 1D histogram
===================

To plot a simple 1d histogram:

.. literalinclude:: ../examples/1d_hist/1d_hist_simple.py
    :language: python
    :start-after: ###

.. image:: ../img/1d_hist_simple.svg
   :alt: Simple hist
   :width: 500


It is really easy to add multiple histogram to the same figure:

.. literalinclude:: ../examples/1d_hist/1d_elt1.py
    :language: python
    :start-after: ###

.. image:: ../img/1d_elt1.svg
   :alt: Simple hist
   :width: 500


or stack them:

.. literalinclude:: ../examples/1d_hist/1d_elt1_stacked.py
    :language: python
    :start-after: ###

.. image:: ../img/1d_elt1_stacked.svg
   :alt: Simple stacked hist
   :width: 500

Histogram with error bars
=========================

To perform a simple histogram with error bars, use the ``plot_error_hist`` function:

.. literalinclude:: ../examples/1d_hist/1d_elt2.py
    :language: python
    :start-after: ###

.. image:: ../img/1d_elt2.svg
   :alt: Simple error hist
   :width: 500


The function can also take what kind of bin uncertainty to use for hist with the argument ``uncertainty_type``: ``"symmetrical"`` for the Poisson standard deviation derived from the variance stored in the histogram object, ``"asymmetrical"`` for asymmetrical uncertainties based on a Poisson confidence interval. Default is ``"symmetrical"``.


Plotting functions
==================

Everything presented for the histogram is also true to plot functions using the ``plot_function`` function:

.. literalinclude:: ../examples/1d_hist/1d_fct.py
    :language: python
    :start-after: ###

.. image:: ../img/1d_fct.svg
    :alt: Simple function
    :width: 500

In particular, you can stack functions:

.. literalinclude:: ../examples/1d_hist/1d_fct_stacked.py
    :language: python
    :start-after: ###

.. image:: ../img/1d_fct_stacked.svg
    :alt: Simple stacked function
    :width: 500

.. _basics-1d_hist_comparison-label:
Comparing two histograms
========================

To compare two histograms, five comparison methods are available: ``ratio``, ``pull``, ``difference``, ``relative_difference`` and ``asymmetry``. The examples below are using the histograms defined above.

Ratio
-----

Ratio is the default comparison method:

.. literalinclude:: ../examples/1d_hist/1d_comparison_ratio.py
    :language: python
    :start-after: ###

.. image:: ../img/1d_comparison_ratio.svg
   :alt: Simple ratio comparison
   :width: 500


Pull
----

To perform a pull comparison:

.. literalinclude:: ../examples/1d_hist/1d_comparison_pull.py
    :language: python
    :start-after: ###

.. image:: ../img/1d_comparison_pull.svg
   :alt: Simple pull comparison
   :width: 500


Difference
----------

To plot the difference between the two histograms:

.. literalinclude:: ../examples/1d_hist/1d_comparison_difference.py
    :language: python
    :start-after: ###

.. image:: ../img/1d_comparison_difference.svg
   :alt: Simple difference comparison
   :width: 500


Relative difference
-------------------

To plot the relative difference between the two histograms:

.. literalinclude:: ../examples/1d_hist/1d_comparison_relative_difference.py
    :language: python
    :start-after: ###

.. image:: ../img/1d_comparison_relative_difference.svg
   :alt: Simple difference comparison
   :width: 500


Asymmetry
---------

To plot the asymmetry between the two histograms:

.. literalinclude:: ../examples/1d_hist/1d_comparison_asymmetry.py
    :language: python
    :start-after: ###

.. image:: ../img/1d_comparison_asymmetry.svg
   :alt: Simple asymmetry comparison
   :width: 500

