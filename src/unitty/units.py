from __future__ import annotations

from dataclasses import dataclass
from typing import Callable
import numpy as np
from numpy.typing import NDArray

from . import bases


@dataclass
class Spec:
    """A simple structure to hold unit specification information.

    Attributes:
        order (float): The exponent or order of the unit.
        abbr (str): The abbreviation of the unit.
    """

    order: float
    abbr: str


class Unit:
    """The core unit object.

    Represents a physical unit with magnitude, specification,
    dimensional vector, and description.

    Attributes:
        value (float): Magnitude of the unit.
        spec (list[Spec]): List of unit specifications.
        vector (NDArray): Dimensional vector for base dimensions.
        desc (str): Description of the unit.
    """

    def __init__(
        self, value: float, spec: str | list[Spec], vector: NDArray, desc: str
    ) -> None:
        """Initialize a Unit instance.

        Args:
            value (float): Magnitude of the unit.
            spec (str | list[Spec]): Abbreviation or list of unit
                specifications.
            vector (NDArray): Dimensional vector for base dimensions.
            desc (str): Description of the unit.

        Note:
            Normally, Units would only be created automatically or from
            other Quantities, not directly by the user.
        """
        if isinstance(spec, str):
            spec = [Spec(1.0, spec)]
        self.value = value
        self.spec = spec
        self.vector = vector
        self.desc = desc

    @classmethod
    def base(cls, base_key: str) -> Unit:
        """Create a base unit from a base key.

        Args:
            base_key (str): The key representing the base unit (e.g., 'm').

        Returns:
            Unit: The created base unit.
        """
        value = 1.0
        spec = [Spec(1.0, base_key)]
        vector = np.zeros(bases.NUM_BASES, dtype=float)
        vector[bases.INDICES[base_key]] = 1.0
        desc = f"Base unit: {base_key}"
        return cls(value, spec, vector, desc)

    @classmethod
    def named(cls, factor: float, unit: Unit, abbr: str, desc: str) -> Unit:
        """Create a named unit from a base unit and factor.

        Args:
            factor (float): Multiplicative factor for the unit.
            unit (Unit): The base unit to derive from.
            abbr (str): Abbreviation for the new unit.
            desc (str): Description of the new unit.

        Returns:
            Unit: The created named unit.
        """
        value = factor * unit.value
        spec = [Spec(1.0, abbr)]
        vector = unit.vector.copy()
        desc = desc
        return cls(value, spec, vector, desc)

    def __str__(self) -> str:
        """Return a string representation of the unit.

        Returns:
            str: String representation of the unit.
        """
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

    def _mul(self, other: Unit) -> Unit:
        """Multiply two units together.

        Args:
            other (Unit): The unit to multiply with.

        Returns:
            Unit: The resulting derived unit.
        """
        value = self.value * other.value
        spec = self.spec.copy()
        spec.extend(other.spec)
        vector = self.vector + other.vector
        desc = "Derived unit"
        return Unit(value, spec, vector, desc)

    def _div(self, other: Unit) -> Unit:
        """Divide this unit by another unit.

        Args:
            other (Unit): The unit to divide by.

        Returns:
            Unit: The resulting derived unit.
        """
        value = self.value * other.value
        spec = self.spec.copy()
        other_spec = [Spec(-s.order, s.abbr) for s in other.spec]
        spec.extend(other_spec)
        vector = self.vector - other.vector
        desc = "Derived"
        return Unit(value, spec, vector, desc)

    def _pow(self, order: float | int) -> Unit:
        """Raise the unit to a power.

        Args:
            order (float | int): The exponent to raise the unit to.

        Returns:
            Unit: The resulting derived unit.
        """
        value = self.value**order
        spec = [Spec(s.order * order, s.abbr) for s in self.spec]
        vector = self.vector * order
        desc = "Derived"
        return Unit(value, spec, vector, desc)

    def __mul__(self, other: Unit) -> Unit:
        """Multiply this unit by another unit or scalar.

        Args:
            other (Unit | float | int): The unit or scalar to multiply with.

        Returns:
            Unit: The resulting unit.
        """
        is_unit = isinstance(other, Unit)
        if is_unit:
            return self._mul(other)
        value = self.value * other
        return Unit(value, self.spec, self.vector, "Derived")

    def __rmul__(self, other: Unit) -> Unit:
        """Multiply this unit by another unit or scalar (right-hand side).

        Args:
            other (Unit | float | int): The unit or scalar to multiply with.

        Returns:
            Unit: The resulting unit.
        """
        is_unit = isinstance(other, Unit)
        if is_unit:
            return self._mul(other)
        value = self.value * other
        return Unit(value, self.spec, self.vector, "Derived")

    def __rlshift__(self, value: float | int | NDArray) -> float | NDArray:
        """Shift left operation for value and unit multiplication.

        Args:
            value (float | int | NDArray): Value to multiply with the
                unit's value.

        Returns:
            float | NDArray: Result of multiplication.
        """
        return self.value * value

    def __pow__(self, exponent: float, modulo: float | None = None) -> Unit:
        """Raise the unit to a power.

        Args:
            exponent (float): The exponent to raise the unit to.
            modulo: Unused, for compatibility.

        Returns:
            Unit: The resulting unit.

        Raises:
            ValueError: If exponent is not a float or int.
        """
        if not isinstance(exponent, float | int):
            raise ValueError(
                "Can only raise units to float or integer powers."
            )
        return self._pow(exponent)

    def __rpow__(self, other: float, modulo: float | None = None) -> None:
        """Prevent units from being used as exponents.

        Args:
            other: Unused.
            modulo: Unused.

        Raises:
            ValueError: Always raised.
        """
        raise ValueError("Units cannot be used as exponents.")

    def __truediv__(self, other: Unit) -> Unit:
        """Divide this unit by another unit or scalar.

        Args:
            other (Unit | float | int): The unit or scalar to divide by.

        Returns:
            Unit: The resulting unit.
        """
        is_unit = isinstance(other, Unit)
        if is_unit:
            return self._div(other)
        value = self.value / other
        return Unit(value, self.spec, self.vector, "Derived")


class Quantity:
    """A quantity is a value with associated units.

    Attributes:
        _value (float | NDArray): The magnitude of the quantity.
        _unit (Unit): The unit associated with the quantity.
    """

    def __init__(self, value: float | NDArray, unit: Unit) -> None:
        """Initialize a Quantity instance.

        Args:
            value (float | NDArray): Magnitude of the quantity.
            unit (Unit): The unit associated with the quantity.

        Note:
            Normally, Quantities would only be created automatically or from
            other Quantities, not directly by the user.
        """
        self._value = value
        self._unit = unit

    @property
    def value(self) -> float | NDArray:
        """Get the value of the quantity in base units.

        Returns:
            float | NDArray: The value in base units.
        """
        return self._value * self._unit.value

    @property
    def unit(self) -> Unit:
        """Get the unit associated with the quantity.

        Returns:
            Unit: The unit of the quantity.
        """
        return self._unit

    def to(self, unit: Unit) -> float | NDArray:
        """Return this quantity expressed in the given unit.

        Args:
            unit (Unit): The unit to convert to.

        Returns:
            float | NDArray: The value in the given unit.

        Raises:
            ValueError: If the unit is incompatible.
        """
        if any(unit.vector != self._unit.vector):
            raise ValueError("Incompatible quantity type")
        return self.value / unit.value

    def __mul__(self, other: Quantity | float | int) -> Quantity:
        """Multiply this quantity by another quantity or scalar.

        Args:
            other (Quantity | float | int): The quantity or scalar to
                multiply with.

        Returns:
            Quantity: The resulting quantity.
        """
        if isinstance(other, Quantity):
            value = self._value * other._value
            new_unit = self._unit * other._unit
            return Quantity(value, new_unit)
        return Quantity(self._value * other, self._unit)

    def __rmul__(self, other: Quantity | float | int) -> Quantity:
        """Multiply this quantity by another quantity or scalar.

        Args:
            other (Quantity | float | int): The quantity or scalar
                to multiply with.

        Returns:
            Quantity: The resulting quantity.
        """
        if isinstance(other, Quantity):
            value = self._value * other._value
            new_unit = self._unit * other._unit
            return Quantity(value, new_unit)
        return Quantity(self._value * other, self._unit)

    def __truediv__(self, other: Quantity | float | int) -> Quantity:
        """Divide this quantity by another quantity or scalar.

        Args:
            other (Quantity | float | int): The quantity or scalar
                to divide by.

        Returns:
            Quantity: The resulting quantity.
        """
        if isinstance(other, Quantity):
            value = self._value / other._value
            new_unit = self._unit / other._unit
            return Quantity(value, new_unit)
        return Quantity(self._value / other, self._unit)

    def __rlshift__(self, value: float | int | NDArray) -> float | NDArray:
        """Shift left operation for value and quantity multiplication.

        Args:
            value (float | int | NDArray): Value to multiply with the
                quantity's value.

        Returns:
            float | NDArray: Result of multiplication.
        """
        return self.value * value

    def __pow__(
        self, exponent: float, modulo: float | None = None
    ) -> Quantity:
        """Raise the quantity to a power.

        Args:
            exponent (float): The exponent to raise the quantity to.
            modulo: Unused, for compatibility.

        Returns:
            Quantity: The resulting quantity.

        Raises:
            ValueError: If exponent is not a float or int.
        """
        if not isinstance(exponent, float | int):
            raise ValueError(
                "Can only raise units to float or integer powers."
            )
        value = self._value**exponent
        new_unit = self._unit**exponent
        return Quantity(value, new_unit)

    def __rpow__(self, other: float, modulo: float | None = None) -> None:
        """Prevent quantities from being used as exponents.

        Args:
            other: Unused.
            modulo: Unused.

        Raises:
            ValueError: Always raised.
        """
        raise ValueError("Units cannot be used as exponents.")

    def __array__(self) -> NDArray:
        """For numpy interoperability.

        Returns:
            np.ndarray: Numpy array of the quantity value.

        See:
            https://numpy.org/devdocs/user/basics.dispatch.html
        """
        return np.array(self.value)

    def __array_ufunc__(
        self,
        ufunc: Callable,
        method: str,
        *inputs: float | Quantity,
        **kwargs: float | str,
    ) -> Quantity:
        """For numpy interoperability with ufuncs.

        Args:
            ufunc: The numpy ufunc.
            method: The method name.
            *inputs: Input arguments.
            **kwargs: Keyword arguments.

        Returns:
            Quantity | NotImplemented: Resulting quantity or NotImplemented.

        See:
            https://numpy.org/devdocs/user/basics.dispatch.html
        """
        ufunc_name = ufunc.__name__
        if method != "__call__":
            return NotImplemented
        if ufunc_name == "multiply":
            value = inputs[0] * inputs[1].value
            return Quantity(value, self._unit)
        if ufunc_name == "power":
            order = inputs[1]
            value = self.value**order
            new_unit = self._unit**order
            return Quantity(value, new_unit)
        elif ufunc_name == "true_divide":
            value = inputs[0] / inputs[1].value
            return Quantity(value, self._unit)
        return NotImplemented
