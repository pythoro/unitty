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

INV_MULT_DERIVS = {v: k for k, v in MULT_DERIVATIONS.items()}
INV_DIV_DERIVS = {v: k for k, v in DIV_DERIVATIONS.items()}

def split_single(t):
    if t in INV_MULT_DERIVS:
        t1, t2 = INV_MULT_DERIVS[t]
        return [t1, t2], []
    if t in INV_DIV_DERIVS:
        t1, t2 = INV_DIV_DERIVS[t]
        return [t1], [t2]
    return [t], []
    
def _split_compound_once(t):
    num = []
    den = []
    for n in t['num']:
        num_new, den_new = split_single(n)
        num.extend(num_new)
        den.extend(den_new)
    for n in t['den']:
        den_new, num_new = split_single(n)
        num.extend(num_new)
        den.extend(den_new)
    return {'num': num, 'den': den}

def split_compound(t):
    t1 = _split_compound_once(t)
    while True:
        t2 = _split_compound_once(t1)
        if t2['num'] == t1['num'] and t2['den'] == t1['den']:
            break
        t1 = t2
    return t2

def ensure_compound(t):
    if not isinstance(t, dict):
        return {'num': [t], 'den': []}
    return t

def tidy_compound(t):
    for n in t['num'].copy():
        if n in t['den']:
            t['num'].remove(n)
            t['den'].remove(n)
    return t

def get_compound_type(t1, t2, method='mult'):
    # TODO: Break apart complex types like pressure
    t1 = ensure_compound(t1)
    t2 = ensure_compound(t2)
    t1 = split_compound(t1)
    t2 = split_compound(t2)
    if method == 'mult':
        num = t1['num'] + t2['num']
        den = t1['den'] + t2['den']
    else:
        num = t1['num'] + t2['den']
        den = t1['den'] + t2['num']       
    out = {'num': num, 'den': den}
    return tidy_compound(out)


def get_mult_type(t1, t2):
    if isinstance(t1, dict) or isinstance(t2, dict):
        return get_compound_type(t1, t2, 'mult')
    if (t1, t2) in MULT_DERIVATIONS:
        return MULT_DERIVATIONS[(t1, t2)]
    elif (t2, t1) in MULT_DERIVATIONS:
        return MULT_DERIVATIONS[(t2, t1)]
    else:
        out = {'num': [t1, t2], 'den': []}
        out = split_compound(out)
        return tidy_compound(out)

def get_div_type(t1, t2):
    if isinstance(t1, dict) or isinstance(t2, dict):
        return get_compound_type(t1, t2, 'div')
    if (t1, t2) in DIV_DERIVATIONS:
        return DIV_DERIVATIONS[(t1, t2)]
    else:
        out = {'num': [t1], 'den': [t2]}
        out = split_compound(out)
        return tidy_compound(out)



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
        return Quantity(self.value * other, unit_type=self.unit_type)

    def __pow__(self, other, modulo=None):
        if not isinstance(other, int):
            raise ValueError('Can only raise units to integer powers.')
        return self._pow(other)
    
    def __truediv__(self, other):
        if isinstance(other, Quantity):
            return self._div(other)
        return Quantity(self.value / other, unit_type=self.unit_type)

    def __rmul__(self, other):
        if isinstance(other, Quantity):
            return self._mul(other)
        return Quantity(self.value * other, unit_type=self.unit_type)

    def __rtruediv__(self, other):
        if isinstance(other, Quantity):
            return self._div(other)
        return Quantity(self.value / other, unit_type=self.unit_type)
    
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
        
            
    