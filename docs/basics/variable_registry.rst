.. _basics-variable_registry-label:

=================
Variable registry
=================

The variable registry is a convenient tool to store and get easily any plotting information of variables. The idea is to store the plotting information of each variable in a ``yaml`` file, and then get or modify this information using dedicated functions. Each variable is identified by a ``variable_key`` that is used to get the information from the registry.

Create the registry
===================

To create a variable registry, you just need to input the list of variable keys you want to store information for. The function :func:`create_variable_registry() <plothist.variable_registry.create_variable_registry>` will automatically create a ``variable_registry.yaml`` with default information for each variable:

.. code-block:: python

    from plothist import create_variable_registry

    variable_keys = ["variable_0", "variable_1", "variable_2"]

    create_variable_registry(variable_keys)

For each variable in the list, the following information is stored by default in the ``variable_registry.yaml`` file:

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

The structure being build automatically, it is then easy to modify the plotting information by hand inside the ``yaml`` file.

To add new variables to an already existing ``variable_registry.yaml`` file, you only need to add the new variable keys to the ``variable_keys`` list and call :func:`create_variable_registry() <plothist.variable_registry.create_variable_registry>` again. By default, the information on the variables already present in the registry is not overwritten. The hand-written modifications are kept, unless the ``reset`` parameter is set to ``True``.

Getting the plotting information
================================

To get the plotting information of a variable, you can use the :func:`get_variable_from_registry() <plothist.variable_registry.get_variable_from_registry>` function, which returns a dictionary with the plotting information:

.. code-block:: python

    from plothist import get_variable_from_registry

    variable = get_variable_from_registry("variable_0")

    print(variable)
    # {'name': 'variable_0', 'bins': 50, 'range': [min, max], 'label': 'variable_0', 'log': False, 'legend_location': 'best', 'legend_ncols': 1, 'docstring': ''}


Update the registry
===================

Multiple functions are available to modify the plotting information of the variables in the registry, add or remove some parameters.

Ranges
------

The :func:`update_variable_registry_ranges() <plothist.variable_registry.update_variable_registry_ranges>` function automatically updates the range parameter in the ``yaml`` file to the ``min`` and ``max`` values of the variable in the dataset:

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

Binning
------

The :func:`update_variable_registry_binning() <plothist.variable_registry.update_variable_registry_binning>` function automatically updates the bins' number parameter in the ``yaml`` file to the length of ``numpy.histogram_bin_edges`` minus one (the bins are regular) of the variable in the dataset:

.. code-block:: python

    from plothist import update_variable_registry_binning

    update_variable_registry_binning(df, variable_keys)

The bins' number has been updated for all the variables in ``variables_keys``. The ``yaml`` file is now:

.. code-block:: yaml

    variable_0:
        name: variable_0
        bins: 121 # = len(numpy.histogram_bin_edges(df["variable_0"])) - 1
        range:
        - "min"
        - "max"
        label: variable_0
        log: false
        legend_location: best
        legend_ncols: 1
        docstring: ''


    variable_1:
        ...

Then, you may manually modify the ``yaml`` to get a more suitable range to display in the plot.

Calling this function again on the same variable keys will not overwrite their ``range`` parameter, unless the ``overwrite`` parameter is set to ``True``.

Add or modify variable properties
---------------------------------

You can also add new plotting properties or modify the existing ones by using the :func:`update_variable_registry() <plothist.variable_registry.update_variable_registry>` and a custom dictionary:

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

The same :func:`get_variable_from_registry() <plothist.variable_registry.get_variable_from_registry>` function can be used to get the new properties.

To modify existing properties, you have to call :func:`update_variable_registry() <plothist.variable_registry.update_variable_registry>` with the new properties and the ``overwrite`` parameter set to ``True``. It will overwrite the existing properties values with the new ones.


Remove parameters
-----------------

To remove a parameter from the plotting information, you can use the :func:`remove_variable_registry_parameters() <plothist.variable_registry.remove_variable_registry_parameters>` function:

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

Here is an example of how to create, update, and use the variable registry to plot histograms. A similar example can be found in :ref:`basics-2d_hist-correlation-label`.

.. code-block:: python

    from plothist import (
        make_hist,
        plot_hist,
        create_variable_registry,
        update_variable_registry,
        update_variable_registry_ranges,
        update_variable_registry_binning,
        get_variable_from_registry,
        add_text,
    )
    import matplotlib.pyplot as plt

    variable_keys = ["variable_0", "variable_1", "variable_2"]

    # Create the registry
    create_variable_registry(variable_keys)

    # Update the ranges
    update_variable_registry_ranges(df, variable_keys)

    # Update the bins' number
    update_variable_registry_binning(df, variable_keys)

    # Add custom info
    update_variable_registry({"text": "my analysis"}, variable_keys)

    for variable_key in variable_keys:
        # Get the variable information using the key. variable is a dictionary
        variable = get_variable_from_registry(variable_key)

        fig, ax = plt.subplots()

        # Make the histogram using the variable information from the registry
        h = make_hist(df[variable["name"]], bins=variable["bins"], range=variable["range"])
        plot_hist(h, ax=ax)

        # Get the label and range from the registry
        ax.set_xlabel(variable["label"])
        ax.set_xlim(variable["range"])
        ax.set_ylabel("Entries")

        # Get the custom text from the registry
        add_text(variable["text"], ax=ax)

        fig.savefig(f"{variable_key}.pdf", bbox_inches="tight")

Advanced example
================

It is sometimes useful to plot the same variable with different plotting parameters. A variable is identified by its ``variable_key`` using :func:`get_variable_from_registry() <plothist.variable_registry.get_variable_from_registry>`, and the ``name`` is the variable name in the dataset.

Example: to plot a zoom on a variable but still keep the original one, you can create a new variable key with the same ``name`` and different plotting parameters:

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

and then just call the new variable key:

.. code-block:: python

    variable_keys = ["variable_0", "variable_0_zoom", "variable_1"]

    for variable_key in variable_keys:
        variable = get_variable_from_registry(variable_key)
        ...
