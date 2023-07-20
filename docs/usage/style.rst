.. _advanced-advanced_examples-label:

=======================
Style, fonts and colors
=======================

Setting style
=============

``import plothist`` automatically sets the matplotlib style to a presentation and publication ready style, with large and readable axis labels and legend.

Latin Modern fonts are used by default. You can install the font by using the script located in the `github repository of plothist <https://github.com/cyrraz/plothist/tree/main/scripts/install_latin_modern_fonts.sh>`.

To have a small plotting style, you can use:

.. code-block:: python

    from plothist import set_style
    set_style("small")

You can also set both styles in the same script:

.. code-block:: python

    from plothist import set_style
    set_style("small")
    fig, ax = ...

    set_style("default")
    fig, ax = ...

For the first hep example in :ref:`advanced-hep_examples-label`:

Default style:

.. image:: ../img/hep_examples_dataMC_stacked.svg
   :alt: Default style
   :width: 500


Small style:

.. image:: ../img/hep_examples_dataMC_stacked_small.svg
   :alt: Small style
   :width: 500


Color palette
=============

When displaying quantities such as yields or intensities, it is recommended to utilize Perceptually Uniform Sequential Colormaps like the cubehelix colormap for accurate representation.

We provide the ``cubehelix_palette()`` (see `here <https://plothist.readthedocs.io/en/latest/documentation/documentation.html#plothist.plotters.cubehelix_palette>`_) function to create such colormap.

.. code-block:: python

    from plothist import cubehelix_palette

    palette = cubehelix_palette(11)

.. image:: ../img/adv_cubehelix.svg
   :alt: Presentation style
..    :width: 500
