# -*- coding: utf-8 -*-
"""
Created on Fri May  1 11:52:26 2020

@author: Reuben
"""

from . import settings
import numpy as np

systems = None

def set_systems(sys):
    global systems
    systems = sys

units = None

def set_units(u):
    global units
    units = u


class Quantity():
    def __init__(self, value, spec, vector):
        self.value = value
        self.spec = spec
        self.vector = vector
        
    def set_unit(self, unit):
        if unit.vector != self.vector:
            raise ValueError('Incompatible quantity type')
        self.spec = unit.spec
                
    def _in_units(self, unit=None):
        if unit is not None:
            if unit.vector != self.vector:
                raise ValueError('Incompatible quantity type')
            spec = unit.spec
            value = self.value * unit.value
        else:
            spec = self.spec
            value = self.value
        value = systems.unitise_typed(value, spec)
        return value, spec

    def in_units(self, unit=None):
        return self._to_str(*self._in_units(unit))

    def _unitise(self):
        return systems.unitise(self.value, self.spec)

    def unitise(self):
        return self._to_str(*self._unitise())

    def _base_unitise(self):
        return systems.base_unitise(self.value, self.vector)
    
    def base_unitise(self):
        return self._to_str(*self._base_unitise())
    
    def _to_str(self, value, spec):
        if isinstance(value, np.ndarray):
            f = str(value)
        else:
            f = '{:0.6g}'.format(value)
        return f + ' ' + units.str_spec(spec)
    
    def __str__(self):
        return self.unitise()
    
    def __repr__(self):
        return self.__str__()

    def _get_quantity(self, quantity, value, spec, vector):
        if settings['always_make_quantities']:
            return Quantity(value, spec, vector)
        else:
            return value

    def __mul__(self, other):
        quantity = isinstance(other, Quantity)
        if quantity:
            return self._mul(other)
        return self._get_quantity(quantity, self.value * other, spec=self.spec,
                        vector=self.vector)

    def __pow__(self, other, modulo=None):
        if not isinstance(other, int):
            raise ValueError('Can only raise units to integer powers.')
        return self._pow(other)
    
    def __truediv__(self, other):
        quantity = isinstance(other, Quantity)
        if quantity:
            return self._div(other)
        return self._get_quantity(quantity, self.value / other, spec=self.spec,
                        vector=self.vector)

    def __rmul__(self, other):
        quantity = isinstance(other, Quantity)
        if quantity:
            return self._mul(other)
        return self._get_quantity(quantity, self.value * other, spec=self.spec,
                        vector=self.vector)


    def __rtruediv__(self, other):
        quantity = isinstance(other, Quantity)
        if quantity:
            return self._div(other)
        return self._get_quantity(quantity, other / self.value,
                        spec=[-u for u in self.spec],
                        vector=-self.vector)
    
    def _mul(self, other):
        spec = self.spec.copy()
        spec.extend(other.spec)
        vector = self.vector + other.vector
        return Quantity(self.value * other.value, spec=spec,
                        vector=vector)

    def _div(self, other):
        spec = self.spec.copy()
        spec.extend([-u for u in other.spec])
        vector = self.vector - other.vector
        return Quantity(self.value / other.value, spec=spec,
                        vector=vector)


    def _pow(self, other):
        new = self
        for n in range(other - 1):
            new = new._mul(self)
        return new
            
    def __rlshift__(self, other):
        quantity = isinstance(other, Quantity)
        if quantity:
            return self._mul(other)
        return Quantity(self.value * other, spec=self.spec,
                        vector=self.vector)
    
    def __rrshift__(self, other):
        return other / self.value
    
    def __array__(self):
        ''' For numpy 
        
        See:
            https://numpy.org/devdocs/user/basics.dispatch.html
        '''
        return np.array(self.value)
    
    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        ''' For numpy 
        
        See:
            https://numpy.org/devdocs/user/basics.dispatch.html
        '''
        if method == '__call__':
            if isinstance(inputs[0], Quantity):
                v1 = inputs[0].value
            else:
                v1 = inputs[0]
            if isinstance(inputs[1], Quantity):
                v2 = inputs[1].value
            else:
                v2 = inputs[1]
            return Quantity(v1 * v2, spec=self.spec,
                        vector=self.vector)
        else:
            return NotImplemented
    


