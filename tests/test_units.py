import pytest
from pytest import approx

from unitty.units import Unit, Quantity
from unitty import bases, config


class TestUnits:
    def test_base(self):
        mass = Unit.base(bases.MASS)
        assert mass.value == 1.0
        assert mass.vector[bases.INDICES[bases.MASS]] == 1.0
        assert mass.desc == f"Base unit: {bases.MASS}"
        assert mass.spec[0].abbr == bases.MASS

    def test_named(self):
        mass = Unit.base(bases.MASS)
        kg = Unit.named(1.0, mass, "kg", "kilogram")
        assert kg.value == 1.0
        assert kg.vector[bases.INDICES[bases.MASS]] == 1.0
        assert kg.desc == "kilogram"
        assert kg.spec[0].abbr == "kg"
    
    def test_mul(self):
        m = Unit.base(bases.MASS)
        s = Unit.base(bases.TIME)
        u = m * s
        assert u.value == 1.0
        assert u.vector[bases.INDICES[bases.MASS]] == 1.0
        assert u.vector[bases.INDICES[bases.TIME]] == 1.0
        assert u.desc == "Derived unit"
        assert len(u.spec) == 2

    def test_div(self):
        length = Unit.base(bases.LENGTH)
        s = Unit.base(bases.TIME)
        u = length / s
        assert u.value == 1.0
        assert u.vector[bases.INDICES[bases.LENGTH]] == 1.0
        assert u.vector[bases.INDICES[bases.TIME]] == -1.0
        assert u.desc == "Derived"
        assert len(u.spec) == 2

    def test_pow(self):
        length = Unit.base(bases.LENGTH)
        u = length**2
        assert u.value == 1.0
        assert u.vector[bases.INDICES[bases.LENGTH]] == 2.0
        assert u.desc == "Derived"
        assert len(u.spec) == 1
        assert u.spec[0].order == 2.0
   

    def test_str(self):
        mass = Unit.base(bases.MASS)
        kg = Unit.named(1.0, mass, "kg", "kilogram")
        length = Unit.base(bases.LENGTH)
        meter = Unit.named(1.0, length, "m", "meter")
        time = Unit.base(bases.TIME)
        sec = Unit.named(1.0, time, "s", "second")
        ms = Unit.named(1e-3, sec, "ms", "millisecond")
        u = kg * meter / ms
        assert str(u) == "kg.m/ms"

    def test_value_not_quantity(self):
        time = Unit.base(bases.TIME)
        sec = Unit.named(1, time, "s", "second")
        ms = Unit.named(1e-3, sec, "ms", "millisecond")
        value = 5 << ms
        assert isinstance(value, float)
        assert value == 5e-3

class TestQuantity:
    def test_creation(self):
        time = Unit.base(bases.TIME)
        sec = Unit.named(1, time, "s", "second")
        ms = Unit.named(1e-3, sec, "ms", "millisecond")
        qty = 5 @ ms
        assert isinstance(qty, Quantity)
        assert qty.value == 5e-3
        assert qty.vector[bases.INDICES[bases.TIME]] == 1.0
        assert qty.spec[0].abbr == "ms"

    def test_to(self):
        time = Unit.base(bases.TIME)
        sec = Unit.named(1, time, "s", "second")
        ms = Unit.named(1e-3, sec, "ms", "millisecond")
        qty = 5 @ ms
        res = qty.to(sec)
        assert res == 0.005
    
    def test_to_parenthises(self):
        time = Unit.base(bases.TIME)
        sec = Unit.named(1, time, "s", "second")
        ms = Unit.named(1e-3, sec, "ms", "millisecond")
        res = (5 @ ms).to(sec)
        assert res == 0.005


