import subprocess
import pkg_resources
import os
import platform

def install_fonts() -> None:
    script_path = pkg_resources.resource_filename(__name__, 'install_latin_modern_fonts.sh')

    try:
        subprocess.run(['bash', script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running Bash script to install the fonts: {e}")
        return 0

    if platform.system() == "Darwin": # MacOS
        subprocess.run(f"mv ~/.fonts/latin*  /Users/{os.getlogin()}/Library/Fonts/", shell=True)
        try:
            subprocess.run("rm ~/.matplotlib/fontlist-v330.json", shell=True)
        except:
            print("Error removing ~/.matplotlib/fontlist-v330.json. Try to find the correct fontlist-XXX.json file and remove it manually.")




if __name__ == '__main__':
    install_fonts()