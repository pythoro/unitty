# -*- coding: utf-8 -*-
"""
Created on Fri May  1 11:51:58 2020

@author: Reuben
"""

from .quantity import Quantity

base = None
unit_bases = None

def set_base(b):
    global base, unit_bases
    base = b
    unit_bases = b.bases


def derive_mult(*unit_types):
    types = list(unit_types)
    types.sort()
    if len(types) == 2:
        t1, t2 = types
        if t1 == 'area':
            if t2 == 'length':
                return 'volume'
        elif t1 == 'length':
            if t2 == 'length':
                return 'area'
            elif t2 == 'area':
                return 'volume'
        elif t1 == 'force':
            if t2 == 'length':
                return 'energy'
    raise ValueError('Cannot multiply ' + str(types))


def derive_div(*unit_types):
    types = list(unit_types)
    if len(types) == 2:
        t1, t2 = types
        if t1 == 'force':
            if t2 == 'area':
                return 'pressure'
        elif t1 == 'mass':
            if t2 == 'volume':
                return 'density'
    raise ValueError('Cannot divide ' + str(types))

class Unit():
    def __init__(self, abbr, mult, unit_type, name):
        self.abbr = abbr
        self.unit_type = unit_type
        self.mult = mult
        self.name = name
        
    def __str__(self):
        return (self.abbr + ' ({:0.3g}'.format(self.mult) 
                               + ' ' + unit_bases[self.unit_type]) + ')'

    def __repr__(self):
        return self.__str__()

    def __mul__(self, other):
        if isinstance(other, Unit):
            new_unit_type = self.mul_type(other.unit_type)
            return Quantity(other.mult * self.mult, new_unit_type)
        else:
            return Quantity(other * self.mult, self.unit_type)

    def __rmul__(self, other):
        return Quantity(other * self.mult, self.unit_type)

    def __truediv__(self, other):
        if isinstance(other, Unit):
            new_unit_type = self.div_type(other.unit_type)
            return Quantity(other.mult * self.mult, new_unit_type)
        else:
            return Quantity(other * self.mult, self.unit_type)

    def __rtruediv__(self, other):
        return Quantity(other * self.mult, self.unit_type)

    def __rmatmul__(self, other):
        return other * self.mult

    def __rrshift__(self, other):
        return other / self.mult
    

class Units(dict):
    def __getattr__(self, abbr):
        if abbr in self:
            return self[abbr]
        return self.__getattribute__(abbr)
    
    
class Length(Unit):
    def mul_type(self, typ):
        if typ == 'length':
            return 'area'
        if typ == 'area':
            return 'volume'
        raise ValueError('Can not multiply length by ' + typ)


class Area(Unit):
    pass

class Volume(Unit):
    pass

class Force(Unit):
    pass

class Unit_Factory():
    @classmethod
    def new(cls, **dct):
        t = dct['unit_type']
        if t == 'length':
            return Length(**dct)
        elif t == 'area':
            return Area(**dct)
        elif t == 'volume':
            return Volume(**dct)
        else:
            return Unit(**dct)
        
