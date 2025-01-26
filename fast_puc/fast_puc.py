"""puc converts floats to strings with correct SI prefixes."""

from __future__ import annotations
import numpy as np

# Constants for special units and characters
MICRO_SYMBOL = "µ"
DB_UNIT = "dB"
PERCENT_UNIT = "%"
FILE_REPLACEMENTS = {
    MICRO_SYMBOL: "u",
    ".": "p",
    "/": "p",
    " ": "_"
}

# SI prefix definitions: (exponent threshold, multiplier, prefix symbol)
SI_PREFIXES = [
    (-19, 0, ""),    # below this, no prefix
    (-16, -18, "a"), # atto
    (-13, -15, "f"), # femto
    (-10, -12, "p"), # pico
    (-7, -9, "n"),   # nano
    (-4, -6, "µ"),   # micro
    (-1, -3, "m"),   # milli
    (2, 0, ""),      # no prefix
    (5, 3, "k"),     # kilo
    (8, 6, "M"),     # mega
    (11, 9, "G"),    # giga
    (14, 12, "T"),   # tera
    (17, 15, "P"),   # peta
]

def format_db_value(val: float, precision: int, separator: str, unit: str) -> str:
    """Format value in decibels.
    
    Args:
        val: Value to format
        precision: Number of significant digits
        separator: Separator between value and unit
        unit: Unit string
        
    Returns:
        Formatted string with dB unit
    """
    return f"{{0:.{precision}g}}".format(10 * np.log10(val)) + separator + unit

def format_percent_value(val: float, precision: int, separator: str, unit: str) -> str:
    """Format value as percentage.
    
    Args:
        val: Value to format
        precision: Number of significant digits
        separator: Separator between value and unit
        unit: Unit string
        
    Returns:
        Formatted string with percent unit
    """
    return f"{{0:.{precision}g}}".format(100 * val) + separator + unit

def format_si_value(val: float, precision: int | float | np.ndarray, 
                   separator: str, unit: str) -> tuple[str, int, str]:
    """Format value with SI prefix.
    
    Args:
        val: Value to format (can be positive or negative)
        precision: Number of significant digits or array for dynamic precision
        separator: Separator between value and unit
        unit: Unit string
        
    Returns:
        Tuple of (formatted string with SI prefix, multiplier, prefix)
    """
    # save sign status
    sign = 1
    if val < 0:
        sign = -1
    val *= sign

    # Determine precision if given as array
    if type(precision) not in [float, int]:
        with np.errstate(divide="ignore", invalid="ignore"):
            exponent = np.floor(np.log10(np.min(np.abs(np.diff(precision)))))
        precision = np.abs(exponent - np.floor(np.log10(val))) + 1
    else:
        exponent = np.floor(np.log10(val))

    # round value to appropriate length
    if np.isfinite(exponent):
        val = np.round(val * 10 ** (-exponent - 1 + precision)) * 10 ** -(-exponent - 1 + precision)
    exponent = np.floor(np.log10(val))

    # Fix special case
    if precision in [4, 5]:
        # 1032.1 nm instead of 1.0321 µm
        exponent -= 3
        
    mult, prefix = get_prefix(exponent)

    # First attempt at formatting
    string = f"{{0:.{int(precision)}g}}".format(sign * val * 10 ** (-mult)) + separator + prefix + unit
    
    # If we got scientific notation, try with one more digit of precision
    if "e+" in string:
        string = f"{{0:.{int(precision + 1)}g}}".format(sign * val * 10 ** (-mult)) + separator + prefix + unit
    
    return string, mult, prefix

def puc(
    value: float | np.ndarray = 0,
    unit: str = "",
    precision: int | float | np.ndarray = 3,
    verbose: bool = False,
    filecompatible: bool = False,
) -> str | tuple[str, int, str]:
    """Format values with SI unit prefixes.
    
    Args:
        value: Numeric value to format
        unit: Unit string with optional modifiers (" ", "_", "!", "dB", "%")
        precision: Number of significant digits
        verbose: If True, return additional formatting information
        filecompatible: If True, return filename-safe string
        
    Returns:
        Formatted string if verbose=False, otherwise (string, multiplier, prefix)
        
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

    # Convert value to float, with better error message
    try:
        val = np.squeeze(value).astype(float)
    except (ValueError, TypeError) as e:
        raise ValueError(f"Cannot convert value '{value}' to float: {str(e)}")

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
        string = format_db_value(val, int(precision), separator, unit)
        mult, prefix = 0, ""
    elif unit == PERCENT_UNIT:
        string = format_percent_value(val, int(precision), separator, unit)
        mult, prefix = 0, ""
    else:
        string, mult, prefix = format_si_value(val, precision, separator, unit)

    # Convert string to be filename compatible
    if filecompatible:
        for old, new in FILE_REPLACEMENTS.items():
            string = string.replace(old, new)

    if verbose:
        return string, mult, prefix
    else:
        return string


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
