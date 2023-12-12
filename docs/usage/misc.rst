.. _usage-misc-label:

====
Misc
====

.. _plot-fit-result-label:
Plot fit results
================

Two steps are necessary when you want to use ``plothist`` to plot the result of a fit using ``RooFit`` or ``zfit``.

Getting the PDF
---------------

First you need to convert your functions to scipy functions. This can be done using a small function.

With RooFit
~~~~~~~~~~~

This should be called after you have fitted your model and you have a ``RooAbsPdf`` object.

.. code-block:: python

   import numpy as np
   from scipy.interpolate import interp1d
   import pickle

   def save_pdf(var, pdf, path="pdf.pkl", n_points=10000):
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
      n_points : int, optional
         The number of points to evaluate the PDF at. Default is 10000.

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
      x = np.linspace(*xlim, n_points)

      for i in x:
         var.setVal(i)
         # Evaluate the PDF at the given x value
         pdf_x.append(pdf.getVal(var))

      # Interpolate the PDF
      pdf_func = interp1d(x, pdf_x)

      with open(path, "wb") as f:
         print(f"Saving model to {f.name}")
         pickle.dump(pdf_func, f)

      return pdf_func


.. warning::

   For a complex PDF that depends on multiple observables, be sure get the correct PDF projection before calling this function (e.g. setting your categories with ``category.setIndex()``, create a PDF product with ``ROOT.RooProdPdf()``, and if one observable depends on the binning creating the projection using ``pdf.createProjection()``...).


With zfit
~~~~~~~~~

This should be called after you have fitted your model and you have a ``zfit.pdf.BasePDF`` object.

.. code-block:: python

    from scipy.interpolate import interp1d
    import pickle

    def save_pdf(var, pdf, path="pdf.pkl", n_points=10000):
        """
        Save a PDF from zfit as a callable function.

        Parameters
        ----------
        var : zfit.Space
            The variable to evaluate the PDF at.
        pdf : zfit.pdf.BasePDF
            The PDF to save.
        path : str, optional
            The path to save the PDF to. Default is "pdf.pkl".
        n_points : int, optional
            The number of points to evaluate the PDF at. Default is 10000.

        Returns
        -------
        pdf_func : scipy.interpolate.interp1d

        Notes
        -----
        The PDF is saved as a scipy.interpolate.interp1d function with pickle.
        """

        lower, upper = var.limits
        x = np.linspace(lower[-1][0], upper[0][0], n_points)

        # Evaluate the PDF at the given points
        pdf_x = zfit.run(pdf.pdf(x, norm_range=var))

        # Interpolate the PDF
        pdf_func = interp1d(x, pdf_x)

        with open(path, "wb") as f:
            print(f"Saving model to {f.name}")
            pickle.dump(pdf_func, f)

        return pdf_func


Renormalize the PDF
-------------------

The ``pdf_func`` you get, by either get it from function or read the saved pickle file for ``RooFit`` or ``zfit``, has an area of 1. When you want to plot it, you need to multiply it by the bin width of your histogram, the number of expected events in the range for this PDF and the integral of the PDF in the range. This can be done easily using this small function:

.. code-block:: python

   from scipy.integrate import quad

   def renormalize(pdf, x_range, n_bins, n_data):
      """
      Renormalize a PDF to its corresponding number of data events.

      Parameters
      ----------
      pdf : callable
         The PDF to renormalize.
      x_range : tuple
         The range of the PDF.
      n_bins : int
         The number of bins. Regular binning is assumed.
      n_data : int
         The number of predicted data events in the x_range associated to the pdf.

      Returns
      -------
      pdf : callable
         The renormalized PDF.
      """

      xmin, xmax = x_range
      bin_width = (xmax - xmin) / n_bins
      integral = quad(pdf, xmin, xmax)[0] # If x_range is equal to the full range of the PDF, this is equal to 1.

      def renormalized_pdf(x):
         return pdf(x) * n_data * bin_width / integral

      return renormalized_pdf

Then you can use ``plot_model()`` or ``plot_data_model_comparison()`` (see :ref:`advanced-asymmetry-label`) to plot the PDF and do all sort of comparisons with the ``plothist`` interface:

.. image:: ../img/asymmetry_comparison_advanced.svg
   :alt: Advanced asymmetry comparison
   :width: 500