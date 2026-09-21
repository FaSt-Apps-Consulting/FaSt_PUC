import pytest

from fast_puc import SI_PREFIXES, puc


@pytest.mark.parametrize(
    "threshold,mult,prefix,test_value",
    [
        # For each prefix, we'll test a value just below its threshold
        # We exclude the first entry (-19, 0, "") since it's just a lower bound
        *[
            (threshold, mult, prefix, 10 ** (threshold - 0.1))
            for threshold, mult, prefix in SI_PREFIXES[1:]
        ],
        # Test some exact powers of 10
        (-18, -18, "a", 1e-18),  # atto
        (-15, -15, "f", 1e-15),  # femto
        (-12, -12, "p", 1e-12),  # pico
        (-9, -9, "n", 1e-9),  # nano
        (-6, -6, "µ", 1e-6),  # micro
        (-3, -3, "m", 1e-3),  # milli
        (0, 0, "", 1),  # unit
        (3, 3, "k", 1e3),  # kilo
        (6, 6, "M", 1e6),  # mega
        (9, 9, "G", 1e9),  # giga
        (12, 12, "T", 1e12),  # tera
        (15, 15, "P", 1e15),  # peta
    ],
)
def test_si_prefixes(threshold, mult, prefix, test_value):
    """Test that each SI prefix is correctly applied for values in its range."""
    result, result_mult, result_prefix = puc(test_value, "m", verbose=True)

    assert result_mult == mult, f"Expected multiplier {mult} for {test_value}, got {result_mult}"
    assert result_prefix == prefix, (
        f"Expected prefix '{prefix}' for {test_value}, got '{result_prefix}'"
    )

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


def test_scientific_notation_small():
    # Should handle e-
    # 1e-20 is below SI atto threshold
    result = puc(1e-20, "W")
    assert "e" in result.lower()