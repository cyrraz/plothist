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
    :start-after: df = generate_dummy_data()

.. image:: ../img/1d_hist_simple.svg
   :alt: Simple hist
   :width: 500



Adding simple elements
======================

It is really easy to add multiple histogram to the same figure:

.. literalinclude:: ../examples/1d_elt1.py
    :language: python
    :start-after: df = generate_dummy_data()

.. image:: ../img/1d_elt1.svg
   :alt: Simple hist
   :width: 500


To this, we can add an error-point histogram:

.. literalinclude:: ../examples/1d_elt2.py
    :language: python
    :start-after: # fig.savefig("1d_elt1.svg", bbox_inches='tight')

.. image:: ../img/1d_elt2.svg
   :alt: Simple hist
   :width: 500


We can also add functions using ``scipy``:

.. literalinclude:: ../examples/1d_elt3.py
    :language: python
    :start-after: # fig.savefig("1d_elt2.svg", bbox_inches='tight')

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

.. literalinclude:: ../examples/1d_comparison_ratio.py
    :language: python
    :start-after: # Histograms setup is done

.. image:: ../img/1d_comparison_ratio.svg
   :alt: Simple ratio comparison
   :width: 500


Pull
----

To perform a pull comparison:

.. literalinclude:: ../examples/1d_comparison_pull.py
    :language: python
    :start-after: # Histograms setup is done

.. image:: ../img/1d_comparison_pull.svg
   :alt: Simple pull comparison
   :width: 500


Difference
----------

To plot the difference between the two histograms:

.. literalinclude:: ../examples/1d_comparison_difference.py
    :language: python
    :start-after: # Histograms setup is done

.. image:: ../img/1d_comparison_difference.svg
   :alt: Simple difference comparison
   :width: 500


Relative difference
-------------------

To plot the relative difference between the two histograms:

.. literalinclude:: ../examples/1d_comparison_relative_difference.py
    :language: python
    :start-after: # Histograms setup is done

.. image:: ../img/1d_comparison_relative_difference.svg
   :alt: Simple difference comparison
   :width: 500
