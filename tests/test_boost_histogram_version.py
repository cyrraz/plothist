import sys

import pytest


def test_import_plothist_version_too_low(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that importing plothist raises ImportError if boost_histogram version is too low."""
    import boost_histogram as bh

    monkeypatch.setattr(bh, "__version__", "1.3.9")
    # pop sys.modules to force re-import
    sys.modules.pop("plothist", None)
    with pytest.raises(
        ImportError, match=r"The version of boost_histogram is lower than 1.4.0"
    ):
        import plothist  # noqa: F401


def test_import_plothist_dev_version_above_minimum(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test that a dev version above the minimum imports successfully."""
    import boost_histogram as bh

    monkeypatch.setattr(bh, "__version__", "1.5.0.dev1")
    sys.modules.pop("plothist", None)
    import plothist  # noqa: F401

    sys.modules.pop("plothist", None)


def test_import_plothist_rc_version_below_minimum(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test that an rc version below the minimum still raises ImportError."""
    import boost_histogram as bh

    monkeypatch.setattr(bh, "__version__", "1.3.9rc1")
    sys.modules.pop("plothist", None)
    with pytest.raises(
        ImportError, match=r"The version of boost_histogram is lower than 1.4.0"
    ):
        import plothist  # noqa: F401
