.. _advanced-advanced_examples-label:

=================
Advanced examples
=================

Setting style
=============

``import plothist`` automatically sets the matplotlib style to a presentation-ready style, with large and readable axis labels and legend.

To have a publication-ready plotting style, you can use:

.. code-block:: python

    from plothist import set_style
    set_style("publication")

You can also set both styles in the same script:

.. code-block:: python

    from plothist import set_style
    set_style("publication")
    fig, ax = ...

    set_style("presentation")
    fig, ax = ...

