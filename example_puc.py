"""Example usage of FaSt_PUC - Pretty Unit Converter."""

# %% Import
from fast_puc import puc

# %% Basic number formatting
print("\n=== Basic Usage ===")
print(puc(1.0001))         # "1"
print(puc(1.0001, "m"))    # "1m"
print(puc(999.999, "W"))   # "1kW"

# %% SI prefix examples
print("\n=== SI Prefixes ===")
print(puc(0.991e-6, "s"))  # "991ns"    - nano
print(puc(1030e-9, "m"))   # "1.03µm"   - micro
print(puc(1.2e6, "Hz"))    # "1.2MHz"   - mega
print(puc(3.5e12, "W"))    # "3.5TW"    - tera

# %% Custom separators
print("\n=== Custom Separators ===")
print(puc(1.0001, " m"))   # "1 m"      - space separator
print(puc(1.0001, "_m"))   # "1_m"      - underscore separator

# %% Special formats
print("\n=== Special Formats ===")
print(puc(0.911, "%"))     # "91.1%"    - percentage
print(puc(1001, "dB"))     # "30dB"     - decibels
print(puc(1030e-9, "!m"))  # "1p03um"   - filename safe

# %% Precision control
print("\n=== Precision Control ===")
print(puc(1.2345, "m", precision=2))       # "1.2m"
print(puc(0.012345, "m", precision=2))     # "12mm"
print(puc(0.000123456, "m", precision=5))  # "123460nm"

# %% Vector precision
print("\n=== Vector Precision ===")
print(puc(1.2, precision=[1.01, 1.012, 1.04]))  # Precision based on vector differences

# %% Verbose output
print("\n=== Verbose Output ===")
result, multiplier, prefix = puc(1.23e6, "W", verbose=True)
print(f"Result: {result}, Multiplier: {multiplier}, Prefix: {prefix}")  # Get formatting details
