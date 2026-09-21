from fast_puc import puc


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