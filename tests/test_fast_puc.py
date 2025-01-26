#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# %%
from fast_puc import puc, SI_PREFIXES
import pytest


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


@pytest.mark.parametrize("threshold,mult,prefix,test_value", [
    # For each prefix, we'll test a value just below its threshold
    # We exclude the first entry (-19, 0, "") since it's just a lower bound
    *[(threshold, mult, prefix, 10**(threshold-0.1)) 
      for threshold, mult, prefix in SI_PREFIXES[1:]],
    
    # Test some exact powers of 10
    (-18, -18, "a", 1e-18),  # atto
    (-15, -15, "f", 1e-15),  # femto
    (-12, -12, "p", 1e-12),  # pico
    (-9, -9, "n", 1e-9),     # nano
    (-6, -6, "µ", 1e-6),     # micro
    (-3, -3, "m", 1e-3),     # milli
    (0, 0, "", 1),           # unit
    (3, 3, "k", 1e3),        # kilo
    (6, 6, "M", 1e6),        # mega
    (9, 9, "G", 1e9),        # giga
    (12, 12, "T", 1e12),     # tera
    (15, 15, "P", 1e15),     # peta
])
def test_si_prefixes(threshold, mult, prefix, test_value):
    """Test that each SI prefix is correctly applied for values in its range."""
    result, result_mult, result_prefix = puc(test_value, "m", verbose=True)
    
    assert result_mult == mult, f"Expected multiplier {mult} for {test_value}, got {result_mult}"
    assert result_prefix == prefix, f"Expected prefix '{prefix}' for {test_value}, got '{result_prefix}'"
    
    # Verify the formatted string
    if prefix:
        assert prefix in result, f"Prefix '{prefix}' not found in result '{result}'"
    assert "m" in result, f"Unit 'm' not found in result '{result}'"

def test_very_large_numbers():
    """Test numbers above the highest prefix threshold."""
    result, mult, prefix = puc(1e20, "m", verbose=True)
    assert mult == 0
    assert prefix == ""
    assert "e+" in result

def test_very_small_numbers():
    """Test numbers below the lowest prefix threshold."""
    result, mult, prefix = puc(1e-20, "m", verbose=True)
    assert mult == 0
    assert prefix == ""
    assert "e-" in result
