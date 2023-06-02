.. _basics-1d_hist-label:

=================
Basic 1D examples
=================


Simple plot
===========

To plot a simple 1d histogram:

.. code-block:: python

    key = "variable_0"

    fig, ax = plt.subplots()

    h = make_hist(df[key])

    plot_hist(h, ax=ax)

    ax.set_xlabel(key)
    ax.set_ylabel("Entries")

.. image:: ../img/demo_simple_hist.png
   :alt: Simple hist
   :width: 320



With variable manager
=====================


If you have multiple variable to plot, use the variable manager:

.. code-block:: python

    variable_keys = ["variable_0", "variable_1", "variable_2"]

    create_variable_registry(variable_keys)

It will automatically create a `yaml` file with all the plotting information for each variable:

.. code-block:: yaml

    variable_0:
    name: variable_0
    bins: 50
    range:
    - min
    - max
    label: variable_0
    log: false
    legend_location: best
    legend_ncols: 1
    docstring: ''


    variable_1:
        ...

It is then really easy to modify the plotting information. Also really convenient to plot the same variable with different plotting parameters, as a variable is identified by its `variable_key`.

Then, just get the variable from the registery to make every plots:

.. code-block:: python

    # If no range specified for some variable_keys, update the yaml with actual min and max value
    update_variable_registry_ranges(df, variable_keys)

    for variable_key in variable_keys:
        variable = get_variable_from_registry(variable_key)

        fig, ax = plt.subplots()
        h = make_hist(
            df[variable["name"]], bins=variable["bins"], range=variable["range"]
        )
        plot_hist(h, ax=ax)
        ax.set_xlabel(variable["label"])

        ax.set_xlim(variable["range"])
        ax.set_ylabel("Entries")


To access the parameters of the variable, use `get_variable_from_registry(variable_key)`.

Also, you can easily update the `[min, max]` range values using `update_variable_registry_ranges(data, [variable_key])`. The yaml will automatically update. Then, you can modify the yaml to get a more suitable range to diplay in the plot.



