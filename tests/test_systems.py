from unitty import systems, units, bases
import pytest
from pytest import approx


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
        q1 = units.Quantity(0.5, m)
        val, unit = measure_1.convert(q1)
        assert unit == m
        assert val == 0.5

        q2 = units.Quantity(0.05, m)
        val, unit = measure_1.convert(q2)
        assert unit == mm
        assert val == 50.0

        q3 = units.Quantity(0.005, m)
        val, unit = measure_1.convert(q3)
        assert unit == mm
        assert val == 5.0

        q4 = units.Quantity(500, m)
        val, unit = measure_1.convert(q4)
        assert unit == km
        assert val == 0.5

    
    def test_convert_no_match(self, measure_1):
        q = units.Quantity(1.0, units.Unit.base(bases.MASS))
        with pytest.raises(ValueError):
            measure_1.convert(q)

    def test_convert_edge(self, measure_1):
        q = units.Quantity(0.1, m)
        val, unit = measure_1.convert(q)
        assert unit == mm
        assert val == 100.0

    def test_convert_small(self, measure_1):
        q = units.Quantity(0.00005, m)
        val, unit = measure_1.convert(q)
        assert val == 0.05
        assert unit == mm

    def test_convert_large(self, measure_1):
        q = units.Quantity(5000000, m)
        val, unit = measure_1.convert(q)
        assert val == 5000.0
        assert unit == km

    def test_call(self, measure_1):
        q1 = units.Quantity(0.5, m)
        val, unit = measure_1(q1)
        assert val == 0.5
        assert unit == m

    def test_get_unit_by_str(self, measure_1):
        assert measure_1.get_unit_by_str("mm") == mm
        assert measure_1.get_unit_by_str("m") == m
        assert measure_1.get_unit_by_str("km") == km
        with pytest.raises(ValueError):
            measure_1.get_unit_by_str("ft")



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
        q = units.Quantity(0.5, m)
        val, unit = system_1.convert(q)
        assert val == 0.5
        assert unit == m

        q = units.Quantity(0.05, m)
        val, unit = system_1.convert(q)
        assert val == 50.0
        assert unit == mm

        q = units.Quantity(500, m)
        val, unit = system_1.convert(q)
        assert val == 0.5
        assert unit == km

    def test_convert_time(self, system_1):
        q = units.Quantity(0.5, s)
        val, unit = system_1.convert(q)
        assert val == 0.5
        assert unit == s

        q = units.Quantity(0.00005, s)
        val, unit = system_1.convert(q)
        assert val == approx(50)
        assert unit == us

        q = units.Quantity(5000, s)
        val, unit = system_1.convert(q)
        assert val == approx(1.3888888888888888)
        assert unit == hr

    def test_convert_no_match(self, system_1):
        q = units.Quantity(1.0, units.Unit.base(bases.MASS))
        with pytest.raises(ValueError):
            system_1.convert(q)
    
    def test_convert_edge(self, system_1):
        q = units.Quantity(0.1, m)
        val, unit = system_1.convert(q)
        assert unit == mm
        assert val == 100.0

        q = units.Quantity(0.1, s)
        val, unit = system_1.convert(q)
        assert unit == ms
        assert val == 100.0

    def test_convert_small(self, system_1):
        q = units.Quantity(0.00005, m)
        val, unit = system_1.convert(q)
        assert val == 0.05
        assert unit == mm

        q = units.Quantity(0.0000005, s)
        val, unit = system_1.convert(q)
        assert val == 0.5
        assert unit == us

    def test_convert_large(self, system_1):
        q = units.Quantity(5000000, m)
        val, unit = system_1.convert(q)
        assert val == approx(5000.0)
        assert unit == km

        q = units.Quantity(50000000, s)
        val, unit = system_1.convert(q)
        assert val == approx(13888.88888888889)
        assert unit == hr

    def test_call(self, system_1):
        q = units.Quantity(0.05, m)
        val, unit = system_1(q)
        assert val == 50.0
        assert unit == mm

    def test_switch_measures(self, system_1, measures_2):
        q = units.Quantity(0.05, m)
        val, unit = system_1(q)
        assert val == 50.0
        assert unit == mm

        system_1.set_measures(measures_2)
        val, unit = system_1(q)
        assert unit == _in
        assert val == approx(1.968503937007874)
        
    def test_get_unit_by_str(self, system_1):
        assert system_1.get_unit_by_str("mm") == mm
        assert system_1.get_unit_by_str("m") == m
        assert system_1.get_unit_by_str("km") == km
        assert system_1.get_unit_by_str("s") == s
        assert system_1.get_unit_by_str("ms") == ms
        assert system_1.get_unit_by_str("hr") == hr
        with pytest.raises(ValueError):
            system_1.get_unit_by_str("ft")
        with pytest.raises(ValueError):
            system_1.get_unit_by_str("kg")
        
