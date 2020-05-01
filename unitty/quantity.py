# -*- coding: utf-8 -*-
"""
Created on Fri May  1 11:52:26 2020

@author: Reuben
"""

systems = None

def set_systems(sys):
    global systems
    systems = sys

MULT_DERIVATIONS = {
        ('length', 'length'): 'area',
        ('length', 'area'): 'volume',
        ('force', 'length'): 'energy',
    }

DIV_DERIVATIONS = {
        ('length', 'area'): 'volume',
        ('mass', 'volume'): 'density',
        ('force', 'area'): 'pressure',
        ('length', 'time'): 'speed',
        ('energy', 'time'): 'power',
    }


def get_compound_type(t1, t2, method='mult'):
    # TODO: Break apart complex types like pressure
    if not isinstance(t1, dict):
        t1 = {'num': [t1], 'den': []}
    if not isinstance(t2, dict):
        t2 = {'num': [t2], 'den': []}
    if method == 'mult':
        num = t1['num'] + t2['num']
        den = t1['den'] + t2['den']
    else:
        num = t1['num'] + t2['den']
        den = t1['den'] + t2['num']       
    for n in num.copy():
        if n in den:
            num.remove(n)
            den.remove(n)        
    return {'num': num, 'den': den}


def get_mult_type(t1, t2):
    if isinstance(t1, dict) or isinstance(t2, dict):
        return get_compound_type(t1, t2, 'mult')
    if (t1, t2) in MULT_DERIVATIONS:
        return MULT_DERIVATIONS[(t1, t2)]
    elif (t2, t1) in MULT_DERIVATIONS:
        return MULT_DERIVATIONS[(t2, t1)]
    else:
        return {'num': [t1, t2], 'den': []}

def get_div_type(t1, t2):
    if isinstance(t1, dict) or isinstance(t2, dict):
        return get_compound_type(t1, t2, 'div')
    if (t1, t2) in DIV_DERIVATIONS:
        return DIV_DERIVATIONS[(t1, t2)]
    else:
        return {'num': [t1], 'den': [t2]}


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
        
            
    