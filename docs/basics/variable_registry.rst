.. _basics-variable_registry-label:

=================
Variable registry
=================


The variable registry is a really convenient tool to store the plotting information of each variable.

Create the registry
===================

To create it, you just need to input the list of variable keys you want to store information for. It will automatically create a ``variable_registry.yaml`` that is easy to use and modify:

.. code-block:: python

    from plothist import create_variable_registry

    variable_keys = ["variable_0", "variable_1", "variable_2"]

    create_variable_registry(variable_keys)

For each variable, the following information is stored by default in the ``variable_registry.yaml`` file:

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

It is then really easy to modify the plotting information by hand inside the ``yaml`` file.

To add new variables to an already existing ``variable_registry.yaml`` file, you only need to add the new variable keys to the ``variable_keys`` list and call ``create_variable_registry`` again. By default, the information on the variables already present in the registry is not overwritten. The hand-written modifications are kept, unless the ``reset`` parameter is set to ``True``.

Getting the plotting information
================================

To get the plotting information of a variable, you can use the ``get_variable_from_registry`` function:

.. code-block:: python

    from plothist import get_variable_from_registry

    variable = get_variable_from_registry("variable_0")

    print(variable)

    >>> {'name': 'variable_0', 'bins': 50, 'range': [min, max], 'label': 'variable_0', 'log': False, 'legend_location': 'best', 'legend_ncols': 1, 'docstring': ''}


Update the registry
===================

Ranges
------

The ``update_variable_registry_ranges`` function automatically updates the range parameter in the ``yaml`` file to the ``min`` and ``max`` values of the variable in the dataset:

.. code-block:: python

    from plothist import update_variable_registry_ranges

    update_variable_registry_ranges(df, variable_keys)

The range has been updated for all the variables in ``variables_keys``. The ``yaml`` file is now:

.. code-block:: yaml

    variable_0:
        name: variable_0
        bins: 50
        range:
        - -10.55227774892869    # min(df["variable_0"])
        - 10.04658448558009     # max(df["variable_0"])
        label: variable_0
        log: false
        legend_location: best
        legend_ncols: 1
        docstring: ''


    variable_1:
        ...

Then, you may manually modify the ``yaml`` to get a more suitable range to display in the plot.

Calling this function again on the same variable keys will not overwrite their ``range`` parameter, unless the ``overwrite`` parameter is set to ``True``.


Add variable properties
-----------------------

You can also add new plotting properties to the variable by using the ``update_variable_registry`` and a custom dictionnary:

.. code-block:: python

    from plothist import update_variable_registry

    new_properties = {
        "text": "default_text",
        "more_info": None,
        "new_property": False,
        "custom_list": [1, "a", True],
        "custom_value": 0,
    }

    update_variable_registry(new_properties, variable_keys)

This will add the new properties to the ``yaml`` file to all the variables in ``variable_keys``:

.. code-block:: yaml

    variable_0:
        name: variable_0
        bins: 50
        range:
        - -10.55227774892869
        - 10.04658448558009
        label: variable_0
        log: false
        legend_location: best
        legend_ncols: 1
        docstring: ''
        text: default_text
        more_info: null         # None is converted to null in yaml
        new_property: false     # False is converted to false in yaml
        custom_list:            # The list is displayed on multiple lines
        - 1
        - a
        - true                  # True is converted to true in yaml
        custom_value: 0


    variable_1:
        ...

The same ``get_variable_from_registry`` function can be used to get the new properties.


Remove parameters
-----------------

To remove a parameter from the plotting informations, you can use the ``remove_variable_registry_parameters`` function:

.. code-block:: python

    from plothist import remove_variable_registry_parameters

    remove_variable_registry_parameters(["range", "log", "legend_ncols", "new_property"], variable_keys)

The ``yaml`` file is updated:

.. code-block:: yaml

    variable_0:
        name: variable_0
        bins: 50
        label: variable_0
        legend_location: best
        docstring: ''
        text: default_text
        more_info: null
        custom_list:
        - 1
        - a
        - true
        custom_value: 0


    variable_1:
        ...


Simple example
==============

To plot multiple variables using the ``variable_manager``, you can use the following code:

.. code-block:: python

    from plothist import (
        make_hist,
        plot_hist,
        create_variable_registry,
        update_variable_registry,
        update_variable_registry_ranges,
        get_variable_from_registry,
        add_text,
    )
    import matplotlib.pyplot as plt

    variable_keys = ["variable_0", "variable_1", "variable_2"]

    # Create the registry
    create_variable_registry(variable_keys)

    # Update the ranges
    update_variable_registry_ranges(df, variable_keys)

    # Add custom info
    update_variable_registry({"text": "simulation"}, variable_keys)

    for variable_key in variable_keys:
        variable = get_variable_from_registry(variable_key)

        fig, ax = plt.subplots()

        h = make_hist(df[variable["name"]], bins=variable["bins"], range=variable["range"])
        plot_hist(h, ax=ax)

        ax.set_xlabel(variable["label"])
        ax.set_xlim(variable["range"])
        ax.set_ylabel("Entries")

        add_text(variable["text"], ax=ax)

        fig.savefig(f"{variable_key}.png", bbox_inches="tight")

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