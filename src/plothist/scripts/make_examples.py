import os
import yaml
import subprocess
import plothist
import hashlib
import warnings
import sys


_matplotlib_version = "3.10.0"
_numpy_version = "2.0.0"


def make_examples(no_input=False, check_svg=False, print_code=False):
    """
    This function can redo automatically all the examples from the documentation. Only works with python 3.9 or higher.

    Parameters
    ----------
    no_input : bool, optional
        If True, the function will not ask for any input and will relaunch all the python files.
    check_svg : bool, optional
        If True, the function will check that the svg files have not changed after the relaunch.
    print_code : bool, optional
        If True, the function will print the code that will be executed for each python file.

    Raises
    ------
    FileNotFoundError
        If the example or img folder does not exist, the function will raise a FileNotFoundError.
    """

    import matplotlib

    if tuple(map(int, matplotlib.__version__.split("."))) < tuple(
        map(int, _matplotlib_version.split("."))
    ):
        warnings.warn(
            f"svg behavior is not consistent across matplotlib versions. Please run this script with matplotlib {_matplotlib_version} or higher. Skipping.",
            stacklevel=2,
        )
        return 1

    import numpy

    if tuple(map(int, numpy.__version__.split("."))) < tuple(
        map(int, _numpy_version.split("."))
    ):
        warnings.warn(
            f"svg behavior is not consistent across numpy versions. Please run this script with numpy {_numpy_version} or higher. Skipping.",
            stacklevel=2,
        )
        return 1

    plothist_folder = (
        plothist.__path__[0]
        if os.environ.get("PLOTHIST_PATH") is None
        else os.environ.get("PLOTHIST_PATH")
    )

    example_folder = plothist_folder + "/../../docs/examples"
    img_folder = plothist_folder + "/../../docs/img"

    if not os.path.exists(example_folder) or not os.path.exists(img_folder):
        raise FileNotFoundError(
            f"Could not find the example {example_folder} or img {img_folder} folder for the documentation.\nIf you installed plothist from source using flit, please run `export PLOTHIST_PATH=path/to/plothist` before launching the script."
        )

    temp_img_folder = plothist_folder + "/docs/temp_img"

    # Get all python files in the example folder
    python_files = [
        file
        for root, dirs, files in os.walk(example_folder)
        for file in files
        if file.endswith(".py")
    ]
    python_files.sort()

    if no_input:
        k_plots = "all"
    else:
        # Ask which python files to relaunch
        print(
            "Which python script do you want to relauch? (ex: 1 2 4 ... [OR] 1d model 2d color [OR] all (just press enter for all))"
        )
        for k_python, python_file in enumerate(python_files):
            print(f"\t{f'{k_python}':<3} - {python_file}")
        k_plots = input("> ")

    if k_plots == "":
        k_plots = "all"

    # Get the list of python files to relaunch
    plots_to_redo = []
    for k_plot in k_plots.split(" "):
        if k_plot == "all":
            plots_to_redo = python_files[:]
            break
        elif k_plot in ["1d", "2d", "model", "color"]:
            plots_to_redo.extend(
                [
                    python_file
                    for python_file in python_files
                    if python_file.startswith(k_plot)
                ]
            )
        else:
            plots_to_redo.append(python_files[int(k_plot)])

    # Temp image folder
    if not os.path.exists(temp_img_folder):
        os.makedirs(temp_img_folder, exist_ok=True)

    # Get the metadata for the svg files
    if not os.path.exists(plothist_folder + "/.svg_metadata.yaml"):
        subprocess.run(
            [
                "wget",
                "-O",
                plothist_folder + "/.svg_metadata.yaml",
                "https://raw.githubusercontent.com/0ctagon/plothist-utils/dbf86375576fa2ca5c35ab3a35bba1ab7715a186/.svg_metadata.yaml",
            ]
        )

    with open(plothist_folder + "/.svg_metadata.yaml", "r") as f:
        svg_metadata = yaml.safe_load(f)

    svg_metadata = "metadata=" + str(svg_metadata)

    if check_svg:
        from pytest import fail

        img_hashes = {}
        for file in os.listdir(img_folder):
            if file.endswith(".svg"):
                with open(os.path.join(img_folder, file), "r") as f:
                    img_hashes[file] = hashlib.sha256(f.read().encode()).hexdigest()

    # Iterate through all subfolders and files in the source folder
    for root, dirs, files in os.walk(example_folder):
        for file in files:
            if file not in plots_to_redo:
                continue

            print(f"Redoing {file}")
            file_path = os.path.join(root, file)
            file_code = ""

            with open(file_path, "r") as f:
                for line in f:
                    if "savefig" in line:
                        if file == "matplotlib_vs_plothist_style.py":
                            line = (
                                "    plt.rcParams['svg.hashsalt'] = '8311311'\n" + line
                            )
                        line = line.replace(
                            "savefig(",
                            f"savefig({svg_metadata}, fname=",
                        )
                    file_code += line

            if print_code:
                print("\n" * 10 + file_code)

            result = subprocess.run(
                ["python", "-c", file_code],
                cwd=temp_img_folder,
                capture_output=True,
                text=True,
            )
            if result.returncode != 0 and check_svg:
                fail(f"Error while redoing {file}:\n{result.stderr}\n{result.stdout}")

    # Move the svg files to the img folder
    for file in os.listdir(temp_img_folder):
        if file.endswith(".svg"):
            subprocess.run(["mv", os.path.join(temp_img_folder, file), img_folder])

    # Remove the temp folder
    subprocess.run(["rm", "-rf", temp_img_folder])

    # Check that the svg files have not changed
    if check_svg:
        new_img_hashes = {}
        for file in os.listdir(img_folder):
            if file.endswith(".svg"):
                with open(os.path.join(img_folder, file), "r") as f:
                    new_img_hashes[file] = hashlib.sha256(f.read().encode()).hexdigest()

        # Check that the hashes are the same and print the ones that are different
        changed_img = []
        for file, file_hash in img_hashes.items():
            if new_img_hashes[file] != file_hash:
                changed_img.append(file)
        if changed_img:
            changed_img.sort()
            fail(
                f"The following images in the doc have changed [{len(changed_img)} out of {len(img_hashes)}]:\n{', '.join(changed_img)}.\nPlease run `plothist_make_examples`, check the new images and commit them if they are correct."
            )
        if len(new_img_hashes) != len(img_hashes):
            fail(
                f"The number of images has changed. Please run `plothist_make_examples`, check the new images and commit them if they are correct. New images:\n{set(new_img_hashes.keys()) - set(img_hashes.keys())}"
            )


if __name__ == "__main__":
    make_examples()
