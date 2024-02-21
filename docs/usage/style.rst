.. _usage-style-label:

================
Style and colors
================

Default style
=============

``import plothist`` automatically sets the matplotlib style to a presentation and publication ready style, with large and readable axis labels and legend.

Here are shown two simple comparison plots done with matplotlib functions only. On the left, the default matplotlib style is used. On the right, ``import plothist`` has been added to the same script used to generate the plot on the left:

|img1| |img2|

.. |img1| image:: ../img/matplotlib_example.svg
   :alt: without plothist
   :width: 320

.. |img2| image:: ../img/plothist_example.svg
   :alt: with plothist
   :width: 320


Color palettes
==============

Multiple palettes are available in ``plothist`` in order to make beautiful plots. The function ``get_color_palette(cmap, N)`` gets ``N`` different colors from a chosen ``cmap`` colormap.


Default palette
---------------

When no colors are specified for a plot, the default palette of the ``plothist`` style is applied (adapted from `here <https://matplotlib.org/stable/gallery/style_sheets/ggplot.html>`_):

.. image:: ../img/usage_style_cycle.svg
   :alt: Default ggplot palette

To easily get this color palette, the function ``get_color_palette()`` can be used with ``ggplot`` as the argument:

.. code-block:: python

    from plothist import get_color_palette

    colors = get_color_palette("ggplot", 7)

    >>> colors
    ['#348ABD','#E24A33', '#988ED5', '#777777', '#FBC15E', '#8EBA42', '#FFB5B8']


Cubehelix palette
-----------------

When displaying quantities such as yields or intensities, it is recommended to utilize Perceptually Uniform Sequential Colormaps like the cubehelix colormap for accurate representation.

We provide the cubehelix palette (adapted from `here <https://seaborn.pydata.org/generated/seaborn.cubehelix_palette.html>`_) to create such colormap:

.. code-block:: python

    from plothist import get_color_palette

    colors = get_color_palette("cubehelix", 7)

.. image:: ../img/usage_cubehelix.svg
   :alt: Cubehelix example

You can also use the ``cubehelix_palette()`` function to tweak the colormap parameters.


Matplotlib palettes
-------------------


The function ``get_color_palette(cmap, N)`` can also take any ``cmap`` matplotlib color palette and sequence it in ``N`` different colors (see `here <https://matplotlib.org/stable/gallery/color/colormap_reference.html>`_ for the different ``cmap`` names).

We recommand using ``viridis``, ``coolwarm`` or ``YlGnBu_r``:

.. code-block:: python

    from plothist import get_color_palette

    # From model examples
    ...
    background_categories_colors = get_color_palette("Any cmap name", len(background_categories))
    ...

.. image:: ../img/usage_colorpalette_examples.svg
   :alt: Color palette examples

* ``viridis``:

.. image:: ../img/usage_viridis_palette.svg
   :alt: viridis palette


* ``coolwarm``:

.. image:: ../img/usage_coolwarm_palette.svg
   :alt: coolwarm palette


* ``YlGnBu_r``:

.. image:: ../img/usage_YlGnBu_r_palette.svg
   :alt: YlGnBu_r palette


Setting style
=============

If the style is not set automatically by ``import plothist``, you can set it manually with the function ``set_style()``:

.. code-block:: python

    from plothist import set_style
    set_style()
