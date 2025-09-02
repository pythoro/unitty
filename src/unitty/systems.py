from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

from . import units


class Measure:
    def __init__(self, unit_list: list[units.Unit]):
        self._unit_list = unit_list
        self._unit_abbrs = {u.abbr: u for u in unit_list}

    def __call__(
        self, quantity: units.Quantity
    ) -> tuple[float | NDArray, units.Unit]:
        return self.convert(quantity)

    def convert(
        self, quantity: units.Quantity
    ) -> tuple[float | NDArray, units.Unit]:
        converteds = []
        ratios = []
        for out_unit in self._unit_list:
            converted = quantity.to(out_unit)
            abs_conv = np.mean(np.abs(converted))
            ratio = abs_conv / 10.0 if abs_conv >= 10 else 10.0 / abs_conv
            converteds.append(converted)
            ratios.append(ratio)
        # Find the index of the minimum difference
        min_index = ratios.index(min(ratios))
        return converteds[min_index], self._unit_list[min_index]

    def get_unit_by_str(self, abbr: str) -> units.Unit:
        """Get a unit by its abbreviation.
        
        Args:
            abbr (str): The abbreviation of the unit to retrieve. This should
                exactly match the abbreviation used when the unit was created,
                or the derived abbreviation (unit.abbr).

        Returns:
            units.Unit: The corresponding Unit instance.

        Raises:
            ValueError: If the unit abbreviation is not found in the measure.
        """
        if abbr not in self._unit_abbrs:
            raise ValueError(f"Unit '{abbr}' not found in measure.")
        return self._unit_abbrs[abbr]


class Measures(dict[str, Measure]):
    pass


class UnitSystem:
    def __init__(self, measures: Measures):
        self._measures = measures

    def __call__(
        self, unit: units.Quantity
    ) -> tuple[float | NDArray, units.Unit]:
        return self.convert(unit)

    def convert(
        self, unit: units.Quantity
    ) -> tuple[float | NDArray, units.Unit]:
        for measure in self._measures.values():
            try:
                return measure.convert(unit)
            except ValueError:
                continue
        raise ValueError("No suitable measure found.")

    def set_measures(self, measures: Measures):
        """Set the Measures instance for the system.
        
        Args:
            measures (Measures): The Measures instance to set. This can be
                used to change the measurement system dynamically.
        """
        self._measures = measures

    def get_unit_by_str(self, abbr: str) -> units.Unit:
        """Get a unit by its abbreviation from any measure.
        
        Args:
            abbr (str): The abbreviation of the unit to retrieve. This should
                exactly match the abbreviation used when the unit was created,
                or the derived abbreviation (unit.abbr).

        Returns:
            units.Unit: The corresponding Unit instance.
        
        Raises:
            ValueError: If the unit abbreviation is not found in any measure.
                
        """
        for measure in self._measures.values():
            try:
                return measure.get_unit_by_str(abbr)
            except ValueError:
                continue
        raise ValueError(f"Unit '{abbr}' not found in any measure.")