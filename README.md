# FaSt_PUC
FaSt_PUC is a pretty unit converter.
It creates a string with suitable metric prefix.

Written by Fabian Stutzki, fast@fast-apps.de

Licensed under MIT

## Usage
Import the package and call the main function:

```python
from fast_puc import puc

puc(1.0001)  # "1"
puc(1.0001, "m")  # "1m"
puc(0.991e-6, "s")  # "991ns"
puc(1030e-9, "m")  # "1.03µm"
```

PUC supports some special characters:

```python
puc(1.0001, " m")  # "1 m"  # with space separator
puc(1.0001, "_m")  # "1_m"  # with underscore separator
puc(0.911, "%")  # "91.1%"  # convert to percent
puc(1001, "dB")  # "30dB"  # convert to dB
puc(1030e-9, "!m")  # "1p03um"  # file name compatible
```