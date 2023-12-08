.. _usage-utilities-label:

=================
Utility functions
=================

Add text
========

``add_text()`` is a useful function to add text to a plot. It allows you to easily position text either to the left or right and at the top or bottom of your plot, thanks to aliases on the x and y parameters. Using them will ensure that your text stays aligned to the left or right of the sub-plot (= ax) you specify. The function is a wrapper around ``plt.text()``, so you can pass any parameter to it that you would pass to ``plt.text()`` like ``fontsize``, ``color``, ``fontweight``, etc.

.. code-block:: python

    from plothist import add_text

    # Example from 1d comparison difference plot
    add_text("Comparison of two hist with difference plot", ax=ax_main)
    add_text("Difference ax", x="right", ax=ax_comparison)
    ...

.. image:: ../img/1d_comparison_difference.svg
   :alt: Simple difference comparison
   :width: 500


Automatic ylabel fontsize
=========================

``set_fitting_ylabel_fontsize(ax)`` is a function that will automatically adjust the fontsize of the ylabel so that it fits in the given sub-plot height. It also output the fontsize it used, so you can use it to set the same fontsize for other labels.

.. code-block:: python

    from plothist import set_fitting_ylabel_fontsize

    # Example from pull comparion in model section
    set_fitting_ylabel_fontsize(ax_main)
    ...

.. image:: ../img/model_examples_pull_no_model_unc.svg
   :alt: Pull comparison
   :width: 500

Reorder legend entries
======================

The function ``reorder_legend(ax, order)`` reorder the legend entries of a given plot. It is useful when you want to have a specific order in your legend.

.. code-block:: python

   import matplotlib.pyplot as plt
   from plothist import plot_reordered_legend

   fig, ax = plt.subplots()
   ax.plot([1, 2, 3], label='Line 1')
   ax.plot([3, 2, 1], label='Line 2')

   # To reorder the legend so that 'Line 2' comes first, use:
   plot_reordered_legend(ax, [1, 0])


Plot fit results from RooFit
============================

When you want to use ``plothist`` to plot the result of a fit using ``RooFit``, first you need to convert your functions to scipy functions. This can be done using this small function:

.. code-block:: python

   import numpy as np
   from scipy.interpolate import interp1d
   import pickle

   def save_pdf(var, pdf, path="pdf.pkl", npoints=10000, verbose=True):
      """
      Save a RooFit PDF as a scipy.interpolate.interp1d function.

      Parameters
      ----------
      var : RooRealVar
         The variable to evaluate the PDF at.
      pdf : RooAbsPdf
         The PDF to save.
      path : str, optional
         The path to save the PDF to. Should end with `.pkl`. Default is "pdf.pkl".
      npoints : int, optional
         The number of points to evaluate the PDF at. Default is 10000.
      verbose : bool, optional
         Whether to print progress. Default is True.

      Returns
      -------
      pdf_func : scipy.interpolate.interp1d
         The PDF as a function.

      Notes
      -----
      The PDF is saved as a scipy.interpolate.interp1d function with pickle.
      """
      pdf_x = []

      xlim = (var.getMin(), var.getMax())
      # Get a sample of x values
      x = np.linspace(*xlim, npoints)

      for k, i in enumerate(x, 1):
         var.setVal(i)
         # Evaluate the PDF at the given x value
         pdf_x.append(pdf.getVal(var))
         if verbose:
               print(f"\t{path.replace('.pkl','')} progress [{k*100/len(x):.1f}%]", end="\r")
      if verbose: print()

      # Interpolate the PDF
      pdf_func = interp1d(x, pdf_x)

      with open(path, "wb") as f:
         if verbose:
            print(f"Saving model to {f.name}")
         pickle.dump(pdf_func, f)

      return pdf_func

The ``pdf_func`` you get, by either get it from function or read the saved pickle file, has an area of 1. When you want to plot it, you need to multiply it by the bin width of your histogram, the number of expected events in the range and the integral of the PDF in the range. This can be done easily using this small function:

.. code-block:: python

   from scipy.integrate import quad

   def renormalize(pdf, x_range, bins, n_data):
      """
      Renormalize a PDF to the number of data events.

      Parameters
      ----------
      pdf : callable
         The PDF to renormalize.
      x_range : tuple
         The range of the PDF.
      bins : int
         The number of bins.
      n_data : int
         The number of data events expected in the PDF range.

      Returns
      -------
      pdf : callable
         The renormalized PDF.
      """
      xmin, xmax = x_range
      bin_width = (xmax - xmin) / bins
      integral = quad(pdf, xmin, xmax)[0]

      return lambda x: pdf(x) * n_data * integral * bin_width

Then you can use ``plot_model()`` or ``plot_data_model_comparison()`` to plot the PDF and do all sort of comparisons with the ``plothist`` and ``PyPlot`` interface.


Save figure
===========

When saving a figure, doing ``fig.savefig(path, bbox_inches="tight")`` works great. It will crop all the unnecessary white space by reducing the final figure size. We recommand this way to save a figure.

If you want to have a fixed figure size (e.g. when putting plots into a LaTeX document), the option matplotlib provides is to call ``fig.tight_layout()`` then saving without ``bbox_inches`` argument. This will keep the figure size to the default value or the value you specify in ``plt.figure()``, but it will also change the size and position of the sub-plots, which usually have a negative effect on the overall appearance of the figure.

``savefig(fig, path)`` is a function that keeps the ``figsize`` you specify, but also keeps the sub-plots as they are. If the sub-plots are too big for the figure, you can also specify a new ``figsize`` and the sub-plots will remain the same size and position, while the final figure will be larger.

For example, below is shown a plot saved with ``fig.savefig(path, bbox_inches="tight")``, then with ``fig.tight_layout()`` and saved with ``fig.savefig(path)``, and finally with ``savefig(fig, path)`` from ``plothist``:

.. only:: html

   .. figure:: ../img/savefig_comparisons.gif