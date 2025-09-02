MASS = "mass"
LENGTH = "length"
TIME = "time"
CURRENT = "current"
TEMPERATURE = "temperature"
SUBSTANCE = "substance"
LUMINOSITY = "luminosity"

# Indices for base quantities
BASES = [MASS, LENGTH, TIME, CURRENT, TEMPERATURE, SUBSTANCE, LUMINOSITY]
INDICES = {b: i for i, b in enumerate(BASES)}
NUM_BASES = len(BASES)

__all__ = [
    "MASS",
    "LENGTH",
    "TIME",
    "CURRENT",
    "TEMPERATURE",
    "SUBSTANCE",
    "LUMINOSITY",
    "BASES",
    "INDICES",
    "NUM_BASES",
]
