from plothist.scripts import make_examples


def test_make_figures():
    """
    Test make_examples.
    """

    make_examples(no_input=True, check_svg=True)
