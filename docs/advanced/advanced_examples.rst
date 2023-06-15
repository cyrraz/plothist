.. _advanced-advanced_examples-label:

=================
Advanced examples
=================

Setting style
=============

The default style of ```plothist`` is presentation-ready, with large and readable axis labels and legend. To have a paper-ready plotting style, you can use:

.. code-block:: python

    from plothist import set_paper_style
    set_paper_style()

You can also set both styles in the same script:

.. code-block:: python

    from plothist import set_paper_style, set_presentation_style
    set_paper_style()
    fig, ax = ...

    set_presentation_style()
    fig, ax = ...

