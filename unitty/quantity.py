# -*- coding: utf-8 -*-
"""
Created on Fri May  1 11:52:26 2020

@author: Reuben
"""

systems = None

def set_systems(sys):
    global systems
    systems = sys




class Quantity():
    def __init__(self, value, unit_type):
        self.value = value
        self.unit_type = unit_type
        self._unit = None
        
    def set_unit(self, unit):
        if unit.unit_type != self.unit_type:
            raise ValueError('Incompatible quantity type')
        self._unit = unit
        
    def in_units(self, unit=None):
        u = self._unit if self._unit is not None else None
        u = unit if unit is not None else u
        if u is not None:
            if u.unit_type != self.unit_type:
                raise ValueError('Incompatible quantity type')
            value = self.value / u.value
            abbr = u.abbr
        else:
            value, abbr = systems.unitise(self.value, self.unit_type)
            if abbr is None:
                return '{:0.3g}'.format(value)
        return value, abbr
    
    def __str__(self):
        value, abbr = self.in_units()
        return '{:0.3g}'.format(value) + ' ' + abbr
    
    def __repr__(self):
        return self.__str__()

    def __mul__(self, other):
        if isinstance(other, Quantity):
            return self._mul(other)
        return self.value * other

    def __pow__(self, other, modulo=None):
        if not isinstance(other, int):
            raise ValueError('Can only raise units to integer powers.')
        return self._pow(other)
    
    def __truediv__(self, other):
        if isinstance(other, Quantity):
            return self._div(other)
        return self.value / other

    def __rmul__(self, other):
        if isinstance(other, Quantity):
            return self._mul(other)
        return self.value * other

    def __rtruediv__(self, other):
        if isinstance(other, Quantity):
            return self._div(other)
        return self.value / other
    
    def _mul(self, other):
        unit_type = get_mult_type(self.unit_type, other.unit_type)
        return Quantity(self.value * other.value, unit_type=unit_type)

    def _div(self, other):
        unit_type = get_div_type(self.unit_type, other.unit_type)
        return Quantity(self.value / other.value, unit_type=unit_type)

    def _pow(self, other):
        new = self
        for n in range(other - 1):
            new = new._mul(self)
        return new
            