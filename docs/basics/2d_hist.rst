.. _basics-2d_hist-label:

========
Basic 2D
========

The examples below make use of a pandas dataframe ``df`` containing dummy data, that can be generated with:

.. code-block:: python

    from plothist.generate_dummy_data import generate_dummy_data
    df = generate_dummy_data()


Simple plot
===========

To plot a simple 2d histogram:

.. code-block:: python

    from plothist import make_2d_hist, plot_2d_hist
    import matplotlib.pyplot as plt

    name_x = "variable_0"
    name_y = "variable_1"

    h = make_2d_hist([df[name_x], df[name_y]])

    fig, ax, ax_colorbar = plot_2d_hist(h, colorbar_kwargs={"label": "Entries"})

    ax.set_xlabel(name_x)
    ax.set_ylabel(name_y)

    ax.set_xlim(-9, 9)
    ax.set_ylim(-9, 9)

    fig.savefig("2d_hist_simple.svg", bbox_inches='tight')

.. image:: ../img/2d_hist_simple.svg
   :alt: Simple 2d hist
   :width: 500


Correlations with variable manager
==================================

See :ref:`basics-variable_manager-label` on how to use the variable manager.

Variable manager is a really useful tool to manage and plot the correlation between multiple variables:

.. code-block:: python

    from itertools import combinations
    from plothist import make_2d_hist, plot_2d_hist
    from plothist import create_variable_registry, update_variable_registry_ranges, get_variable_from_registry
    import matplotlib.pyplot as plt

    # No need to redo this step if the registry was already created before
    variable_keys = ["variable_0", "variable_1", "variable_2"]
    create_variable_registry(variable_keys)
    update_variable_registry_ranges(df, variable_keys)

    fig, axs = plt.subplots(nrows=3, ncols=2, figsize=(3.5, 12), gridspec_kw={"width_ratios": [4, 0.3]})
    plt.subplots_adjust(hspace=.5)

    # Get all the correlation plot between the variables
    variable_keys_combinations = list(combinations(variable_keys, 2))

    for k_combination, variable_keys_combination in enumerate(variable_keys_combinations):
        variable0 = get_variable_from_registry(variable_keys_combination[0])
        variable1 = get_variable_from_registry(variable_keys_combination[1])

        h = make_2d_hist(
            [df[variable0["name"]], df[variable1["name"]]],
            bins=(variable0["bins"], variable1["bins"]),
            range=(variable0["range"], variable1["range"]),
        )

        ax = axs[k_combination][0]
        ax_colorbar = axs[k_combination][1]

        plot_2d_hist(h, fig=fig, ax=ax, ax_colorbar=ax_colorbar, colorbar_kwargs={"label": "Entries"})

        ax.set_xlabel(variable0["name"])
        ax.set_ylabel(variable1["name"])

        ax.set_xlim(variable0["range"])
        ax.set_ylim(variable1["range"])

    fig.savefig("2d_hist_correlations.svg", bbox_inches='tight')

.. image:: ../img/2d_hist_correlations.svg
   :alt: Simple 2d hist
   :width: 1500


Advanced
========


Uneven binning
------------

Instead of inputing a number of bins and a range in ``make_2d_hist()``, the bins parameter can be a list of all the edges:

.. code-block:: python

    import matplotlib.pyplot as plt
    from plothist import make_2d_hist, plot_2d_hist

    name_x = "variable_0"
    name_y = "variable_1"
    # Bins [-10,0], [0,10] for variable 1,
    # and bins [-10,-5], [-5,0], [0,5], [5,10] for variable 2
    bins = [[-10, 0, 10], [-10, -5, 0, 5, 10]]

    h = make_2d_hist([df[name_x], df[name_y]], bins=bins)

    fig, ax, ax_colorbar = plot_2d_hist(h, colorbar_kwargs={"label": "Entries"})

    ax.set_xlabel(name_x)
    ax.set_ylabel(name_y)

    fig.savefig("2d_hist_uneven.svg", bbox_inches='tight')


.. image:: ../img/2d_hist_uneven.svg
   :alt: 2d hist with uneven binning
   :width: 500



Display 1D distributions
------------------------

To plot a 2d histogram with x and y projections:

.. code-block:: python

    from plothist import make_2d_hist, plot_2d_hist_with_projections

    name_x = "variable_0"
    name_y = "variable_1"

    h = make_2d_hist([df[name_x], df[name_y]], bins=[50,50])

    fig, ax_2d, ax_x_projection, ax_y_projection, ax_colorbar = plot_2d_hist_with_projections(
        h,
        xlabel="variable_0",
        ylabel="variable_1",
        ylabel_x_projection="Entries",
        xlabel_y_projection="Entries",
        offset_x_labels=False,
        colorbar_kwargs={"label": "Entries"},
        save_as="2d_hist_with_projections.svg",
    )

.. image:: ../img/2d_hist_with_projections.svg
   :alt: 2d hist with x and y projections
   :width: 500
