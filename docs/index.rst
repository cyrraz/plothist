PlotHist
========

**Plot histograms in a scalable way and a beautiful style.**

|img1|      |img2|

.. |img1| image:: img/intro_2dhist_hep.png
   :alt: Complex hep example
   :width: 320

.. |img2| image:: img/intro_hist_hep.png
   :alt: Hep example
   :width: 320

|GitHub Project| |PyPI version| |Docs from latest| |Docs from main| |Code style: black|

Main idea
---------

**Major advantages over other plotting libraries**: scalability, style and user friendly way of managing variables.

**First idea**: separate the histogram creation from its data. Then you can easily manage histogram objects (`boostHist` library) and plot large amount of variables and data really fast.

.. code-block:: python

    key = "variable_0"

    fig, ax = plt.subplots()

    h = make_hist(df[key])

    plot_hist(h, ax=ax)

    ax.set_xlabel(key)
    ax.set_ylabel("Entries")

.. image:: img/demo_simple_hist.png
   :alt: Simple hist
   :width: 320


**Second idea**: plot a lot of variable easily with the variable manager

.. code-block:: python

    variable_keys = ["variable_0", "variable_1", "variable_2"]

    create_variable_registry(variable_keys)

will automatically create a `yaml` file with all the plotting information for each variable:

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

-> Really easy to modify the plotting information. Also really convenient to plot the same variable with different plotting parameters.

Then, just get the variable from the registery to make every plots

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

et voila.



.. |GitHub Project| image:: https://img.shields.io/badge/GitHub--blue?style=social&logo=GitHub
   :target: https://github.com/cyrraz/plothist
.. |PyPI version| image:: https://badge.fury.io/py/plothist.svg
   :target: https://badge.fury.io/py/plothist
.. |Code style: black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
.. |Docs from latest| image:: https://img.shields.io/badge/docs-v0.7.2-blue.svg
   :target: https://plothist.readthedocs.io/
.. |Docs from main| image:: https://img.shields.io/badge/docs-main-blue.svg
   :target: https://plothist.readthedocs.io/en/latest/