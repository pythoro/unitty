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
    def __init__(self, value, unit_type, unit_vec):
        self.value = value
        self.unit_type = unit_type
        self.unit_vec = unit_vec
        
    def set_unit(self, unit):
        if unit.unit_vec != self.unit_vec:
            raise ValueError('Incompatible quantity type')
        self.unit_type = unit.unit_type
        
    def _str_unit_type(self, unit_type):
        if unit_type is None:
            return 'base'
        elif len(unit_type)==0:
            return 'dimensionless'
        num = [ut for ut in unit_type if not ut.startswith('-')]
        den = [ut[1:] for ut in unit_type if ut.startswith('-')]
        s_num = '1' if len(num) == 0 else '.'.join(num)
        n = len(den)
        if n == 0:
            return s_num
        elif n == 1:
            return s_num + '/' + den[0]
        else:
            return s_num + '/(' + '.'.join(den) + ')'
        
    def in_units(self, unit=None):
        if unit is not None:
            if unit.unit_vec != self.unit_vec:
                raise ValueError('Incompatible quantity type')
            unit_type = unit.unit_type
        else:
            unit_type = self.unit_type
        value = systems.unitise_typed(self.value, self.unit_type)
        return value, unit_type

    def unitise(self):
        return systems.unitise(self.value, self.unit_vec, in_base=False)

    def in_base(self):
        return systems.unitise(self.value, self.unit_vec, in_base=True)
    
    def __str__(self):
        value, unit_type = self.in_units()
        return ('{:0.3g}'.format(value) + ' ' 
                + self._str_unit_type(unit_type))
    
    def __repr__(self):
        return self.__str__()

    def __mul__(self, other):
        if isinstance(other, Quantity):
            return self._mul(other)
        return Quantity(self.value * other, unit_type=[self.abbr],
                        unit_vec=self.unit_vec)

    def __pow__(self, other, modulo=None):
        if not isinstance(other, int):
            raise ValueError('Can only raise units to integer powers.')
        return self._pow(other)
    
    def __truediv__(self, other):
        if isinstance(other, Quantity):
            return self._div(other)
        return Quantity(self.value / other, unit_type=[self.abbr],
                        unit_vec=self.unit_vec)

    def __rmul__(self, other):
        if isinstance(other, Quantity):
            return self._mul(other)
        return Quantity(self.value * other, unit_type=[self.abbr],
                        unit_vec=self.unit_vec)


    def __rtruediv__(self, other):
        if isinstance(other, Quantity):
            return self._div(other)
        ut = ['-' + u for u in self.unit_type]
        return Quantity(other / self.value, unit_type=ut,
                        unit_vec=-self.unit_vec)
    
    def _mul(self, other):
        unit_type = [self.abbr]
        unit_type.append(other.abbr)
        unit_vec = self.unit_vec + other.unit_vec
        return Quantity(self.value * other.value, unit_type=unit_type,
                        unit_vec=unit_vec)

    def _div(self, other):
        unit_type = [self.abbr]
        unit_type.append('-' + other.abbr)
        unit_vec = self.unit_vec - other.unit_vec
        return Quantity(self.value / other.value, unit_type=unit_type,
                        unit_vec=unit_vec)


    def _pow(self, other):
        new = self
        for n in range(other - 1):
            new = new._mul(self)
        return new
            