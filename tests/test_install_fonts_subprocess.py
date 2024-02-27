import subprocess

def print_json_fonts():
    import json
    with open("/home/runner/.cache/matplotlib/fontlist-v330.json", "r") as f:
        data = json.load(f)
        for datakey, datavalue in data.items():
            if datakey == "ttflist":
                for elt in datavalue:
                    for key, value in elt.items():
                        if key == "name":
                            if "Latin Modern" in value:
                                print("Found latin modern font in the json file: ", elt)
                                return

def test_install_latin_modern_fonts():
    subprocess.run(["python", "/opt/hostedtoolcache/Python/3.8.18/x64/lib/python3.8/site-packages/plothist/scripts/install_latin_modern_fonts.py"])

    try:
        print_json_fonts()
        print("fonts in the json  ")
    except:
        from matplotlib.font_manager import _load_fontmanager
        fm = _load_fontmanager(try_read_cache=False)
        print_json_fonts()
        print("fonts in the json.")
        print(sorted(fm.get_font_names()), " fm.get_font_names()")

    from matplotlib.font_manager import findfont, get_font_names
    print(sorted(get_font_names()))

    print("Now reloading matplotlib to see if the fonts are available.")
    import importlib
    importlib.reload(matplotlib.font_manager)
    print("Now the fonts should be available???")

    print_json_fonts()


    print("\n")
    from matplotlib.font_manager import findfont, get_font_names
    print(sorted(get_font_names()))
    for font in get_font_names():
        print(findfont(font))
    failed = True
    for font_type in ["Math", "Sans", "Roman"]:
        try:
            print(findfont(f"Latin Modern {font_type}", fallback_to_default=False))
            failed = False
            print(f"The font Latin Modern {font_type} was found with font_directory={font_directory}.")
        except ValueError:
            # failed = True
            print(f"The font Latin Modern {font_type} was not found.")
        try:
            print(findfont(f"Latin Modern {font_type}", fallback_to_default=False, fontext="otf"))
            failed = False
            print(f"The font Latin Modern {font_type} was found with font_directory={font_directory}.")
        except ValueError:
            # failed = True
            print(f"The font Latin Modern {font_type} was not found.")
        try:
            print(findfont(f"Latin Modern {font_type}", fallback_to_default=False, rebuild_if_missing=True))
            failed = False
            print(f"The font Latin Modern {font_type} was found with font_directory={font_directory}.")
        except ValueError:
            # failed = True
            print(f"The font Latin Modern {font_type} was not found.")

    assert not failed