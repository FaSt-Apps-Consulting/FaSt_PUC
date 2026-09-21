from fast_puc import puc


def test_basic_input():
    assert puc(1.0001) == "1"
    assert puc(1.0001, "m") == "1m"
    assert puc([1.0001], "s") == "1s"
    assert puc(0.991e-6, "s") == "991ns"
    assert puc(1030e-9, "m") == "1.03µm"  # 1030nm would be better