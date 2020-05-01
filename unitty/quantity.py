# -*- coding: utf-8 -*-
"""
Created on Fri May  1 11:52:26 2020

@author: Reuben
"""

systems = None

def set_systems(sys):
    global systems
    systems = sys

DERIVATIONS = {
    'length * length': 'area',
    'length / length': None,
    'length * area': 'volume',
    'area * length': 'volume',
    'area / area': None,
    'mass / volume': 'density',
    'mass / mass': None,
    'force / area': 'pressure',
    'force / force': None,
    'force * length': 'energy',
    'length * force': 'energy',
    'length / time': 'speed',
    'time / time': None,
    'energy / time': 'power',
    'energy / energy': None,
    }


def derive_unit(s):
    if s in DERIVATIONS:
        return DERIVATIONS[s]
    else:
        raise ValueError(s + ' does not match a known unit type.')

def get_mult_type(t1, t2):
    return t1 + ' * ' + t2

def get_div_type(t1, t2):
    return t1 + ' / ' + t2


class Quantity():
    def __init__(self, value, unit_type):
        self.value = value
        self.unit_type = unit_type
        
    def __str__(self):
        value, unit = systems.unitise(self.value, self.unit_type)
        if unit is None:
            return '{:0.3g}'.format(value)
        return '{:0.3g}'.format(value) + ' ' + unit
    
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
        return other / self.value
    
    def _mul(self, other):
        s = get_mult_type(self.unit_type, other.unit_type)
        unit_type = derive_unit(s)
        return Quantity(self.value * other.value, unit_type=unit_type)

    def _div(self, other):
        s = get_div_type(self.unit_type, other.unit_type)
        unit_type = derive_unit(s)
        return Quantity(self.value / other.value, unit_type=unit_type)

    def _pow(self, other):
        new = self
        for n in range(other - 1):
            new = new._mul(self)
        return new
        
            