from __future__ import annotations

from numpy.typing import NDArray
from . import bases
from dataclasses import dataclass
import numpy as np
from typing import Any


@dataclass
class Spec:
    """A simple structure to hold unit specification information."""

    order: float
    abbr: str


class Unit:
    """The core unit object."""

    def __init__(
        self, value: float, spec: str | list[Spec], vector: NDArray, desc: str
    ) -> None:
        """Initialize a Unit instance.

        Args:
            value (int, float, arraylike) : A float representing the magnitude of
                the quantity in terms of base dimensions (length, time, mass, etc)
            spec: A list of Spec instances, or a string abbreviation of the unit.
            vector (ndarray): Each base dimensions is independent, and the exponent
                for each base dimension is represented as a number. This vectore is
                an array of such numbers for all base dimensions. This allows quick
                and robust dimensionality checking.
            desc (str): A description of the unit.

        Note:
            Normally, Quantities would only be created automatically or from
            other Quantities, not directly by the user.
        """
        if isinstance(spec, str):
            spec = [Spec(1.0, spec)]
        self.value = value
        self.spec = spec
        self.vector = vector
        self.desc = desc

    @classmethod
    def base(cls, base_key: str):
        """Create a base unit from a base key."""
        value = 1.0
        spec = [Spec(1.0, base_key)]
        vector = np.zeros(bases.NUM_BASES, dtype=float)
        vector[bases.INDICES[base_key]] = 1.0
        desc = f"Base unit: {base_key}"
        return cls(value, spec, vector, desc)

    @classmethod
    def named(cls, factor: float, unit: Unit, abbr: str, desc: str):
        """Create a base unit from a base key."""
        value = factor * unit.value
        spec = [Spec(1.0, abbr)]
        vector = unit.vector.copy()
        desc = desc
        return cls(value, spec, vector, desc)

    def to(self, unit: Unit):
        """Return this quantity expressed in the given unit."""
        if any(unit.vector != self.vector):
            raise ValueError("Incompatible quantity type")
        print(type(self.value / unit.value))
        return self.value / unit.value

    def _create(
        self, value: float, spec: list[Spec], vector: NDArray, desc: str
    ):
        return Unit(value, spec, vector, desc)

    def __str__(self):
        numerators = [s for s in self.spec if s.order > 0]
        denominators = [s for s in self.spec if s.order < 0]
        str_numerators = ".".join(
            [
                f"{s.abbr}^{s.order}" if s.order != 1.0 else s.abbr
                for s in numerators
            ]
        )
        str_denominators = ".".join(
            [
                f"{s.abbr}^{-s.order}" if s.order != -1.0 else s.abbr
                for s in denominators
            ]
        )
        if len(denominators) > 1:
            str_denominators = f"({str_denominators})"
        if len(denominators) > 0:
            return f"{str_numerators}/{str_denominators}"
        else:
            return f"{str_numerators}"

    def _mul(self, other: Unit):
        value = self.value * other.value
        spec = self.spec.copy()
        spec.extend(other.spec)
        vector = self.vector + other.vector
        desc = "Derived unit"
        return Unit(value, spec, vector, desc)

    def _div(self, other: Unit):
        value = self.value * other.value
        spec = self.spec.copy()
        other_spec = [Spec(-s.order, s.abbr) for s in other.spec]
        spec.extend(other_spec)
        vector = self.vector - other.vector
        desc = "Derived"
        return Unit(value, spec, vector, desc)

    def _pow(self, order: float | int):
        value = self.value**order
        spec = [Spec(s.order * order, s.abbr) for s in self.spec]
        vector = self.vector * order
        desc = "Derived"
        return Unit(value, spec, vector, desc)

    def __mul__(self, other: Unit):
        is_unit = isinstance(other, Unit)
        if is_unit:
            return self._mul(other)
        value = self.value * other
        return self._create(value, self.spec, self.vector, "Derived")

    def __rmul__(self, other: Unit):
        is_unit = isinstance(other, Unit)
        if is_unit:
            return self._mul(other)
        value = self.value * other
        return self._create(value, self.spec, self.vector, "Derived")

    def __pow__(self, exponent: float, modulo=None):
        if not isinstance(exponent, float | int):
            raise ValueError(
                "Can only raise units to float or integer powers."
            )
        return self._pow(exponent)

    def __rpow__(self, other: Any, modulo=None):
        raise ValueError(
            "Units cannot be used as exponents."
        )

    def __truediv__(self, other: Unit):
        is_unit = isinstance(other, Unit)
        if is_unit:
            return self._div(other)
        value = self.value / other
        return self._create(value, self.spec, self.vector, "Derived")
