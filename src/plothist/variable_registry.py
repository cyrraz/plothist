"""
Collection of functions to manage the variable registry
"""

from __future__ import annotations

import os
import warnings

import boost_histogram as bh
import numpy as np
import yaml

from plothist.histogramming import create_axis


def _check_if_variable_registry_exists(path: str) -> None:
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
    if not os.path.exists(path) and path == "./variable_registry.yaml":
        raise RuntimeError("Did you forget to run create_variable_registry()?")


def _save_variable_registry(
    variable_registry: dict[str, dict], path: str = "./variable_registry.yaml"
) -> None:
    """
    Save the variable registry to a yaml file.

    Parameters
    ----------
    variable_registry : dict[str, dict]
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
    variable_keys: list[str],
    path: str = "./variable_registry.yaml",
    custom_dict: dict | None = None,
    reset: bool = False,
) -> None:
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
    range: tuple[float, float]
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
    variable_keys : list[str]
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

    with open(path) as f:
        variable_registry = yaml.safe_load(f)
        if variable_registry is None:
            variable_registry = {}

        for variable_key in variable_keys:
            if variable_key not in variable_registry or reset:
                if custom_dict is not None:
                    variable_registry.update({variable_key: custom_dict})
                else:
                    variable_registry.update(
                        {
                            variable_key: {
                                "name": variable_key,
                                "bins": "auto",
                                "range": ("min", "max"),
                                "label": variable_key,
                                "log": False,
                                "legend_location": "best",
                                "legend_ncols": 1,
                                "docstring": "",
                            }
                        }
                    )

    _save_variable_registry(variable_registry, path=path)


def get_variable_from_registry(
    variable_key: str, path: str = "./variable_registry.yaml"
) -> dict:
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

    with open(path) as f:
        variable_registry = yaml.safe_load(f)
        if "range" in variable_registry[variable_key] and isinstance(
            variable_registry[variable_key]["range"], list
        ):
            variable_registry[variable_key]["range"] = tuple(
                variable_registry[variable_key]["range"]
            )
        return variable_registry[variable_key]


def update_variable_registry(
    dictionary: dict,
    variable_keys: list[str] | None = None,
    path: str = "./variable_registry.yaml",
    overwrite: bool = False,
) -> None:
    """
    Update the variable registry file with a dictionary. Each key in the provided dictionary will be added as parameters for each variable. If they are already in the variable information, they will be updated with the new values only if the overwrite flag is True.

    Parameters
    ----------
    dictionary : dict
        A dictionary containing the information to update the registry with.
    variable_keys : list[str]
        A list of variable keys for which to update the registry. Default is None: all variables in the registry are updated.
    path : str, optional
        The path to the variable registry file (default is "./variable_registry.yaml").
    overwrite : bool, optional
        If True, the keys will be overwritten by the provided value in the dictionary (default is False).

    Returns
    -------
    None
    """
    _check_if_variable_registry_exists(path)

    with open(path) as f:
        variable_registry = yaml.safe_load(f)

    if variable_keys is None:
        variable_keys = list(variable_registry.keys())

    for variable_key in variable_keys:
        for key, value in dictionary.items():
            if key not in variable_registry[variable_key] or overwrite:
                variable_registry[variable_key].update({key: value})

    _save_variable_registry(variable_registry, path=path)


def remove_variable_registry_parameters(
    parameters: list[str],
    variable_keys: list[str] | None = None,
    path: str = "./variable_registry.yaml",
) -> None:
    """
    Remove the specified parameters from the variable registry file.

    Parameters
    ----------
    parameters : list[str]
        A list of parameters to remove from the variable keys.
    variable_keys : list[str]
        A list of variable keys for which to remove the specified parameters from the registry. Default is None: all variables in the registry are updated.
    path : str, optional
        The path to the variable registry file (default is "./variable_registry.yaml").

    Returns
    -------
    None
    """
    _check_if_variable_registry_exists(path)

    with open(path) as f:
        variable_registry = yaml.safe_load(f)

    if variable_keys is None:
        variable_keys = list(variable_registry.keys())

    for variable_key in variable_keys:
        for parameter in parameters:
            if parameter in variable_registry[variable_key]:
                _ = variable_registry[variable_key].pop(parameter)
            else:
                warnings.warn(
                    f"{parameter} parameter not present in the registry {path} for {variable_key}, skipping.",
                    stacklevel=2,
                )

    _save_variable_registry(variable_registry, path=path)


def update_variable_registry_ranges(*args, **kwargs):
    warnings.warn(
        "`update_variable_registry_ranges` is deprecated since v1.7.0 and will be removed in future versions. "
        "Use `update_variable_registry_binning` instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    return update_variable_registry_binning(*args, **kwargs)


def update_variable_registry_binning(
    data,
    variable_keys: list[str] | None = None,
    path: str = "./variable_registry.yaml",
    overwrite: bool = False,
) -> None:
    """
    Update both the bins and range parameters for multiple variables in the variable registry file.

    Parameters
    ----------
    data : numpy.ndarray or pandas.DataFrame
        A dataset containing the data for the variables.
    variable_keys : list[str]
        A list of variable keys for which to update the parameters in the registry.
        The variable needs to have a bin and range properties in the registry.
        Default is None: all variables in the registry are updated.
    path : str, optional
        The path to the variable registry file (default is "./variable_registry.yaml").
    overwrite : bool, optional
        If True, the bin and range parameters will be overwritten even if they differ from "auto" and ("min", "max") (default is False).

    Returns
    -------
    None

    Raises
    ------
    RuntimeError
        If the variable does not have a name, bins or range property in the registry.
    """
    _check_if_variable_registry_exists(path)

    if variable_keys is None:
        with open(path) as f:
            variable_registry = yaml.safe_load(f)
        variable_keys = list(variable_registry.keys())

    for variable_key in variable_keys:
        variable = get_variable_from_registry(variable_key, path=path)
        if not all(key in variable for key in ["bins", "range", "name"]):
            raise RuntimeError(
                f"Variable {variable_key} does not have a name, bins or range property in the registry {path}."
            )

        bins = "auto" if overwrite else variable["bins"]
        bin_number = len(np.histogram_bin_edges(data[variable["name"]], bins=bins)) - 1

        range_val = ("min", "max") if overwrite else variable["range"]

        if bins == "auto" or tuple(range_val) == ("min", "max"):
            axis = create_axis(
                bin_number,
                tuple(range_val),
                data[variable["name"]],
            )
            if isinstance(axis, bh.axis.Regular):
                update_variable_registry(
                    {
                        "bins": bin_number,
                        "range": (float(axis.edges[0]), float(axis.edges[-1])),
                    },
                    [variable_key],
                    path=path,
                    overwrite=True,
                )
