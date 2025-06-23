.. _basics-func_1d-label:

==============
Plot functions
==============

The examples below make use of a numpy ndarray ``df`` containing dummy data (you may also use a pandas dataframe), that can be loaded with:

.. code-block:: python

    from plothist_utils import get_dummy_data

    df = get_dummy_data()

.. note::
   This page presents functions of ``plothist`` step by step and gives information about how to use them.
   To reproduce the examples, please visit the `example gallery <https://plothist.readthedocs.io/en/latest/example_gallery/>`_, because it contains a standalone script for each example, that you can run directly.

.. note::
    All the functions used in the examples below can take a lot more arguments to customize the plot, see the :ref:`documentation-label` for more details.


Simple function
===============

Plothist supports plotting of functions using the :func:`plot_function() <plothist.plotters.plot_function>` function:

.. literalinclude:: ../../src/plothist/examples/func_1d/fct_1d.py
    :language: python
    :start-after: ###

.. image:: ../img/fct_1d.png
    :alt: Simple function
    :width: 500

In particular, you can stack functions using the ``stacked=True`` argument:

.. literalinclude:: ../../src/plothist/examples/func_1d/1d_fct_stacked.py
    :language: python
    :start-after: ###

.. image:: ../img/1d_fct_stacked.svg
    :alt: Simple stacked function
    :width: 500


Comparison with functions
=========================

To compare one histogram with a model made of one or multiple functions, see the :ref:`advanced-model-functions-comparison-label` section.

To compare two functions together, see the :ref:`advanced-asymmetry-label`.

Utilities
=========

Example on how to convert a function from an external fitting package to an object that can be used by ``plothist`` can be found in the :ref:`plot-fit-result-label` section.
