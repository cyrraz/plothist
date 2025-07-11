import pytest

from plothist.test_helpers import run_script_and_get_object


def test_run_script_and_get_object_file_not_found() -> None:
    """
    Check that FileNotFoundError is raised when using run_script_and_get_object() with invalid path.
    """
    non_existent_path = "non_existent_script.py"

    with pytest.raises(
        FileNotFoundError, match=f"Script file not found: {non_existent_path}"
    ):
        run_script_and_get_object(non_existent_path, "some_variable")
