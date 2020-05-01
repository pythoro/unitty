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

    def __rmatmul__(self, other):
        return Quantity(other * self.mult, self.unit_type)

    def __rmul__(self, other):
        return other * self.mult

    def __rrshift__(self, other):
        return other / self.mult


class Units(dict):
    def __getattr__(self, abbr):
        if abbr in self:
            return self[abbr]
        return self.__getattribute__(abbr)