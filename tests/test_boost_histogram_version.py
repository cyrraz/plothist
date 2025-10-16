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
