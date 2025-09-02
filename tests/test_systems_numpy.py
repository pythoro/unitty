from unitty import systems, units, bases
import pytest
from pytest import approx
import numpy as np


length = units.Unit.base(bases.LENGTH)
m = units.Unit.named(1.0, length, "m", "meter")
mm = units.Unit.named(0.001, m, "mm", "millimeter")
km = units.Unit.named(1000, m, "km", "kilometer")

_in = units.Unit.named(0.0254, m, "in", "inch")
ft = units.Unit.named(12, _in, "ft", "foot")
yd = units.Unit.named(3, ft, "yd", "yard")
mi = units.Unit.named(5280, ft, "mi", "mile")


time = units.Unit.base(bases.TIME)
s = units.Unit.named(1.0, time, "s", "second")
us = units.Unit.named(1e-6, s, "us", "microsecond")
ms = units.Unit.named(1e-3, s, "ms", "millisecond")
min = units.Unit.named(60.0, s, "min", "minute")
hr = units.Unit.named(3600.0, s, "hr", "hour")


@pytest.fixture
def measure_1():
    measure = systems.Measure([mm, m, km])
    return measure


class TestMeasure:
    def test_convert(self, measure_1):
        q1 = units.Quantity(np.array([0.5, 0.75]), m)
        val, unit = measure_1.convert(q1)
        assert unit == m
        assert val == approx(np.array([0.5, 0.75]))

        q2 = units.Quantity(np.array([0.05, 0.075]), m)
        val, unit = measure_1.convert(q2)
        assert unit == mm
        assert val == approx(np.array([50.0, 75.0]))

        q3 = units.Quantity(np.array([0.005, 0.0075]), m)
        val, unit = measure_1.convert(q3)
        assert unit == mm
        assert val == approx(np.array([5.0, 7.5]))

        q4 = units.Quantity(np.array([500, 750]), m)
        val, unit = measure_1.convert(q4)
        assert unit == km
        assert val == approx(np.array([0.5, 0.75]))

    
    def test_convert_no_match(self, measure_1):
        q = units.Quantity(np.array([1.0]), units.Unit.base(bases.MASS))
        with pytest.raises(ValueError):
            measure_1.convert(q)

    def test_convert_edge(self, measure_1):
        q = units.Quantity(np.array([0.1, 0.05, 0.01]), m)
        val, unit = measure_1.convert(q)
        assert unit == mm
        assert val == approx(np.array([100.0, 50.0, 10.0]))

    def test_convert_small(self, measure_1):
        q = units.Quantity(np.array([0.00005, 0.01]), m)
        val, unit = measure_1.convert(q)
        assert unit == mm
        assert val == approx(np.array([0.05, 10.0]))

    def test_convert_large(self, measure_1):
        q = units.Quantity(np.array([5000000, 10]), m)
        val, unit = measure_1.convert(q)
        assert val == approx(np.array([5000.0, 0.01]))
        assert unit == km

    def test_call(self, measure_1):
        q = units.Quantity(np.array([5000000, 10]), m)
        val, unit = measure_1(q)
        assert val == approx(np.array([5000.0, 0.01]))
        assert unit == km


@pytest.fixture
def measures_1():
    measures = systems.Measures()
    measures["length"] = systems.Measure([mm, m, km])
    measures["time"] = systems.Measure( [us, ms, s, min, hr] )
    return measures

@pytest.fixture
def measures_2():
    measures = systems.Measures()
    measures["length"] = systems.Measure([_in, ft, yd, mi])
    measures["time"] = systems.Measure( [us, ms, s, min, hr] )
    return measures

@pytest.fixture
def system_1(measures_1):
    system = systems.UnitSystem(measures_1)
    return system


class TestMeasurementSystem:
    def test_convert_length(self, system_1):
        q = units.Quantity(np.array([0.5, 0.6]), m)
        val, unit = system_1.convert(q)
        assert val == approx(np.array([0.5, 0.6]))
        assert unit == m

        q = units.Quantity(np.array([0.05, 0.06]), m)
        val, unit = system_1.convert(q)
        assert val == approx(np.array([50.0, 60.0]))
        assert unit == mm

        q = units.Quantity(np.array([500, 300]), m)
        val, unit = system_1.convert(q)
        assert val == approx(np.array([0.5, 0.3]))
        assert unit == km

    def test_convert_time(self, system_1):
        q = units.Quantity(np.array([0.5, 0.2]), s)
        val, unit = system_1.convert(q)
        assert val == approx(np.array([0.5, 0.2]))
        assert unit == s

        q = units.Quantity(np.array([0.00005, 0.0002]), s)
        val, unit = system_1.convert(q)
        assert val == approx(np.array([50, 200]))
        assert unit == us

        q = units.Quantity(np.array([5000, 2000]), s)
        val, unit = system_1.convert(q)
        assert unit == min
        assert val == approx(np.array([5000/60, 2000/60]))

    def test_convert_no_match(self, system_1):
        q = units.Quantity(np.array([1.0]), units.Unit.base(bases.MASS))
        with pytest.raises(ValueError):
            system_1.convert(q)
    
    def test_convert_edge(self, system_1):
        q = units.Quantity(np.array([0.1, 0.05]), m)
        val, unit = system_1.convert(q)
        assert unit == mm
        assert val == approx(np.array([100.0, 50.0]))

        q = units.Quantity(np.array([0.1, 0.01]), s)
        val, unit = system_1.convert(q)
        assert unit == ms
        assert val == approx(np.array([100.0, 10.0]))

    def test_convert_small(self, system_1):
        q = units.Quantity(np.array([0.00005, 0.00004]), m)
        val, unit = system_1.convert(q)
        assert val == approx(np.array([0.05, 0.04]))
        assert unit == mm

        q = units.Quantity(np.array([0.0000005, 0.0000004]), s)
        val, unit = system_1.convert(q)
        assert unit == us
        assert val == approx(np.array([0.5, 0.4]))

    def test_convert_large(self, system_1):
        q = units.Quantity(np.array([5000000, 7000000]), m)
        val, unit = system_1.convert(q)
        assert val == approx(np.array([5000.0, 7000.0]))
        assert unit == km

        q = units.Quantity(np.array([50000000, 70000000]), s)
        val, unit = system_1.convert(q)
        assert val == approx(np.array([13888.88888888889, 19444.444444444443]))
        assert unit == hr

    def test_call(self, system_1):
        q = units.Quantity(np.array([0.05, 0.04]), m)
        val, unit = system_1(q)
        assert val == approx(np.array([50.0, 40.0]))
        assert unit == mm

