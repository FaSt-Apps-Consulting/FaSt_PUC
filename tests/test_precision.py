import numpy as np

from fast_puc import puc


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


def test_zero_with_array_precision():
    # Should not crash and should return "0"
    assert puc(0, precision=np.array([1.0, 1.01])) == "0"


def test_db_percent_with_array_precision():
    # Should not crash
    assert "dB" in puc(10, "dB", precision=np.array([1.0, 1.01]))
    assert "%" in puc(0.5, "%", precision=np.array([1.0, 1.01]))


def test_brittle_precision():
    # Precision calculated as 4.000...1 should still trigger nm logic
    assert puc(1032.1e-9, "m", precision=5.0) == "1032.1nm"
    assert puc(1032.1e-9, "m", precision=4.0) == "1032nm"