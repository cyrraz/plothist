.. _basics-variable_manager-label:

================
Variable registry
================


How to use the variable registry
===============================

If you have multiple variable to plot, you can use the variable registry, defined with the variable keys from your dataset:

.. code-block:: python

    from plothist import create_variable_registry

    variable_keys = ["variable_0", "variable_1", "variable_2"]

    create_variable_registry(variable_keys)

It will automatically create a ``yaml`` file with all the plotting information for each variable:

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

It is then really easy to modify the plotting information of every variables.

Then, just get the variable from the registery to make every plots:

.. code-block:: python

    from plothist import make_hist, plot_hist
    from plothist import update_variable_registry_ranges, get_variable_from_registry
    import matplotlib.pyplot as plt

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


As we can see in the example, ``get_variable_from_registry(variable_key)`` is used to get access the parameters of the variable.

Also, you can easily get the ``[min, max]`` range values using ``update_variable_registry_ranges(data, [variable_key])``. The yaml will automatically update. Then, you can modify the yaml to get a more suitable range to display in the plot.


Advanced example
================

It is also really convenient to plot the same variable with different plotting parameters. A variable is identified by its ``variable_key`` using ``get_variable_from_registry``, and the ``name`` is the variable name in the dataset.

To plot a zoom on some variable, but still keep the original plot:

.. code-block:: yaml

    variable_0:
    name: variable_0
    bins: 50
    range:
    - -10
    - 10
    label: $Variable_{0}$
    log: false
    legend_location: best
    legend_ncols: 1
    docstring: ''

    variable_0_zoom:
    name: variable_0
    bins: 50
    range:
    - -1
    - 1
    label: $Zoom of Variable_{0}$
    log: false
    legend_location: upper right
    legend_ncols: 1
    docstring: ''


    variable_1:
        ...

and then just call:

.. code-block:: python

    variable_keys = ["variable_0", "variable_0_zoom", "variable_1"]

    for variable_key in variable_keys:
        variable = get_variable_from_registry(variable_key)
        ...