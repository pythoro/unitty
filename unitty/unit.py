# -*- coding: utf-8 -*-
"""
Created on Fri May  1 11:51:58 2020

@author: Reuben
"""

from .quantity import Quantity

class Unit(Quantity):
    def __init__(self, abbr, value, vector, spec, name):
        self.abbr = abbr
        self.value = value
        self.vector = vector
        self.spec = spec
        self.name = name
        
    def __str__(self):
        return self.base_unitise()

    def __repr__(self):
        return self.__str__()

    def __rlshift__(self, other):
        if not isinstance(other, Quantity):
            raise ValueError('Quantity not recognised.')
        other.set_unit(self)

    def __rrshift__(self, other):
        return other / self.value
    
    def __rmatmul__(self, other):
        return Quantity(self.value * other, spec=self.spec,
                        vector=self.vector)
    