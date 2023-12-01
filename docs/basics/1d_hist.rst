.. _basics-1d_hist-label:

========
Basic 1D
========

The examples below make use of a pandas dataframe ``df`` containing dummy data, that can be generated with:

.. code-block:: python

    from plothist.generate_dummy_data import generate_dummy_data
    df = generate_dummy_data()


Simple 1D histogram
===================

To plot a simple 1d histogram:

.. literalinclude:: ../examples/1d_hist_simple.py
    :language: python
    :start-after: ###

.. image:: ../img/1d_hist_simple.svg
   :alt: Simple hist
   :width: 500


It is really easy to add multiple histogram to the same figure:

.. literalinclude:: ../examples/1d_elt1.py
    :language: python
    :start-after: ###

.. image:: ../img/1d_elt1.svg
   :alt: Simple hist
   :width: 500


or stack them:

.. code-block:: python

    fig2, ax2 = plt.subplots()

    plot_hist(
        [h1, h2],
        label=["c1", "c2"],
        ax=ax2,
        edgecolor="black",
        linewidth=0.5,
        histtype="stepfilled",
        stacked=True,
    )

    ax2.set_xlabel(name)
    ax2.set_ylabel("Entries")
    ax2.set_xlim(x_range)
    ax2.legend()

    fig2.savefig("1d_elt1_stacked.svg", bbox_inches="tight")

.. image:: ../img/1d_elt1_stacked.svg
   :alt: Simple stacked hist
   :width: 500

Histogram with error bars
=========================

To perform a simple histogram with error bars, use the ``plot_error_hist`` function:

.. literalinclude:: ../examples/1d_elt2.py
    :language: python
    :start-after: ###

.. image:: ../img/1d_elt2.svg
   :alt: Simple error hist
   :width: 500


The function can also take what kind of bin uncertainty to use for hist with the argument ``uncertainty_type``: ``"symmetrical"`` for the Poisson standard deviation derived from the variance stored in the histogram object, ``"asymmetrical"`` for asymmetrical uncertainties based on a Poisson confidence interval. Default is ``"symmetrical"``.


Plotting functions
==================

Everything presented for the histogram is also true to plot functions using ``plot_function`` function:

.. code-block:: python

    from plothist import plot_function
    from scipy.stats import norm
    from matplotlib import pyplot as plt

    # Define the gaussian function of mean=0.5 and std_dev=3
    def f(x):
        return 1000*norm.pdf(x, loc=0.5, scale=3)

    fig, ax = plt.subplots()

    plot_function(f, range=[-10, 10], ax=ax)

    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")

    fig.savefig("1d_fct.svg", bbox_inches='tight')

.. image:: ../img/1d_fct.svg
    :alt: Simple function
    :width: 500

and stack them:

.. code-block:: python

    from plothist import plot_function
    from scipy.stats import norm
    from matplotlib import pyplot as plt

    # Another function
    def g(x):
        return 1000*norm.pdf(x, loc=2, scale=3)

    fig, ax = plt.subplots()

    plot_function(
        [f, g],
        range=[-10, 10],
        ax=ax,
        labels=["f1", "f2"],
        stacked=True,

    )

    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.legend()

    fig.savefig("1d_fct_stacked.svg", bbox_inches='tight')


.. image:: ../img/1d_fct_stacked.svg
    :alt: Simple stacked function
    :width: 500


Any function from ``scipy.stats`` can also be used to plot a function using ``ax.plot()``.


.. _basics-1d_hist_comparison-label:
Comparing two histograms
========================

To compare two histograms, four comparison methods are available: ``ratio``, ``pull``, ``difference`` and ``relative_difference``. The examples below are using the histograms defined above.

Ratio
-----

Ratio is the default comparison method:

.. literalinclude:: ../examples/1d_comparison_ratio.py
    :language: python
    :start-after: ###

    fig.savefig("1d_comparison_ratio.svg", bbox_inches='tight')

.. image:: ../img/1d_comparison_ratio.svg
   :alt: Simple ratio comparison
   :width: 500


Pull
----

To perform a pull comparison:

.. literalinclude:: ../examples/1d_comparison_pull.py
    :language: python
    :start-after: ###

    fig.savefig("1d_comparison_pull.svg", bbox_inches='tight')

.. image:: ../img/1d_comparison_pull.svg
   :alt: Simple pull comparison
   :width: 500


Difference
----------

To plot the difference between the two histograms:

.. literalinclude:: ../examples/1d_comparison_difference.py
    :language: python
    :start-after: ###

.. image:: ../img/1d_comparison_difference.svg
   :alt: Simple difference comparison
   :width: 500


Relative difference
-------------------

To plot the relative difference between the two histograms:

.. literalinclude:: ../examples/1d_comparison_relative_difference.py
    :language: python
    :start-after: ###

    fig.savefig("1d_comparison_relative_difference.svg", bbox_inches='tight')

.. image:: ../img/1d_comparison_relative_difference.svg
   :alt: Simple difference comparison
   :width: 500



Asymmetry
---------

To plot the asymmetry between the two histograms:

.. code-block:: python

    from plothist import plot_two_hist_comparison

    fig, ax_main, ax_comparison = plot_two_hist_comparison(
        h2,
        h3,
        xlabel=name,
        ylabel="Entries",
        h1_label="$h_1$",
        h2_label="$h_2$",
        comparison = "asymmetry", # <--
    )

    fig.savefig("1d_comparison_asymmetry.svg", bbox_inches='tight')

.. image:: ../img/1d_comparison_asymmetry.svg
   :alt: Simple asymmetry comparison
   :width: 500

