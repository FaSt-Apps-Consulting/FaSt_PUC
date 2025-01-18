from fast_puc import puc

print(puc(1.0001))  # "1"
print(puc(1.0001, "m"))  # "1m"
print(puc(0.991e-6, "s"))  # "991ns"
print(puc(1030e-9, "m"))  # "1.03µm"
print(puc(1.00001, "m"))  # 1m
print(puc(999.999, "W"))  # 1kW

print(puc(3, precision=[1.01, 1.02, 1.04]))
