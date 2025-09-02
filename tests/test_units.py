import numpy as np
from pytest import approx

from unitty import bases
from unitty.units import Quantity, Unit
import pytest

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
        qty = Quantity(5.0, ms)
        assert isinstance(qty, Quantity)
        assert qty.value == 0.005  # Always in base units
        assert qty.unit is ms

    def test_to(self):
        time = Unit.base(bases.TIME)
        sec = Unit.named(1, time, "s", "second")
        ms = Unit.named(1e-3, sec, "ms", "millisecond")
        qty = Quantity(5, ms)
        res = qty.to(sec)
        assert res == 0.005

    def test_to_parenthises(self):
        time = Unit.base(bases.TIME)
        sec = Unit.named(1, time, "s", "second")
        ms = Unit.named(1e-3, sec, "ms", "millisecond")
        res = Quantity(5, ms).to(sec)
        assert res == 0.005

    def test_to_2(self):
        time = Unit.base(bases.TIME)
        sec = Unit.named(1, time, "s", "second")
        ms = Unit.named(1e-3, sec, "ms", "millisecond")
        us = Unit.named(1e-6, sec, "us", "microsecond")
        qty = Quantity(5, ms)
        res = qty.to(us)
        assert res == 5000.0

    def test_str(self):
        time = Unit.base(bases.TIME)
        sec = Unit.named(1, time, "s", "second")
        ms = Unit.named(1e-3, sec, "ms", "millisecond")
        qty = Quantity(5, ms)
        assert str(qty) == "5 ms"

    def test_add(self):
        time = Unit.base(bases.TIME)
        s = Unit.named(1, time, "s", "second")
        time1 = Quantity(5, s)
        time2 = Quantity(2, s)
        total = time1 + time2
        assert isinstance(total, Quantity)
        assert total.unit.abbr == "s"
        assert total.value == approx(7)

    def test_add_incompatible(self):
        time = Unit.base(bases.TIME)
        length = Unit.base(bases.LENGTH)
        s = Unit.named(1, time, "s", "second")
        m = Unit.named(1, length, "m", "meter")
        time1 = Quantity(5, s)
        length1 = Quantity(2, m)
        with pytest.raises(ValueError):
            time1 + length1  # type: ignore

    def test_sub(self):
        time = Unit.base(bases.TIME)
        s = Unit.named(1, time, "s", "second")
        time1 = Quantity(5, s)
        time2 = Quantity(2, s)
        total = time1 - time2
        assert isinstance(total, Quantity)
        assert total.unit.abbr == "s"
        assert total.value == approx(3)

    def test_sub_incompatible(self):
        time = Unit.base(bases.TIME)
        length = Unit.base(bases.LENGTH)
        s = Unit.named(1, time, "s", "second")
        m = Unit.named(1, length, "m", "meter")
        time1 = Quantity(5, s)
        length1 = Quantity(2, m)
        with pytest.raises(ValueError):
            time1 - length1  # type: ignore

    def test_multiply(self):
        time = Unit.base(bases.TIME)
        length = Unit.base(bases.LENGTH)
        s = Unit.named(1, time, "s", "second")
        m = Unit.named(1, length, "m", "meter")
        dist = Quantity(5, m)
        time = Quantity(2, s)
        speed = dist * time
        assert isinstance(speed, Quantity)
        assert speed.unit.abbr == "m.s"
        assert speed.value == approx(5 * 2)

    def test_divide(self):
        time = Unit.base(bases.TIME)
        length = Unit.base(bases.LENGTH)
        s = Unit.named(1, time, "s", "second")
        m = Unit.named(1, length, "m", "meter")
        dist = Quantity(5, m)
        time = Quantity(2, s)
        speed = dist / time
        assert isinstance(speed, Quantity)
        assert speed.unit.abbr == "m/s"
        assert speed.value == approx(5 / 2)


class TestQuantityNumpy:
    def test_creation(self):
        time = Unit.base(bases.TIME)
        sec = Unit.named(1, time, "s", "second")
        ms = Unit.named(1e-3, sec, "ms", "millisecond")
        arr = np.linspace(0, 10, 5)
        qty = Quantity(arr, ms)
        assert isinstance(qty, Quantity)
        assert qty.value == approx(arr * 1e-3)  # Always in base units
        assert qty.unit is ms

    def test_mul(self):
        time = Unit.base(bases.TIME)
        sec = Unit.named(1, time, "s", "second")
        ms = Unit.named(1e-3, sec, "ms", "millisecond")
        arr = np.linspace(0, 10, 5)
        qty = Quantity(arr, ms)
        new_qty = 5 * qty
        assert isinstance(new_qty, Quantity)
        assert new_qty.value == approx(5 * arr * 1e-3)  # Always in base units
        assert new_qty.unit is ms

    def test_rmul(self):
        time = Unit.base(bases.TIME)
        sec = Unit.named(1, time, "s", "second")
        ms = Unit.named(1e-3, sec, "ms", "millisecond")
        arr = np.linspace(0, 10, 5)
        qty = Quantity(arr, ms)
        new_qty = qty * 5
        assert isinstance(new_qty, Quantity)
        assert new_qty.value == approx(5 * arr * 1e-3)  # Always in base units
        assert new_qty.unit is ms

    def test_truediv(self):
        time = Unit.base(bases.TIME)
        sec = Unit.named(1, time, "s", "second")
        ms = Unit.named(1e-3, sec, "ms", "millisecond")
        arr = np.linspace(0, 10, 5)
        qty = Quantity(arr, ms)
        new_qty = qty / 5
        assert isinstance(new_qty, Quantity)
        assert new_qty.value == approx(arr / 5 * 1e-3)  # Always in base units
        assert new_qty.unit is ms

    def test_pow(self):
        time = Unit.base(bases.TIME)
        sec = Unit.named(1, time, "s", "second")
        ms = Unit.named(1e-3, sec, "ms", "millisecond")
        arr = np.linspace(0, 10, 5)
        qty = Quantity(arr, ms)
        new_qty = qty**2
        assert isinstance(new_qty, Quantity)
        assert new_qty.value == approx(
            (arr * 1e-3) ** 2
        )  # Always in base units
        assert new_qty.unit is not ms
        assert new_qty.unit.value == 1e-6
