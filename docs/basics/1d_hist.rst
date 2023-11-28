.. _basics-1d_hist-label:

========
Basic 1D
========

The examples below make use of a pandas dataframe ``df`` containing dummy data, that can be generated with:

.. code-block:: python

    from plothist.generate_dummy_data import generate_dummy_data
    df = generate_dummy_data()


Simple plot
===========

To plot a simple 1d histogram:

.. literalinclude:: ../examples/1d_hist_simple.py
    :language: python
    :lines: 11-

.. image:: ../img/1d_hist_simple.svg
   :alt: Simple hist
   :width: 500



Adding simple elements
======================

It is really easy to add multiple histogram to the same figure:

.. code-block:: python

    from plothist import make_hist, plot_hist
    import matplotlib.pyplot as plt

    name = "variable_1"
    category = "category"

    x1 = df[name][df[category] == 1]
    x2 = df[name][df[category] == 2]

    x_range = (min(min(x1), min(x2)), max(max(x1), max(x2)))

    h1 = make_hist(x1, bins=50, range=x_range)
    h2 = make_hist(x2, bins=50, range=x_range)

    fig, ax = plt.subplots()

    plot_hist(h1, ax=ax, histtype="step", linewidth=1.2, label="c1")
    plot_hist(h2, ax=ax, histtype="step", linewidth=1.2, label="c2")

    ax.set_xlabel(name)
    ax.set_ylabel("Entries")
    ax.set_xlim(x_range)
    ax.legend()

    fig.savefig("1d_elt1.svg", bbox_inches='tight')

.. image:: ../img/1d_elt1.svg
   :alt: Simple hist
   :width: 500


To this, we can add an error-point histogram:

.. code-block:: python

    from plothist import plot_error_hist

    x3 = df[name][df[category] == 3]

    h3 = make_hist(x3, bins=50, range=x_range)

    plot_error_hist(h3, ax=ax, color="black", label="c3")

    # Update the legend
    ax.legend()

    fig.savefig("1d_elt2.svg", bbox_inches='tight')

.. image:: ../img/1d_elt2.svg
   :alt: Simple hist
   :width: 500


We can also add functions using ``scipy``:

.. code-block:: python

    import numpy as np
    from scipy.stats import norm

    x = np.linspace(x_range[0], x_range[1], 200)

    # Define the gaussian function of mean=8 and std_dev=1
    y = norm.pdf(x, 8, 1)

    # Normalize the function
    y *= 900 / max(y)

    ax.plot(x, y, color='green', label='Gaussian')

    # Update the legend
    ax.legend()

    fig.savefig("1d_elt3.svg", bbox_inches='tight')

.. image:: ../img/1d_elt3.svg
   :alt: Simple hist
   :width: 500


.. _basics-1d_hist_comparison-label:
Comparing two histograms
========================

To compare two histograms, four comparison methods are available: ``ratio``, ``pull``, ``difference`` and ``relative_difference``. The examples below are using the histograms defined above.

Ratio
-----

Ratio is the default comparison method:

.. code-block:: python

    from plothist import compare_two_hist

    # Default comparison is ratio
    fig, ax_main, ax_comparison = compare_two_hist(
        h2,
        h3,
        xlabel=name,
        ylabel="Entries",
        h1_label="c2",
        h2_label="c3",
        save_as="1d_comparison_ratio.svg",
    )

.. image:: ../img/1d_comparison_ratio.svg
   :alt: Simple ratio comparison
   :width: 500

Pull
----

To perform a pull comparison:

.. code-block:: python

    from plothist import compare_two_hist

    fig, ax_main, ax_comparison = compare_two_hist(
        h2,
        h3,
        xlabel=name,
        ylabel="Entries",
        h1_label="$c_{2}$",
        h2_label="$c_{3}$",
        comparison = "pull", # <--
        save_as="1d_comparison_pull.svg",
    )

.. image:: ../img/1d_comparison_pull.svg
   :alt: Simple pull comparison
   :width: 500


Difference
----------

To plot the difference between the two histograms:

.. code-block:: python

    from plothist import compare_two_hist, add_text

    fig, ax_main, ax_comparison = compare_two_hist(
        h2,
        h3,
        xlabel=name,
        ylabel="Entries",
        h1_label="$\mathcal{C}_{2}$",
        h2_label="$\mathcal{C}_{3}$",
        comparison = "difference", # <--
    )

    add_text("Comparison of two hist with difference plot", ax=ax_main)
    add_text("Difference ax", x="right", ax=ax_comparison)

    fig.savefig("1d_comparison_difference.svg", bbox_inches='tight')

.. image:: ../img/1d_comparison_difference.svg
   :alt: Simple difference comparison
   :width: 500



Relative difference
-------------------

To plot the relative difference between the two histograms:

.. code-block:: python

    from plothist import compare_two_hist

    fig, ax_main, ax_comparison = compare_two_hist(
        h2,
        h3,
        xlabel=name,
        ylabel="Entries",
        h1_label="$\mathbf{H\,\,1}$",
        h2_label="$\mathbf{H\,\,2}$",
        comparison = "relative_difference", # <--
        save_as="1d_comparison_relative_difference.svg",
    )

.. image:: ../img/1d_comparison_relative_difference.svg
   :alt: Simple difference comparison
   :width: 500
