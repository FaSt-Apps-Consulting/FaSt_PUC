from fast_puc import puc


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