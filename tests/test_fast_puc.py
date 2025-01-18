#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# %%
from fast_puc import puc


# %%
def test_basic_input():
    assert puc(1.0001) == "1"
    assert puc(1.0001, "m") == "1m"
    assert puc([1.0001], "s") == "1s"
    assert puc(0.991e-6, "s") == "991ns"
    assert puc(1030e-9, "m") == "1.03µm"  # 1030nm would be better


def test_precision():
    assert puc(1.2345, "m", precision=2) == "1.2m"
    assert puc(0.012345, "m", precision=2) == "12mm"
    assert puc(0.0012345, "m", precision=3) == "1.23mm"
    assert puc(0.000123456, "m", precision=5) == "123460nm"
    assert puc(1.000213, "m", precision=5) == "1000.2mm"


def test_precision_vector():
    assert puc(1.001, "m", precision=[1.01, 1.02, 1.03]) == "1m"  # should be 1001mm
    assert puc(1.001, "m", precision=[1.001, 1.002, 1.003]) == "1001mm"
    assert puc(1.001, "m", precision=[1.0001, 1.0002, 1.0003]) == "1.001m"  # should be 1001.0mm


def test_options():
    assert puc(1.0001, " m") == "1 m"  # space
    assert puc(1.0001, "_m") == "1_m"  # space
    assert puc(1030e-9, "!m") == "1p03um"  # file compatible


def test_option_percent():
    assert puc(0.911, "%") == "91.1%"  # percent
    assert puc(0.911, "%", precision=2) == "91%"  # percent
    assert puc(9.231, "%") == "923%"  # percent
    assert puc(9.23112, "%", precision=4) == "923.1%"  # percent


def test_option_db():
    assert puc(10, "dB") == "10dB"  # dB
    assert puc(101, "dB") == "20dB"  # dB
    assert puc(1001, "dB") == "30dB"  # dB
    assert puc(1011, "dB", precision=4) == "30.05dB"  # dB


def test_cornercases():
    assert puc(0, "W") == "0W"
    assert puc(250, "m", precision=2) == "250m"
    assert puc(250e-4, "m", precision=1) == "20mm"  # due to np.round(2.5)=2.0
    assert puc(250e-6, "m", precision=2) == "250µm"
    assert puc(999, "W") == "999W"
    assert puc(999, "W", precision=2) == "1kW"
    assert puc(999.999, "W") == "1kW"
    assert puc(9.999e-4, "W") == "1mW"
    assert puc(999.999999, "m", precision=2) == "1km"
    return
