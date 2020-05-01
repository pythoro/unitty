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


class Unit(Quantity):
    def __init__(self, abbr, value, unit_type, name):
        self.abbr = abbr
        self.unit_type = unit_type
        self.value = value
        self.name = name
        
    def __str__(self):
        return (self.abbr + ' ({:0.3g}'.format(self.value) 
                               + ' ' + unit_bases[self.unit_type]) + ')'

    def __repr__(self):
        return self.__str__()

    def __rmatmul__(self, other):
        return other * self.value

    def __rrshift__(self, other):
        return other / self.value
    

