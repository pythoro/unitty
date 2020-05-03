# -*- coding: utf-8 -*-
"""
Created on Fri May  1 11:51:58 2020

@author: Reuben
"""

from .quantity import Quantity

class Unit(Quantity):
    def __init__(self, abbr, value, unit_vec, unit_type, name, base_type):
        self.abbr = abbr
        self.value = value
        self.unit_vec = unit_vec
        self.unit_type = unit_type
        self.name = name
        self.base_type = base_type
        
    def __str__(self):
        value, unit_type = self.unitise()
        return (self.abbr + ' ({:0.3g}'.format(value) 
                    + ' ' + self._str_unit_type(unit_type) + ')')

    def __repr__(self):
        return self.__str__()

    def __rlshift__(self, other):
        if not isinstance(other, Quantity):
            raise ValueError('Quantity not recognised.')
        other.set_unit(self)

    def __rrshift__(self, other):
        return other / self.value
    
    def __rmatmul__(self, other):
        return Quantity(self.value * other, unit_type=self.unit_type,
                        unit_vec=self.unit_vec)
    