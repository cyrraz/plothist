from __future__ import annotations

import os

import pytest
import yaml
from numpy import histogram_bin_edges
from plothist_utils import get_dummy_data

from plothist import (
    create_variable_registry,
    get_variable_from_registry,
    remove_variable_registry_parameters,
    update_variable_registry,
    update_variable_registry_binning,
    update_variable_registry_ranges,
)

variable_keys = ["variable_0", "variable_1", "variable_2"]


def test_variable_registry_warning() -> None:
    """
    Test variable registry creation. Skips the test if the default registry file is already present,
    to avoid interfering with existing data.
    """
    default_registry_path = "./variable_registry.yaml"

    if os.path.exists(default_registry_path):
        pytest.skip("Default registry exists; skipping to avoid deleting user data.")

    with pytest.raises(RuntimeError) as err:
        get_variable_from_registry("variable_0")

    assert str(err.value) == "Did you forget to run create_variable_registry()?"


def test_variable_registry_creation() -> None:
    """
    Test variable registry creation.
    """
    registry_path = "./_test_variable_registry_creation.yaml"
    create_variable_registry(variable_keys, path=registry_path)
    if not os.path.exists(registry_path):
        pytest.fail("Variable registry not created.")

    os.remove(registry_path)


def test_variable_registry_info() -> None:
    """
    Test variable registry information.
    """
    registry_path = "./_test_variable_registry_info.yaml"
    create_variable_registry(variable_keys, path=registry_path, reset=True)

    for key in variable_keys:
        registry = get_variable_from_registry(key, path=registry_path)
        assert registry == {
            "name": key,
            "bins": 50,
            "range": ("min", "max"),
            "label": key,
            "log": False,
            "legend_location": "best",
            "legend_ncols": 1,
            "docstring": "",
        }

    # The registry is not overwritten by the custom_dict as reset=False
    create_variable_registry(
        variable_keys, path=registry_path, custom_dict={"name": key, "text": "test"}
    )

    for key in variable_keys:
        registry = get_variable_from_registry(key, path=registry_path)
        assert registry == {
            "name": key,
            "bins": 50,
            "range": ("min", "max"),
            "label": key,
            "log": False,
            "legend_location": "best",
            "legend_ncols": 1,
            "docstring": "",
        }

    # The registry is overwritten by the custom_dict as reset=True
    create_variable_registry(
        variable_keys, path=registry_path, custom_dict={"text": "test"}, reset=True
    )

    for key in variable_keys:
        registry = get_variable_from_registry(key, path=registry_path)
        assert registry == {"text": "test"}

    os.remove(registry_path)


def test_update_variable_registry_ranges() -> None:
    """
    Test variable registry range update.
    """
    dummy_data = get_dummy_data()

    registry_path = "./_test_variable_registry_ranges.yaml"

    # Test multiple conditions for missing properties
    create_variable_registry(
        variable_keys, path=registry_path, custom_dict={"bins": 50}, reset=True
    )

    with pytest.raises(RuntimeError) as err:
        update_variable_registry_ranges(dummy_data, variable_keys, path=registry_path)
    assert (
        str(err.value)
        == f"Variable {variable_keys[0]} does not have a name, bins or range property in the registry {registry_path}."
    )

    create_variable_registry(
        variable_keys, path=registry_path, custom_dict={"name": "test"}, reset=True
    )

    with pytest.raises(RuntimeError) as err:
        update_variable_registry_binning(dummy_data, variable_keys, path=registry_path)
    assert (
        str(err.value)
        == f"Variable {variable_keys[0]} does not have a name, bins or range property in the registry {registry_path}."
    )

    create_variable_registry(
        variable_keys, path=registry_path, custom_dict={"range": (-1, 1)}, reset=True
    )

    with pytest.raises(RuntimeError) as err:
        update_variable_registry_binning(dummy_data, variable_keys, path=registry_path)
    assert (
        str(err.value)
        == f"Variable {variable_keys[0]} does not have a name, bins or range property in the registry {registry_path}."
    )

    create_variable_registry(
        variable_keys,
        path=registry_path,
        custom_dict={"bins": 50, "name": "test"},
        reset=True,
    )

    with pytest.raises(RuntimeError) as err:
        update_variable_registry_ranges(dummy_data, variable_keys, path=registry_path)
    assert (
        str(err.value)
        == f"Variable {variable_keys[0]} does not have a name, bins or range property in the registry {registry_path}."
    )

    create_variable_registry(
        variable_keys,
        path=registry_path,
        custom_dict={"bins": 50, "range": (-1, 1)},
        reset=True,
    )

    with pytest.raises(RuntimeError) as err:
        update_variable_registry_ranges(dummy_data, variable_keys, path=registry_path)
    assert (
        str(err.value)
        == f"Variable {variable_keys[0]} does not have a name, bins or range property in the registry {registry_path}."
    )

    create_variable_registry(
        variable_keys,
        path=registry_path,
        custom_dict={"name": "test", "range": (-1, 1)},
        reset=True,
    )

    with pytest.raises(RuntimeError) as err:
        update_variable_registry_ranges(dummy_data, variable_keys, path=registry_path)
    assert (
        str(err.value)
        == f"Variable {variable_keys[0]} does not have a name, bins or range property in the registry {registry_path}."
    )

    # Standard registry creation
    create_variable_registry(variable_keys, path=registry_path, reset=True)

    update_variable_registry_ranges(dummy_data, variable_keys, path=registry_path)

    for key in variable_keys:
        registry = get_variable_from_registry(key, path=registry_path)
        if key == "variable_0":
            assert registry["range"] == (-10.55227774892869, 10.04658448558009)
        elif key == "variable_1":
            assert registry["range"] == (-9.32198527389102, 10.320677227899562)
        elif key == "variable_2":
            assert registry["range"] == (-17.983319077507936, 16.84354525625102)

    # Change range value by hand for variable_0
    registry = get_variable_from_registry("variable_0", path=registry_path)
    registry["range"] = (-1, 1)
    with open(registry_path, "w") as f:
        yaml.safe_dump({"variable_0": registry}, f, sort_keys=False)
        f.write("\n" * 2)

    # Check the new value
    registry = get_variable_from_registry("variable_0", path=registry_path)
    assert registry["range"] == (-1, 1)

    # Range values shouldn't be updated as overwrite=False
    update_variable_registry_ranges(dummy_data, ["variable_0"], path=registry_path)

    registry = get_variable_from_registry("variable_0", path=registry_path)
    assert registry["range"] == (-1, 1)

    # Range values should be updated as overwrite=True
    update_variable_registry_ranges(
        dummy_data, ["variable_0"], path=registry_path, overwrite=True
    )

    registry = get_variable_from_registry("variable_0", path=registry_path)
    assert registry["range"] == (-10.55227774892869, 10.04658448558009)

    # Same tests as above but with update_variable_registry() function
    update_variable_registry(
        {"range": (-1, 1)},
        ["variable_0"],
        path=registry_path,
    )

    registry = get_variable_from_registry("variable_0", path=registry_path)
    assert registry["range"] == (-10.55227774892869, 10.04658448558009)

    update_variable_registry(
        {"range": (-1, 1)},
        ["variable_0"],
        path=registry_path,
        overwrite=True,
    )

    registry = get_variable_from_registry("variable_0", path=registry_path)
    assert registry["range"] == (-1, 1)

    update_variable_registry(
        {"range": (-2, 2)},
        None,
        path=registry_path,
        overwrite=True,
    )

    registry = get_variable_from_registry("variable_0", path=registry_path)
    assert registry["range"] == (-2, 2)

    os.remove(registry_path)


def test_update_variable_registry_binning() -> None:
    """
    Test variable registry binning update.
    """
    dummy_data = get_dummy_data()

    registry_path = "./_test_variable_registry_binning.yaml"

    # Test multiple conditions for missing properties
    create_variable_registry(
        variable_keys, path=registry_path, custom_dict={"bins": 50}, reset=True
    )

    with pytest.raises(RuntimeError) as err:
        update_variable_registry_binning(dummy_data, variable_keys, path=registry_path)
    assert (
        str(err.value)
        == f"Variable {variable_keys[0]} does not have a name, bins or range property in the registry {registry_path}."
    )

    create_variable_registry(
        variable_keys, path=registry_path, custom_dict={"name": "test"}, reset=True
    )

    with pytest.raises(RuntimeError) as err:
        update_variable_registry_binning(dummy_data, variable_keys, path=registry_path)
    assert (
        str(err.value)
        == f"Variable {variable_keys[0]} does not have a name, bins or range property in the registry {registry_path}."
    )

    create_variable_registry(
        variable_keys, path=registry_path, custom_dict={"range": (-1, 1)}, reset=True
    )

    with pytest.raises(RuntimeError) as err:
        update_variable_registry_binning(dummy_data, variable_keys, path=registry_path)
    assert (
        str(err.value)
        == f"Variable {variable_keys[0]} does not have a name, bins or range property in the registry {registry_path}."
    )

    create_variable_registry(
        variable_keys,
        path=registry_path,
        custom_dict={"bins": 50, "name": "test"},
        reset=True,
    )

    with pytest.raises(RuntimeError) as err:
        update_variable_registry_binning(dummy_data, variable_keys, path=registry_path)
    assert (
        str(err.value)
        == f"Variable {variable_keys[0]} does not have a name, bins or range property in the registry {registry_path}."
    )

    create_variable_registry(
        variable_keys,
        path=registry_path,
        custom_dict={"bins": 50, "range": (-1, 1)},
        reset=True,
    )

    with pytest.raises(RuntimeError) as err:
        update_variable_registry_binning(dummy_data, variable_keys, path=registry_path)
    assert (
        str(err.value)
        == f"Variable {variable_keys[0]} does not have a name, bins or range property in the registry {registry_path}."
    )

    create_variable_registry(
        variable_keys,
        path=registry_path,
        custom_dict={"name": "test", "range": (-1, 1)},
        reset=True,
    )

    with pytest.raises(RuntimeError) as err:
        update_variable_registry_binning(dummy_data, variable_keys, path=registry_path)
    assert (
        str(err.value)
        == f"Variable {variable_keys[0]} does not have a name, bins or range property in the registry {registry_path}."
    )

    # Standard registry creation
    create_variable_registry(variable_keys, path=registry_path, reset=True)

    update_variable_registry_binning(dummy_data, variable_keys, path=registry_path)

    for key in variable_keys:
        registry = get_variable_from_registry(key, path=registry_path)
        assert registry["bins"] == (
            len(histogram_bin_edges(dummy_data[key], bins="auto")) - 1
        )

    # Change bins value by hand for variable_0
    registry = get_variable_from_registry("variable_0", path=registry_path)
    registry["bins"] = 20
    with open(registry_path, "w") as f:
        yaml.safe_dump({"variable_0": registry}, f, sort_keys=False)
        f.write("\n" * 2)

    # Check the new value
    registry = get_variable_from_registry("variable_0", path=registry_path)
    assert registry["bins"] == 20

    # Range values shouldn't be updated as overwrite=False
    update_variable_registry_binning(dummy_data, ["variable_0"], path=registry_path)

    registry = get_variable_from_registry("variable_0", path=registry_path)
    assert registry["bins"] == 20

    # Range values should be updated as overwrite=True
    update_variable_registry_binning(
        dummy_data, ["variable_0"], path=registry_path, overwrite=True
    )

    registry = get_variable_from_registry("variable_0", path=registry_path)
    assert (
        registry["bins"]
        == len(histogram_bin_edges(dummy_data["variable_0"], bins="auto")) - 1
    )

    # Same tests as above but with update_variable_registry() function
    update_variable_registry(
        {"bins": 20},
        ["variable_0"],
        path=registry_path,
    )

    registry = get_variable_from_registry("variable_0", path=registry_path)
    assert (
        registry["bins"]
        == len(histogram_bin_edges(dummy_data["variable_0"], bins="auto")) - 1
    )

    update_variable_registry(
        {"bins": 20},
        ["variable_0"],
        path=registry_path,
        overwrite=True,
    )

    registry = get_variable_from_registry("variable_0", path=registry_path)
    assert registry["bins"] == 20

    update_variable_registry(
        {"bins": 30},
        None,
        path=registry_path,
        overwrite=True,
    )

    registry = get_variable_from_registry("variable_0", path=registry_path)
    assert registry["bins"] == 30

    os.remove(registry_path)


def test_updating_variable_registry() -> None:
    """
    Test variable registry update.
    """

    registry_path = "./_test_variable_registry_update.yaml"

    create_variable_registry(variable_keys, path=registry_path, reset=True)

    new_properties = {
        "text": "default_text",
        "more_info": None,
        "new_property": False,
        "custom_list": [1, "a", True],
        "custom_value": 0,
    }

    update_variable_registry(new_properties, variable_keys, path=registry_path)

    for key in variable_keys:
        registry = get_variable_from_registry(key, path=registry_path)
        assert registry == {
            "name": key,
            "bins": 50,
            "range": ("min", "max"),
            "label": key,
            "log": False,
            "legend_location": "best",
            "legend_ncols": 1,
            "docstring": "",
            "text": "default_text",
            "more_info": None,
            "new_property": False,
            "custom_list": [1, "a", True],
            "custom_value": 0,
        }

    remove_variable_registry_parameters(
        ["range", "log", "legend_ncols", "new_property"],
        variable_keys,
        path=registry_path,
    )

    for key in variable_keys:
        registry = get_variable_from_registry(key, path=registry_path)
        assert registry == {
            "name": key,
            "bins": 50,
            "label": key,
            "legend_location": "best",
            "docstring": "",
            "text": "default_text",
            "more_info": None,
            "custom_list": [1, "a", True],
            "custom_value": 0,
        }

    os.remove(registry_path)


def test_remove_variable_registry_parameters_warning() -> None:
    """
    Test that removing parameters from the variable registry raises a warning
    if the parameter is not present in the registry.
    """
    registry_path = "./_test_variable_registry_remove_warning.yaml"

    create_variable_registry(variable_keys, path=registry_path)
    remove_variable_registry_parameters(
        ["bins"], variable_keys=None, path=registry_path
    )

    with pytest.warns(
        UserWarning,
        match=f"bins parameter not present in the registry {registry_path} for variable_0, skipping.",
    ):
        remove_variable_registry_parameters(
            ["bins"], variable_keys=["variable_0"], path=registry_path
        )

    os.remove(registry_path)


def test_update_variable_registry_ranges_all_keys() -> None:
    """
    Test update of variable registry with variable_keys=None
    """
    dummy_data = get_dummy_data()

    registry_path = "./_test_variable_registry_update_all_keys.yaml"

    create_variable_registry(variable_keys, path=registry_path)
    update_variable_registry_ranges(dummy_data, variable_keys=None, path=registry_path)

    for key in variable_keys:
        variable = get_variable_from_registry(key, path=registry_path)
        assert pytest.approx(variable["range"][0]) == dummy_data[key].min()
        assert pytest.approx(variable["range"][1]) == dummy_data[key].max()

    os.remove(registry_path)


def test_update_variable_registry_binning_all_keys() -> None:
    """
    Test update of variable registry with variable_keys=None
    """
    dummy_data = get_dummy_data()

    registry_path = "./_test_variable_registry_update_all_keys.yaml"

    create_variable_registry(variable_keys, path=registry_path)
    update_variable_registry_binning(dummy_data, variable_keys=None, path=registry_path)

    for key in variable_keys:
        variable = get_variable_from_registry(key, path=registry_path)
        assert (
            pytest.approx(variable["bins"])
            == len(histogram_bin_edges(dummy_data[key], bins="auto")) - 1
        )

    os.remove(registry_path)
