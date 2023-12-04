import os
import yaml
import subprocess
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "--print_code", action="store_true", help="Print the code of the examples"
)
args = parser.parse_args()

# Define folders
plothist_folder = os.path.dirname(os.path.realpath(__file__)) + "/../.."
example_folder = plothist_folder + "/docs/examples"
img_folder = plothist_folder + "/docs/img"
temp_img_folder = plothist_folder + "/docs/temp_img"

python_files = [
    file
    for root, dirs, files in os.walk(example_folder)
    for file in files
    if file.endswith(".py")
]
python_files.sort()

print(
    "Which python script do you want to relauch? (ex: 1 2 4 ... [OR] 1d model 2d color [OR] all (just press enter for all))"
)
for k_python, python_file in enumerate(python_files):
    print(f"\t{f'{k_python}':<3} - {python_file}")
k_plots = input("> ")
if k_plots == "":
    k_plots = "all"

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
    os.mkdir(temp_img_folder)

# Get the metadata for the svg files
with open(plothist_folder + "/plothist/scripts/metadata.yaml", "r") as f:
    svg_metadata = yaml.safe_load(f)
svg_metadata = "metadata=" + str(svg_metadata)

import matplotlib.pyplot as plt

# Set figure.max_open_warning to a large number to avoid warnings
plt.rcParams["figure.max_open_warning"] = 1000

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

        if args.print_code:
            print("\n" * 10 + file_code)

        subprocess.run(["python", "-c", file_code], cwd=temp_img_folder)

# Move the svg files to the img folder
for file in os.listdir(temp_img_folder):
    if file.endswith(".svg"):
        subprocess.run(["mv", os.path.join(temp_img_folder, file), img_folder])

# Remove the temp folder
subprocess.run(["rm", "-rf", temp_img_folder])
