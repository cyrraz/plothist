def test_install_latin_modern_fonts_test():
    """
    Test install_latin_modern_fonts.
    """


    from matplotlib.font_manager import findfont
    print(findfont("DejaVuSerif", fallback_to_default=True))
    print(findfont("www", fallback_to_default=True))

    failed = True

    for font_type in ["Math", "Sans", "Roman"]:
        try:
            print(findfont(f"Latin Modern {font_type}", fallback_to_default=False))
            failed = False
            print(f"The font Latin Modern {font_type} was found.")
        except ValueError:
            # failed = True
            print(f"The font Latin Modern {font_type} was not found.")
        try:
            print(findfont(f"Latin Modern {font_type}", fallback_to_default=False, fontext="otf"))
            failed = False
            print(f"The font Latin Modern {font_type} was found.")
        except ValueError:
            # failed = True
            print(f"The font Latin Modern {font_type} was not found.")
        try:
            print(findfont(f"Latin Modern {font_type}", fallback_to_default=False, rebuild_if_missing=True))
            failed = False
            print(f"The font Latin Modern {font_type} was found.")
        except ValueError:
            # failed = True
            print(f"The font Latin Modern {font_type} was not found.")


        # if failed:
        #     fail(f"Installation failed.")

    assert not failed

test_install_latin_modern_fonts_test()