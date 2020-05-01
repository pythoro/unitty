# -*- coding: utf-8 -*-
"""
Created on Fri May  1 11:51:58 2020

@author: Reuben
"""

from .quantity import Quantity

class Unit():
    def __init__(self, name, mult, unit_type, base_unit):
        self.name = name
        self.unit_type = unit_type
        self.mult = mult
        self.base_unit = base_unit
        
    def __str__(self):
        return (self.name + ' ({:0.3g}'.format(self.mult) 
                               + ' x ' + self.unit_type) + ')'

    def __repr__(self):
        return self.__str__()

    def __rmul__(self, other):
        return Quantity(other * self.mult, self.unit_type)


class Units(dict):
    def __getattr__(self, name):
        if name in self:
            return self[name]
        return self.__getattribute__(name)