from plothist import (
    get_dummy_data,
    create_variable_registry,
    get_variable_from_registry,
    update_variable_registry_ranges,
    update_variable_registry,
    remove_variable_registry_parameters,
)
from pytest import fail, warns, raises
import yaml
import os

registry_path = "registry.yaml"
variable_keys = ["variable_0", "variable_1", "variable_2"]


def test_variable_registry_warning():
    """
    Test variable registry creation.
    """
    if os.path.exists("variable_registry.yaml"):
        os.remove("variable_registry.yaml")

    with raises(RuntimeError) as err:
        get_variable_from_registry("variable_0")
    assert str(err.value) == "Did you forgot to run create_variable_registry()?"


def test_variable_registry_creation():
    """
    Test variable registry creation.
    """
    if os.path.exists("variable_registry.yaml"):
        os.remove("variable_registry.yaml")
    if os.path.exists("test.yaml"):
        os.remove("test.yaml")

    create_variable_registry(variable_keys)

    if not os.path.exists("variable_registry.yaml"):
        fail("variable_registry.yaml not created.")

    # With custom path
    create_variable_registry(variable_keys, path="test.yaml")
    if not os.path.exists("test.yaml"):
        fail("test.yaml not created.")


def test_variable_registry_info():
    """
    Test variable registry information.
    """

    create_variable_registry(variable_keys, path=registry_path, reset=True)

    for key in variable_keys:
        registry = get_variable_from_registry(key, path=registry_path)
        assert registry == {
            "name": key,
            "bins": 50,
            "range": ["min", "max"],
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
            "range": ["min", "max"],
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


def test_update_variable_registry_ranges():
    """
    Test variable registry range update.
    """
    df = get_dummy_data()

    # Test multiple conditions for missing properties
    create_variable_registry(
        variable_keys, path=registry_path, custom_dict={"bins": 50}, reset=True
    )

    with raises(RuntimeError) as err:
        update_variable_registry_ranges(df, variable_keys, path=registry_path)
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

    with raises(RuntimeError) as err:
        update_variable_registry_ranges(df, variable_keys, path=registry_path)
    assert (
        str(err.value)
        == f"Variable {variable_keys[0]} does not have a name, bins or range property in the registry {registry_path}."
    )

    create_variable_registry(
        variable_keys,
        path=registry_path,
        custom_dict={"bins": 50, "range": [-1, 1]},
        reset=True,
    )

    with raises(RuntimeError) as err:
        update_variable_registry_ranges(df, variable_keys, path=registry_path)
    assert (
        str(err.value)
        == f"Variable {variable_keys[0]} does not have a name, bins or range property in the registry {registry_path}."
    )

    create_variable_registry(
        variable_keys,
        path=registry_path,
        custom_dict={"name": "test", "range": [-1, 1]},
        reset=True,
    )

    with raises(RuntimeError) as err:
        update_variable_registry_ranges(df, variable_keys, path=registry_path)
    assert (
        str(err.value)
        == f"Variable {variable_keys[0]} does not have a name, bins or range property in the registry {registry_path}."
    )

    # Standard registry creation
    create_variable_registry(variable_keys, path=registry_path, reset=True)

    update_variable_registry_ranges(df, variable_keys, path=registry_path)

    for key in variable_keys:
        registry = get_variable_from_registry(key, path=registry_path)
        if key == "variable_0":
            assert registry["range"] == [-10.55227774892869, 10.04658448558009]
        elif key == "variable_1":
            assert registry["range"] == [-9.32198527389102, 10.320677227899562]
        elif key == "variable_2":
            assert registry["range"] == [-17.983319077507936, 16.84354525625102]

    # Change range value by hand for variable_0
    registry = get_variable_from_registry("variable_0", path=registry_path)
    registry["range"] = [-1, 1]
    with open(registry_path, "w") as f:
        yaml.safe_dump({"variable_0": registry}, f, sort_keys=False)
        f.write("\n" * 2)

    # Check the new value
    registry = get_variable_from_registry("variable_0", path=registry_path)
    assert registry["range"] == [-1, 1]

    # Range values shouldn't be updated as overwrite=False
    update_variable_registry_ranges(df, ["variable_0"], path=registry_path)

    registry = get_variable_from_registry("variable_0", path=registry_path)
    assert registry["range"] == [-1, 1]

    # Range values should be updated as overwrite=True
    update_variable_registry_ranges(
        df, ["variable_0"], path=registry_path, overwrite=True
    )

    registry = get_variable_from_registry("variable_0", path=registry_path)
    assert registry["range"] == [-10.55227774892869, 10.04658448558009]

    # Same tests as above but with update_variable_registry() function
    update_variable_registry(
        {"range": [-1, 1]},
        ["variable_0"],
        path=registry_path,
    )

    registry = get_variable_from_registry("variable_0", path=registry_path)
    assert registry["range"] == [-10.55227774892869, 10.04658448558009]

    update_variable_registry(
        {"range": [-1, 1]},
        ["variable_0"],
        path=registry_path,
        overwrite=True,
    )

    registry = get_variable_from_registry("variable_0", path=registry_path)
    assert registry["range"] == [-1, 1]


def test_updating_variable_registry():
    """
    Test variable registry update.
    """

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
            "range": ["min", "max"],
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
