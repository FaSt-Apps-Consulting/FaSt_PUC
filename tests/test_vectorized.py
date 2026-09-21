import numpy as np

from fast_puc import puc


def test_vector_input_list():
    assert puc([900e-6, 1000e-6, 1100e-6], "m") == ["900µm", "1mm", "1.1mm"]
    assert puc([1.0, 2.0], "W") == ["1W", "2W"]
    assert puc([-1e-3, 1e-3], "m") == ["-1mm", "1mm"]
    assert puc([0, 1e-3], "m") == ["0m", "1mm"]


def test_vector_input_numpy():
    assert puc(np.array([1e-3, 2e-3]), "m") == ["1mm", "2mm"]
    # 2D input flattens to a flat list
    assert puc(np.array([[1e-3], [2e-3]]), "m") == ["1mm", "2mm"]


def test_vector_verbose():
    assert puc(np.array([1e-3, 2e-3]), "m", verbose=True) == [
        ("1mm", -3, "m"),
        ("2mm", -3, "m"),
    ]


def test_vector_db_and_percent():
    assert puc([10, 101], "dB") == ["10dB", "20dB"]
    assert puc([0.5, 0.911], "%") == ["50%", "91.1%"]


def test_vector_filecompatible_and_separator():
    assert puc([1030e-9, 1000e-9], "!m") == ["1p03um", "1um"]
    assert puc([1e-3, 2e-3], " m") == ["1 mm", "2 mm"]


def test_vector_precision_scalar():
    assert puc([1.234, 2.345], "m", precision=2) == ["1.2m", "2.3m"]


def test_vector_dynamic_precision():
    assert puc([1.001, 1.002, 1.003], "m", precision=[1.001, 1.002, 1.003]) == [
        "1001mm",
        "1002mm",
        "1003mm",
    ]


def test_vector_special_case_precision():
    assert puc([1032.1e-9, 1000e-9], "m", precision=5) == ["1032.1nm", "1000nm"]


def test_vector_scientific_notation():
    assert puc([1e20, 1e-20], "m") == ["1e+20m", "1e-20m"]


def test_vector_outlier_values():
    assert puc([1e-20, 1.0, 1e20], "m") == ["1e-20m", "1m", "1e+20m"]