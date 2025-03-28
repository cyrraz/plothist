import glob
import os
import subprocess
import tempfile

import pytest

scripts = glob.glob("docs/examples/**/*.py", recursive=True)


@pytest.mark.parametrize("script", scripts)
def test_examples(script):
    original_directory = os.getcwd()
    with tempfile.TemporaryDirectory(dir=os.getcwd()) as tmpdirname:
        os.chdir(tmpdirname)
        script_name = os.path.basename(script)
        os.system(f"cp {original_directory}/{script} {script_name}")
        result = subprocess.run(["python", script_name], capture_output=True, text=True)
        os.chdir(original_directory)
        assert result.returncode == 0, (
            f"Script {script} failed with error: {result.stderr}"
        )
