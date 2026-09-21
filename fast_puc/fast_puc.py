"""puc converts floats to strings with correct SI prefixes."""

from __future__ import annotations

import numpy as np

# Constants for special units and characters
MICRO_SYMBOL = "µ"
DB_UNIT = "dB"
PERCENT_UNIT = "%"
FILE_REPLACEMENTS = {MICRO_SYMBOL: "u", ".": "p", "/": "p", " ": "_"}


def _make_filecompatible(string: str) -> str:
    """Apply the filename-safe character replacements to a string."""
    for old, new in FILE_REPLACEMENTS.items():
        string = string.replace(old, new)
    return string

# SI prefix definitions: (exponent threshold, multiplier, prefix symbol)
SI_PREFIXES = [
    (-19, 0, ""),  # below this, no prefix
    (-16, -18, "a"),  # atto
    (-13, -15, "f"),  # femto
    (-10, -12, "p"),  # pico
    (-7, -9, "n"),  # nano
    (-4, -6, "µ"),  # micro
    (-1, -3, "m"),  # milli
    (2, 0, ""),  # no prefix
    (5, 3, "k"),  # kilo
    (8, 6, "M"),  # mega
    (11, 9, "G"),  # giga
    (14, 12, "T"),  # tera
    (17, 15, "P"),  # peta
]


def format_db_value(
    val: float | np.ndarray, precision: int, separator: str, unit: str
) -> list[str]:
    """Format value(s) in decibels.

    Args:
        val: Value or array of values to format
        precision: Number of significant digits
        separator: Separator between value and unit
        unit: Unit string

    Returns:
        List of formatted strings with dB unit
    """
    values = np.atleast_1d(np.asarray(val, dtype=float)).ravel()
    return [f"{{0:.{precision}g}}".format(10 * np.log10(v)) + separator + unit for v in values]


def format_percent_value(
    val: float | np.ndarray, precision: int, separator: str, unit: str
) -> list[str]:
    """Format value(s) as percentage.

    Args:
        val: Value or array of values to format
        precision: Number of significant digits
        separator: Separator between value and unit
        unit: Unit string

    Returns:
        List of formatted strings with percent unit
    """
    values = np.atleast_1d(np.asarray(val, dtype=float)).ravel()
    return [f"{{0:.{precision}g}}".format(100 * v) + separator + unit for v in values]


def _resolve_precision_per_element(
    precision: float | np.ndarray | list[float], values: np.ndarray
) -> np.ndarray:
    """Resolve scalar or dynamic precision into one precision per value.

    When ``precision`` is an array, the automatic precision is derived from the
    minimum non-zero difference between its elements.
    """
    if not np.isscalar(precision):
        with np.errstate(divide="ignore", invalid="ignore"):
            diffs = np.abs(np.diff(precision))
            min_diff = np.min(diffs[diffs > 0]) if np.any(diffs > 0) else 1
            data_exponent = np.floor(np.log10(min_diff))
        with np.errstate(divide="ignore", invalid="ignore"):
            per_element = np.abs(data_exponent - np.floor(np.log10(np.abs(values)))) + 1
        # Zeros short-circuit before precision is used; mask to avoid log10(0) -> inf
        return np.where(np.abs(values) == 0, 0.0, per_element)
    return np.full(np.shape(values), float(np.asarray(precision).item()))


def _format_si_element(
    val: float, precision: float, separator: str, unit: str
) -> tuple[str, int, str]:
    """Format a single value with SI prefix.

    Args:
        val: Value to format (can be positive or negative)
        precision: Number of significant digits
        separator: Separator between value and unit
        unit: Unit string

    Returns:
        Tuple of (formatted string with SI prefix, multiplier, prefix)
    """
    # save sign status
    sign = 1
    if val < 0:
        sign = -1
    val = np.abs(val)

    # Handle zero case explicitly
    if val == 0:
        return "0" + separator + unit, 0, ""

    with np.errstate(divide="ignore", invalid="ignore"):
        exponent = np.floor(np.log10(val))

    # round value to appropriate length
    if np.isfinite(exponent):
        val = np.round(val * 10 ** (-exponent - 1 + precision)) * 10 ** -(-exponent - 1 + precision)
    with np.errstate(divide="ignore", invalid="ignore"):
        exponent = np.floor(np.log10(val))

    # Fix special case
    if int(precision) in [4, 5]:
        # 1032.1 nm instead of 1.0321 µm
        exponent -= 3

    mult, prefix = get_prefix(exponent)

    # First attempt at formatting
    string = (
        f"{{0:.{int(precision)}g}}".format(sign * val * 10 ** (-mult)) + separator + prefix + unit
    )

    # If we got scientific notation, try with one more digit of precision
    if "e" in string.lower():
        string = (
            f"{{0:.{int(precision + 1)}g}}".format(sign * val * 10 ** (-mult))
            + separator
            + prefix
            + unit
        )

    return string, mult, prefix


def format_si_value(
    val: float | np.ndarray, precision: float | np.ndarray | list[float], separator: str, unit: str
) -> list[tuple[str, int, str]]:
    """Format value(s) with SI prefix.

    Args:
        val: Value(s) to format (can be positive or negative)
        precision: Number of significant digits or array for dynamic precision
        separator: Separator between value and unit
        unit: Unit string

    Returns:
        List of (formatted string with SI prefix, multiplier, prefix) per element
    """
    values = np.atleast_1d(np.asarray(val, dtype=float)).ravel()
    precisions = _resolve_precision_per_element(precision, values)
    return [_format_si_element(v, p, separator, unit) for v, p in zip(values, precisions)]


def puc(
    value: float | np.ndarray | list[float] | tuple[float, ...] = 0,
    unit: str = "",
    precision: float | np.ndarray | list[float] = 3,
    verbose: bool = False,
    filecompatible: bool = False,
) -> str | tuple[str, int, str] | list[str] | list[tuple[str, int, str]]:
    """Format values with SI unit prefixes.

    Vectorized: when ``value`` is a list or NumPy array, a flat list of formatted
    strings is returned (one per element). A scalar input returns a single string.
    With ``verbose=True`` the same shapes hold, but each element is a
    ``(string, multiplier, prefix)`` tuple.

    Args:
        value: Numeric value or array of values to format
        unit: Unit string with optional modifiers (" ", "_", "!", "dB", "%")
        precision: Number of significant digits, or array for dynamic precision
        verbose: If True, return additional formatting information
        filecompatible: If True, return filename-safe string

    Returns:
        Formatted string (or list of strings) if verbose=False, otherwise
        (string, multiplier, prefix) tuple (or list of tuples)

    Raises:
        ValueError: If value cannot be converted to float
    """
    # Validate inputs
    if not isinstance(unit, str):
        raise TypeError("unit must be a string")
    if not isinstance(verbose, bool):
        raise TypeError("verbose must be a boolean")
    if not isinstance(filecompatible, bool):
        raise TypeError("filecompatible must be a boolean")

    # Convert value to float array
    try:
        val = np.squeeze(np.asarray(value)).astype(float)
    except (ValueError, TypeError) as e:
        raise ValueError(f"Cannot convert value '{value}' to float: {e!s}")

    is_scalar = val.ndim == 0

    # Ensure precision is scalar for dB and % formatting
    if not np.isscalar(precision):
        # Fallback to default if we can't easily determine a scalar precision
        p_val = 3
    else:
        p_val = int(np.asarray(precision).item())

    # preprocess input
    separator = ""
    if " " in unit:
        separator = " "
        unit = unit.replace(" ", "")
    elif "_" in unit:
        separator = "_"
        unit = unit.replace("_", "")

    if "!" in unit:
        filecompatible = True
        unit = unit.replace("!", "")

    if unit == DB_UNIT:
        results = [(s, 0, "") for s in format_db_value(val, p_val, separator, unit)]
    elif unit == PERCENT_UNIT:
        results = [(s, 0, "") for s in format_percent_value(val, p_val, separator, unit)]
    else:
        results = format_si_value(val, precision, separator, unit)

    # Convert strings to be filename compatible
    if filecompatible:
        results = [
            (_make_filecompatible(string), mult, prefix) for string, mult, prefix in results
        ]

    if is_scalar:
        string, mult, prefix = results[0]
        if verbose:
            return string, mult, prefix
        return string

    if verbose:
        return results
    return [string for string, _, _ in results]


def get_prefix(exponent: float) -> tuple[int, str]:
    """Get the SI prefix for a given exponent.

    Args:
        exponent: The exponent of the number in base 10

    Returns:
        Tuple of (multiplier, prefix_symbol)
    """
    for threshold, mult, prefix in SI_PREFIXES:
        if exponent <= threshold:
            return mult, prefix
    return 0, ""  # default case for very large numbers
