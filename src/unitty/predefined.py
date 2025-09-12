from .units import Unit
from . import bases

# length
# =================================
length = Unit.base(bases.LENGTH)
# Metric
m = Unit.named(1, length, "m", "meter")
mm = Unit.named(0.001, m, "mm", "millimeter")
cm = Unit.named(0.01, m, "cm", "centimeter")
km = Unit.named(1000, m, "km", "kilometer")
um = Unit.named(1e-6, m, "um", "micrometer")
nm = Unit.named(1e-9, m, "nm", "nanometer")
pm = Unit.named(1e-12, m, "pm", "picometer")
# Imperial / US
inch = Unit.named(25.4, mm, "in", "inch")
ft = Unit.named(12, inch, "ft", "foot")
yd = Unit.named(3, ft, "yd", "yard")
mi = Unit.named(5280, ft, "mi", "mile")
thou = Unit.named(1e-3, inch, "th", "thou")
mil = Unit.named(1e-3, inch, "mil", "mil")

# length**2 (area)
# ----------------
# Metric
m2 = Unit.named(1, m**2, "m2", "square meter")
mm2 = Unit.named(1, mm**2, "mm2", "square millimeter")
cm2 = Unit.named(1, cm**2, "cm2", "square centimeter")
km2 = Unit.named(1, km**2, "km2", "square kilometer")

# Imperial / US
in2 = Unit.named(1, inch**2, "in2", "square inch")
ft2 = Unit.named(1, ft**2, "ft2", "square foot")
yd2 = Unit.named(1, yd**2, "yd2", "square yard")
mi2 = Unit.named(1, mi**2, "mi2", "square mile")

# length**3 (volume)
# -------------------
m3 = Unit.named(1, m**3, "m3", "cubic meter")
mm3 = Unit.named(1, mm**3, "mm3", "cubic millimeter")
cm3 = Unit.named(1, cm**3, "cm3", "cubic centimeter")
km3 = Unit.named(1, km**3, "km3", "cubic kilometer")
L = Unit.named(0.001, m3, "L", "liter")
mL = Unit.named(0.001, L, "mL", "milliliter")

in3 = Unit.named(1, inch**3, "in3", "cubic inch")
ft3 = Unit.named(1, ft**3, "ft3", "cubic foot")
gal = Unit.named(4.54609, L, "gal", "imperial gallon")
USgal = Unit.named(3.785411784, L, "USgal", "US gallon")
floz = Unit.named(28.4130625, mL, "floz", "imperial fluid ounce")
USfloz = Unit.named(29.5735295625, mL, "USfloz", "US fluid ounce")
UScup = Unit.named(8, USfloz, "UScup", "US cup")

# time
# =================================
time = Unit.base(bases.TIME)
s = Unit.named(1.0, time, "s", "second")
min = Unit.named(60, s, "min", "minute")
hr = Unit.named(60, min, "hr", "hour")
day = Unit.named(24, hr, "day", "day")
yr = Unit.named(365.25, day, "yr", "year")



# mass
# =================================
mass = Unit.base(bases.MASS)
kg = Unit.named(1.0, mass, "kg", "kilogram")
g = Unit.named(1e-3, kg, "g", "gram")
mg = Unit.named(1e-3, g, "mg", "milligram")
ug = Unit.named(1e-3, mg, "ug", "microgram")
pg = Unit.named(1e-3, ug, "pg", "picogram")
tonne = Unit.named(1e3, kg, "tonne", "tonne")

oz = Unit.named(28.349523125, g, "oz", "ounce mass")
lb = Unit.named(0.45359237, kg, "lb", "pound mass")
ton = Unit.named(2000, lb, "ton", "US ton")


# temperature
# =================================
temperature = Unit.base(bases.TEMPERATURE)
_base = "K"
K = [1.0, "temperature", "kelvin"]

[substance]
_base = "mol"
mol = [1.0, "substance", "mole"]

[luminosity]
_base = "cd"
cd = [1.0, "luminosity", "candela"]



#########################
####  DERIVED UNITS  ####
#########################

# current
# =================================
current = Unit.base(bases.CURRENT)
A = Unit.named(1.0, current, "A", "ampere")

A = [1.0, "current", "ampere"]

# energy
# =================================
_base = "J"
J = [1.0, ["N", "m"], "joule", { SI_prefixes = ["m", "k", "M"] }]




[force]
_base = "N"
N = [1.0, ["kg", "m", "-s", "-s"], "newton", { SI_prefixes = ["m", "k", "M"] }]
lbf = [4.4482216152605, "N", "pounds force"]
kip = [4448.2216, "N", "kip"]


[torque]
_base = "Nm"
Nm = [1.0, ["N", "m"], "newton meter", { SI_prefixes = ["m", "k", "M"] }]
ft_lb = [1.0, ["ft", "lbf"], "newton meter"]

[power]
_base = "W"
W = [1.0, ["J", "-s"], "watt", { SI_prefixes = ["m", "k", "M", "G"] }]

[pressure]
_base = "Pa"
Pa = [
    1.0,
    [
        "N",
        "-m",
        "-m",
    ],
    "pascal",
    { SI_prefixes = [
        "m",
        "h",
        "k",
        "M",
        "G",
    ] },
]
bar = [1e5, "Pa", "bar"]
mbar = [1e-3, "bar", "millibar"]
atm = [101325, "Pa", "atmosphere"]
psi = [6894.75728, "Pa", "pounds force per square inch"]
ksi = [68947.5728, "Pa", "kilopounds per square inch"]
psf = [47.880208, "Pa", "pounds force per square foot"]

[density]
_base = "kgm3"
gm3 = [
    1.0,
    [
        "g",
        "-m",
        "-m",
        "-m",
    ],
    "kilograms per cubic meter",
    { SI_prefixes = [
        "m",
        "k",
    ] },
]
pcf = [16.01846337396, "kgm3", "pounds mass per cubic foot"]

[speed]
_base = "mps"
mps = [1.0, ["m", "-s"], "meters per second", { SI_prefixes = ["k"] }]
kph = [1.0, ["km", "-hour"], "kilometers per hour"]
fps = [1.0, ["ft", "-s"], "feet per second"]
mph = [1.0, ["mi", "-hour"], "miles per hour"]

