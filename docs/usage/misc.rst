.. _usage-misc-label:

====
Misc
====


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


With zfit
~~~~~~~~~

This should be called after you have fitted your model and you have a ``zfit.pdf.BasePDF`` object.

.. code-block:: python

    from scipy.interpolate import interp1d
    import pickle

    def save_pdf(var, pdf, path="pdf.pkl", npoints=10000, verbose=True):
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
        npoints : int, optional
            The number of points to evaluate the PDF at. Default is 10000.
        verbose : bool, optional
            Whether to print progress. Default is True.

        Returns
        -------
        pdf_func : scipy.interpolate.interp1d

        Notes
        -----
        The PDF is saved as a scipy.interpolate.interp1d function with pickle.
        """

        lower, upper = var.limits
        x = np.linspace(lower[-1][0], upper[0][0], npoints)

        # Evaluate the PDF at the given points
        pdf_x = zfit.run(pdf.pdf(x, norm_range=var))

        # Interpolate the PDF
        pdf_func = interp1d(x, pdf_x)

        with open(path, "wb") as f:
            if verbose:
                print(f"Saving model to {f.name}")
            pickle.dump(pdf_func, f)

        return pdf_func


Renormalize the PDF
-------------------

The ``pdf_func`` you get, by either get it from function or read the saved pickle file for ``RooFit`` or ``zfit``, has an area of 1. When you want to plot it, you need to multiply it by the bin width of your histogram, the number of expected events in the range and the integral of the PDF in the range. This can be done easily using this small function:

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

Then you can use ``plot_model()`` or ``plot_data_model_comparison()`` to plot the PDF and do all sort of comparisons with the ``plothist`` interface.