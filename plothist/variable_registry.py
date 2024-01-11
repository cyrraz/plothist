# -*- coding: utf-8 -*-
"""
Collection of functions to manage the variable registry
"""
import yaml
import os
import warnings
import boost_histogram as bh
from plothist.histogramming import create_axis


def _check_if_variable_registry_exists(path):
    """
    Check if the variable registry file exists at the specified path.

    Parameters
    ----------
    path : str
        The path to the variable registry file.

    Returns
    -------
    None

    Raises
    ------
    RuntimeError
        If the variable registry file does not exist.
    """
    if not os.path.exists(path):
        if path == "./variable_registry.yaml":
            raise RuntimeError("Did you forgot to run create_variable_registry()?")


def _save_variable_registry(variable_registry, path="./variable_registry.yaml"):
    """
    Save the variable registry to a yaml file.

    Parameters
    ----------
    variable_registry : dict
        The variable registry to save.
    path : str, optional
        The path to the variable registry file (default is "./variable_registry.yaml").

    Returns
    -------
    None
    """

    with open(path, "w") as f:
        for key, value in variable_registry.items():
            yaml.safe_dump({key: value}, f, sort_keys=False)
            f.write("\n" * 2)


def create_variable_registry(
    variable_keys, path="./variable_registry.yaml", custom_dict=None, reset=False
):
    """
    Create the variable registry yaml file given a list of variable keys.
    It stores all the plotting information for each variable.

    It checks if the variable registry file exists. If not, it creates an empty file at the specified path.
    It then loads the existing variable registry, or creates an empty registry if it doesn't exist.
    For each variable in the input list, if the variable is not already in the registry or the reset flag is True,
    it adds the variable to the registry with default settings.
    Finally, it writes the updated variable registry back to the file.

    Default dictionary parameters of one variable in the yaml:

    name : str
        variable name in data.
    bins : int
        Number of bins, default is 50.
    range: list of two float
        Range of the variables, default is [min, max] of the data.
    label : str
        Label to display, default is variable name. Latex supported by surrounding the label with $label$.
    log : bool
        True if plot in logscale, default is False
    legend_location : str
        Default is best
    legend_ncols : int
        Default set to 1
    docstring : str
        Default is empty

    Can also not use the default dictionary and provide a custom one using the 'custom_dict' parameter.

    Parameters
    ----------
    variable_keys : list
        A list of variable keys to be registered.
    path : str, optional
        The path to the variable registry file (default is "./variable_registry.yaml").
    custom_dict : dict, optional
        A dictionary containing the plotting information for the variables. Default dictionary is the one described above.
    reset : bool, optional
        If True, the registry will be reset to default values for all variable keys (default is False).


    """

    if not os.path.exists(path):
        with open(path, "w") as f:
            pass

    with open(path, "r") as f:
        variable_registry = yaml.safe_load(f)
        if variable_registry is None:
            variable_registry = {}

        for variable_key in variable_keys:
            if variable_key not in variable_registry.keys() or reset:
                if custom_dict is not None:
                    variable_registry.update({variable_key: custom_dict})
                else:
                    variable_registry.update(
                        {
                            variable_key: {
                                "name": variable_key,
                                "bins": 50,
                                "range": ["min", "max"],
                                "label": variable_key,
                                "log": False,
                                "legend_location": "best",
                                "legend_ncols": 1,
                                "docstring": "",
                            }
                        }
                    )

    _save_variable_registry(variable_registry, path=path)


def get_variable_from_registry(variable_key, path="./variable_registry.yaml"):
    """
    This function retrieves the parameter information for a variable from the variable registry file specified by the 'path' parameter.
    It loads the variable registry file and returns the dictionary entry corresponding to the specified variable name.

    Parameters
    ----------
    variable_key : str
        The name of the variable for which to retrieve parameter information.
    path : str, optional
        The path to the variable registry file (default is "./variable_registry.yaml").

    Returns
    -------
    dict
        A dictionary containing the parameter information for the specified variable.

    See also
    --------
    create_variable_registry
    """

    _check_if_variable_registry_exists(path)

    with open(path, "r") as f:
        variable_registry = yaml.safe_load(f)
        return variable_registry[variable_key]


def update_variable_registry(
    dictionary, variable_keys=None, path="./variable_registry.yaml", overwrite=False
):
    """
    Update the variable registry file with a dictionary. Each key in the provided dictionnary will be added as parameters for each variable. If they are already in the variable information, they will be updated with the new values only if the overwrite flag is True.

    Parameters
    ----------
    dictionary : dict
        A dictionary containing the information to update the registry with.
    variable_keys : list
        A list of variable keys for which to update the registry. Default is None: all variables in the registry are updated.
    path : str, optional
        The path to the variable registry file (default is "./variable_registry.yaml").
    overwrite : bool, optional
        If True, the keys will be overwrite by the provided value in the dictonnary (default is False).

    Returns
    -------
    None
    """
    _check_if_variable_registry_exists(path)

    with open(path, "r") as f:
        variable_registry = yaml.safe_load(f)

    if variable_keys is None:
        variable_keys = list(variable_registry.keys())

    for variable_key in variable_keys:
        for key, value in dictionary.items():
            if key not in variable_registry[variable_key].keys() or overwrite:
                variable_registry[variable_key].update({key: value})

    _save_variable_registry(variable_registry, path=path)


def remove_variable_registry_parameters(
    parameters, variable_keys=None, path="./variable_registry.yaml"
):
    """
    Remove the specified parameters from the variable registry file.

    Parameters
    ----------
    parameters : list
        A list of parameters to remove from the variable keys.
    variable_keys : list
        A list of variable keys for which to remove the specified parameters from the registry. Default is None: all variables in the registry are updated.
    path : str, optional
        The path to the variable registry file (default is "./variable_registry.yaml").

    Returns
    -------
    None
    """
    _check_if_variable_registry_exists(path)

    with open(path, "r") as f:
        variable_registry = yaml.safe_load(f)

    if variable_keys is None:
        variable_keys = list(variable_registry.keys())

    for variable_key in variable_keys:
        for parameter in parameters:
            if parameter in variable_registry[variable_key].keys():
                _ = variable_registry[variable_key].pop(parameter)
            else:
                warnings.warn(
                    f"{parameter} parameter not present in the registry {path} for {variable_key}, skipping."
                )

    _save_variable_registry(variable_registry, path=path)


def update_variable_registry_ranges(
    data,
    variable_keys=None,
    path="./variable_registry.yaml",
    overwrite=False,
):
    """
    Update the range parameters for multiple variables in the variable registry file.

    Parameters
    ----------
    data : dict or pandas.DataFrame
        A dataset containing the data for the variables.
    variable_keys : list
        A list of variable keys for which to update the range parameters in the registry. The variable needs to have a bin and range properties in the registry. Default is None: all variables in the registry are updated.
    path : str, optional
        The path to the variable registry file (default is "./variable_registry.yaml").
    overwrite : bool, optional
        If True, the range parameters will be overwrite even if it's not equal to ["min", "max"] (default is False).

    Returns
    -------
    None

    Raises
    ------
    RuntimeError
        If the variable does not have a bins or range property in the registry.
    """
    _check_if_variable_registry_exists(path)

    if variable_keys is None:
        with open(path, "r") as f:
            variable_registry = yaml.safe_load(f)
        variable_keys = list(variable_registry.keys())

    for variable_key in variable_keys:
        variable = get_variable_from_registry(variable_key, path=path)
        if "bins" not in variable.keys() or "range" not in variable.keys():
            raise RuntimeError(
                f"Variable {variable_key} does not have a bins or range property in the registry {path}."
            )

        range = ["min", "max"] if overwrite else variable["range"]

        if range == ["min", "max"]:
            axis = create_axis(data[variable_key], variable["bins"], range)
            if isinstance(axis, bh.axis.Regular):
                update_variable_registry(
                    {"range": [float(axis.edges[0]), float(axis.edges[-1])]},
                    [variable_key],
                    path=path,
                    overwrite=True,
                )
