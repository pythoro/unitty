from __future__ import annotations

from . import units
from numpy.typing import NDArray


class Measure:
    def __init__(self, unit_list: list[units.Unit]):
        self._unit_list = unit_list

    def convert(
        self, quantity: units.Quantity
    ) -> tuple[float | NDArray, units.Unit]:
        for out_unit in self._unit_list[::-1]:
            res = quantity.to(out_unit)
            if res >= 0.1:
                return res, out_unit
        return quantity.to(self._unit_list[0]), self._unit_list[0]


class Measures(dict[str, Measure]):
    pass


class MeasurementSystem:
    def __init__(self, measures: Measures):
        self._measures = measures

    def convert(
        self, unit: units.Quantity
    ) -> tuple[float | NDArray, units.Unit]:
        for measure in self._measures.values():
            try:
                return measure.convert(unit)
            except ValueError:
                continue
        raise ValueError("No suitable measure found.")
