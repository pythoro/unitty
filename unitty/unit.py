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


