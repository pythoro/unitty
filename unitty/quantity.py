# -*- coding: utf-8 -*-
"""
Created on Fri May  1 11:52:26 2020

@author: Reuben
"""

systems = None

def set_systems(sys):
    global systems
    systems = sys

class Quantity():
    def __init__(self, value, unit_type):
        self.value = value
        self.unit_type = unit_type
        
    def __str__(self):
        value, unit = systems.unitise(self.value, self.unit_type)
        return '{:0.3g}'.format(value) + ' ' + unit
    
    def __repr__(self):
        return self.__str__()
    
    def __mul__(self, other):
        return self.value.__mul__(other)
    
    def __rmul__(self, other):
        return self.value.__rmul__(other)