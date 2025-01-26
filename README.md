# FaSt_PUC

FaSt_PUC is a Python package that provides pretty unit conversion with automatic SI prefix selection. It intelligently formats numbers with appropriate metric prefixes (like k, M, G, µ, n, etc.) to make them more readable.

## Features

- Automatic selection of SI prefixes from atto (a) to peta (P)
- Support for custom unit strings
- Special formatting options for percentages and decibels
- File name compatible output
- Configurable precision
- Support for NumPy arrays
- No external dependencies except NumPy

## Installation

Install using pip:

```bash
pip install fast-puc
```

## Basic Usage

Import the package and call the main function:

```python
from fast_puc import puc

# Basic number formatting
puc(1.0001)         # "1"
puc(1.0001, "m")    # "1m"
puc(0.991e-6, "s")  # "991ns"
puc(1030e-9, "m")   # "1.03µm"
puc(999.999, "W")   # "1kW"
```

## Advanced Features

### Custom Separators and Special Formats

```python
# Custom separators
puc(1.0001, " m")   # "1 m"    # with space separator
puc(1.0001, "_m")   # "1_m"    # with underscore separator

# Special formats
puc(0.911, "%")     # "91.1%"  # convert to percent
puc(1001, "dB")     # "30dB"   # convert to dB
puc(1030e-9, "!m")  # "1p03um" # file name compatible with special character !
```

### Precision Control

```python
puc(1.2345, "m", precision=2)      # "1.2m"
puc(0.012345, "m", precision=2)    # "12mm"
puc(0.000123456, "m", precision=5) # "123460nm"
```

### Advanced Options

The `puc` function accepts several optional parameters:

```python
puc(value,               # Number to format (float or numpy array)
    unit="",            # Unit string with optional modifiers
    precision=3,        # Number of significant digits
    verbose=False,      # Return additional formatting info
    filecompatible=False) # Make output safe for filenames
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

Licensed under MIT License. See [LICENSE](LICENSE) for details.

## Author

Written by Fabian Stutzki (fast@fast-apps.de)

For more information, visit [https://www.fast-apps.de](https://www.fast-apps.de)