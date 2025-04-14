from __future__ import annotations

import numpy as np
import pytest
from pytest import approx
from uhi.numpy_plottable import ensure_plottable_histogram

ROOT = pytest.importorskip("ROOT")


def test_root_imported() -> None:
    assert ROOT.TString("Hello World") == "Hello World"


def test_root_th1f_convert() -> None:
    th = ROOT.TH1F("h1", "h1", 50, 10, 10)
    th.FillRandom("gaus", 100)
    h = ensure_plottable_histogram(th)
    assert all(th.GetBinContent(i + 1) == approx(iv) for i, iv in enumerate(h.values()))
    assert all(
        th.GetBinError(i + 1) == approx(ie)
        for i, ie in enumerate(np.sqrt(h.variances()))
    )
