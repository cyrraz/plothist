# -*- coding: utf-8 -*-
"""
Collection of functions to manage the variable registry
"""
import yaml
import os
import boost_histogram as bh
from plothist.plotters import create_axis


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


def create_variable_registry(variables, path="./variable_registry.yaml", custom_dict=None, reset=False):
    """Create the variable registry yaml file given a list of variables.
    It stores all the plotting information for each variable.

    It checks if the variable registry file exists. If not, it creates an empty file at the specified path.
    It then loads the existing variable registry, or creates an empty registry if it doesn't exist.
    For each variable in the input list, if the variable is not already in the registry or the reset flag is True,
    it adds the variable to the registry with default settings.
    Finally, it writes the updated variable registry back to the file.

    Default dictionnary parameters of one variable in the yaml:

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

    Parameters
    ----------
    variables : list
        A list of variable names to be registered.
    path : str, optional
        The path to the variable registry file (default is "./variable_registry.yaml").
    reset : bool, optional
        If True, the registry will be reset to default values for all variables (default is False).


    """

    if not os.path.exists(path):
        with open(path, "w") as f:
            pass

    with open(path, "r") as f:
        variable_registry = yaml.safe_load(f)
        if variable_registry is None:
            variable_registry = {}

        for variable in variables:
            if variable not in variable_registry.keys() or reset:
                if custom_dict is not None:
                    variable_registry.update({variable : custom_dict})
                else:
                    variable_registry.update(
                        {
                            variable: {
                                "name": variable,
                                "bins": 50,
                                "range": ["min", "max"],
                                "label": variable,
                                "log": False,
                                "legend_location": "best",
                                "legend_ncols": 1,
                                "docstring": "",
                            }
                        }
                    )

    _save_variable_registry(variable_registry, path=path)


def get_variable_from_registry(variable, path="./variable_registry.yaml"):
    """
    This function retrieves the parameter information for a variable from the variable registry file specified by the 'path' parameter.
    It loads the variable registry file and returns the dictionary entry corresponding to the specified variable name.

    Parameters
    ----------
    variable : str
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
        return variable_registry[variable]


def update_variable_registry(
    variable_key, x_min, x_max, path="./variable_registry.yaml"
):
    # TODO: bins could be a list for 2D uneven binning
    # TODO: extend updating function
    """
    Update the range parameter for a variable in the variable registry file.

    Parameters
    ----------
    variable_key : str
        The key identifier of the variable to update in the registry.
    x_min : float
        The new minimum value for the range of the variable.
    x_max : float
        The new maximum value for the range of the variable.
    path : str, optional
        The path to the variable registry file (default is "./variable_registry.yaml").

    Returns
    -------
    None

    See Also
    --------
    create_variable_registry
    """
    _check_if_variable_registry_exists(path)

    with open(path, "r") as f:
        variable_registry = yaml.safe_load(f)
    variable_registry[variable_key]["range"] = [x_min, x_max]

    _save_variable_registry(variable_registry, path=path)


def update_variable_registry_ranges(data, variables, path="./variable_registry.yaml"):
    """
    Update the range parameters for multiple variables in the variable registry file.

    Parameters
    ----------
    data : dict
        A dictionary containing the data for the variables.
    variables : list
        A list of variable keys for which to update the range parameters in the registry. The variable needs to have a bin and range properties in the registry.
    path : str, optional
        The path to the variable registry file (default is "./variable_registry.yaml").

    Returns
    -------
    None

    Raises
    ------
    NotImplementedError
        If non-regular binning is encountered in the registry.

    See Also
    --------
    get_variable_from_registry, update_variable_registry, create_axis

    """
    for variable_key in variables:
        variable = get_variable_from_registry(variable_key, path=path)
        try:
            bins = variable["bins"]
            range = variable["range"]
        except:
            raise RuntimeError(
                f"Variable {variable_key} does not have a bins or range property in the registry."
            )
        axis = create_axis(data[variable_key], bins, range)
        if isinstance(axis, bh.axis.Regular):
            update_variable_registry(
                variable_key, float(axis.edges[0]), float(axis.edges[-1]), path=path
            )
        else:
            raise NotImplemented(
                f"Only regular binning allowed in registry. {type(axis)}"
            )
