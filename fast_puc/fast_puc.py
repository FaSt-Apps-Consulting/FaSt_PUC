"""unit converts floats to strings with correct SI prefixes."""

import numpy as np


def puc(value=0, unit="", precision=3, verbose=False, filecompatible=False):
    """Formatting of values for scientific use of SI units

    from fast_puc import puc
    puc(0.1,"m")  # "100mm"
    puc(200e-9,"s")  # "200ns"
    puc(1.000213, "m", precision=5)  # "1000.2mm"
    puc(1.0001, " m")  # "1 m" with space
    puc(1.0001, "_m")  # "1_m" with underscore
    puc(0.911, "%")  # "91.1%" converted to percent
    puc(1001, "dB")  # "30dB" converted to dB
    puc(1030e-9, "!m")  # "1p03um" file name compatible without .

    The following wildcards can be used in the argument unit:
    - "dB" converts to decibels
    - "%" converts to percent
    - " " between number and unit
    - "_" between number and unit
    - "!" generates a filename compatible string "2p43nm"

    verbose=True returns additional information for scaling of vectors."""

    # preprocess input
    try:
        val = np.squeeze(value).astype(float)
    except ValueError as excpt:
        print("Cannot convert input to float")
        print(excpt)
        return str(value)

    # process hidden options
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

    if unit == "dB":
        string = (
            ("{0:." + str(int(precision)) + formatter + "}").format(10 * np.log10(val))
            + separator
            + unit
        )
    elif unit == "%":
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
        string = string.replace("µ", "u")
        string = string.replace(".", "p")
        string = string.replace("/", "p")
        string = string.replace(" ", "_")

    if verbose:
        # Return string, multiplier and prefix
        return string, mult, prefix
    else:
        # Return just the formatted string
        return string


def get_prefix(exponent):
    if exponent <= -19:
        prefix = ""
        mult = 0
    elif exponent <= -16:
        prefix = "a"
        mult = -18
    elif exponent <= -13:
        prefix = "f"
        mult = -15
    elif exponent <= -10:
        prefix = "p"
        mult = -12
    elif exponent <= -7:
        prefix = "n"
        mult = -9
    elif exponent <= -4:
        prefix = "µ"
        mult = -6
    elif exponent <= -1:
        prefix = "m"
        mult = -3
    elif exponent <= 2:
        prefix = ""
        mult = 0
    elif exponent <= 5:
        prefix = "k"
        mult = 3
    elif exponent <= 8:
        prefix = "M"
        mult = 6
    elif exponent <= 11:
        prefix = "G"
        mult = 9
    elif exponent <= 14:
        prefix = "T"
        mult = 12
    elif exponent <= 17:
        prefix = "P"
        mult = 15
    return mult, prefix
