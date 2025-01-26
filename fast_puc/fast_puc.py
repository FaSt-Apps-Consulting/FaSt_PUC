"""puc converts floats to strings with correct SI prefixes."""

from __future__ import annotations
import numpy as np
from enum import Enum

class SIPrefix(Enum):
    ATTO = (-18, "a")
    FEMTO = (-15, "f")
    PICO = (-12, "p")
    NANO = (-9, "n")
    MICRO = (-6, "µ")
    MILLI = (-3, "m")
    NONE = (0, "")
    KILO = (3, "k")
    MEGA = (6, "M")
    GIGA = (9, "G")
    TERA = (12, "T")
    PETA = (15, "P")

MICRO_SYMBOL = "µ"
DB_UNIT = "dB"
PERCENT_UNIT = "%"
FILE_REPLACEMENTS = {
    MICRO_SYMBOL: "u",
    ".": "p",
    "/": "p",
    " ": "_"
}

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

    formatter = "g"

    if unit == DB_UNIT:
        string = (
            ("{0:." + str(int(precision)) + formatter + "}").format(10 * np.log10(val))
            + separator
            + unit
        )
    elif unit == PERCENT_UNIT:
        string = (
            ("{0:." + str(int(precision)) + formatter + "}").format(sign * 100 * val)
            + separator
            + unit
        )
    else:
        mult, prefix = get_prefix(exponent)

        string = (
            ("{0:." + str(int(precision)) + formatter + "}").format(sign * val * 10 ** (-mult))
            + separator
            + prefix
            + unit
        )
        if "e+" in string:
            string = (
                ("{0:." + str(int(precision + 1)) + formatter + "}").format(
                    sign * val * 10 ** (-mult)
                )
                + separator
                + prefix
                + unit
            )

    # Convert string to be filename compatible
    if filecompatible:
        for old, new in FILE_REPLACEMENTS.items():
            string = string.replace(old, new)

    if verbose:
        # Return string, multiplier and prefix
        return string, mult, prefix
    else:
        # Return just the formatted string
        return string


def get_prefix(exponent: float) -> tuple[int, str]:
    """Get the SI prefix for a given exponent.
    
    Args:
        exponent: The exponent of the number in base 10
        
    Returns:
        Tuple of (multiplier, prefix_symbol)
    """
    if exponent <= -19:
        return SIPrefix.NONE.value
    elif exponent <= -16:
        return SIPrefix.ATTO.value
    elif exponent <= -13:
        return SIPrefix.FEMTO.value
    elif exponent <= -10:
        return SIPrefix.PICO.value
    elif exponent <= -7:
        return SIPrefix.NANO.value
    elif exponent <= -4:
        return SIPrefix.MICRO.value
    elif exponent <= -1:
        return SIPrefix.MILLI.value
    elif exponent <= 2:
        return SIPrefix.NONE.value
    elif exponent <= 5:
        return SIPrefix.KILO.value
    elif exponent <= 8:
        return SIPrefix.MEGA.value
    elif exponent <= 11:
        return SIPrefix.GIGA.value
    elif exponent <= 14:
        return SIPrefix.TERA.value
    elif exponent <= 17:
        return SIPrefix.PETA.value
    return SIPrefix.NONE.value
