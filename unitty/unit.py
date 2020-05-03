# -*- coding: utf-8 -*-
"""
Created on Fri May  1 11:51:58 2020

@author: Reuben
"""

from .quantity import Quantity

class Unit():
    def __init__(self, abbr, value, unit_vec, unit_type, name):
        self.abbr = abbr
        self.value = value
        self.unit_vec = unit_vec
        self.unit_type = unit_type
        self.name = name
        
    def str_unit_type(self):
        num = [ut for ut in self.unit_type if not ut.startswith('-')]
        den = [ut[1:] for ut in self.unit_type if ut.startswith('-')]
        s_num = '1' if len(num) == 0 else '.'.join(num)
        n = len(den)
        if n == 0:
            return s_num
        elif n == 1:
            print(den)
            return s_num + '/' + den[0]
        else:
            return s_num + '/(' + '.'.join(den) + ')'
        
    def __str__(self):
        return (self.abbr + ' ({:0.3g}'.format(self.value) 
                               + ' ' + self.str_unit_type() + ')')

    def __repr__(self):
        return self.__str__()

    def __rlshift__(self, other):
        if not isinstance(other, Quantity):
            raise ValueError('Quantity not recognised.')
        other.set_unit(self)

    def __rrshift__(self, other):
        return other / self.value
    
    def __rmatmul__(self, other):
        return Quantity(self.value * other, unit_type=self.unit_type)
    