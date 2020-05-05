# -*- coding: utf-8 -*-
"""
Created on Fri May  1 11:52:26 2020

@author: Reuben
"""

from . import settings, get_active, get_units, get_systems
import numpy as np

class Quantity():
    def __init__(self, value, spec, vector, abbr=None, name=None):
        self.value = value
        self.spec = spec
        self.vector = vector
        self.abbr = abbr
        self.name = name
        self._parent = get_active()
        
    def set_unit(self, unit):
        if any(unit.vector != self.vector):
            raise ValueError('Incompatible quantity type')
        self.spec = unit.spec
        self.value = self.value * unit.value
        self.abbr = unit.abbr if unit.abbr is not None else None
        self.name = unit.name if unit.name is not None else None
                
    def _in_units(self, unit=None):
        if unit is not None:
            if unit.vector != self.vector:
                raise ValueError('Incompatible quantity type')
            spec = unit.spec
            value = self.value * unit.value
        else:
            spec = self.spec
            value = self.value
        value = get_systems(self._parent).unitise_typed(value, spec)
        return value, spec

    def in_units(self, unit=None):
        return self._to_str(*self._in_units(unit))

    def _unitise(self):
        return get_systems(self._parent).unitise(self.value, self.spec)

    def unitise(self):
        return self._to_str(*self._unitise())

    def _base_unitise(self):
        return get_systems(self._parent).base_unitise(self.value, self.vector)
    
    def base_unitise(self):
        return self._to_str(*self._base_unitise())
    
    def _to_str(self, value, spec):
        if isinstance(value, np.ndarray):
            f = str(value)
        else:
            f = '{:0.6g}'.format(value)
        return f + ' ' + get_units(self._parent).str_spec(spec)
    
    def __str__(self):
        return self.unitise()
    
    def __repr__(self):
        return self.__str__()

    def _get_quantity(self, quantity, value, spec, vector):
        if settings['always_make_quantities']:
            return Quantity(value=value, spec=spec, vector=vector)
        else:
            return value

    def __add__(self, other):
        quantity = isinstance(other, Quantity)
        if not quantity:
            raise NotImplementedError('Quantity instances can only be added '
                                      + 'to Quantity instances.')
        if quantity:
            if any(other.vector != self.vector):
                raise ValueError('Incompatible units.')
        return Quantity(self.value + other.value, spec=self.spec,
                        vector=self.vector)

    def __sub__(self, other):
        quantity = isinstance(other, Quantity)
        if not quantity:
            raise NotImplementedError('Quantity instances can only be added '
                                      + 'to Quantity instances.')
        if quantity:
            if any(other.vector != self.vector):
                raise ValueError('Incompatible units.')
        return Quantity(self.value - other.value, spec=self.spec,
                        vector=self.vector)

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

    def __rpow__(self, other, modulo=None):
        if isinstance(other, Quantity):
            raise ValueError('Units cannot be raised to the power of other '
                             + 'units.')
        return self._get_quantity(False, other**self.value, spec=self.spec,
                        vector=self.vector)
    
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
        return Quantity(value=self.value / other.value, spec=spec,
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
        return Quantity(value=self.value * other, spec=self.spec,
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
        ufunc_name = ufunc.__name__
        if method != '__call__':
            return NotImplemented
        quantity = isinstance(inputs[0], Quantity)
        if ufunc_name=='multiply':
            value = inputs[0] * inputs[1].value
            return self._get_quantity(quantity, value,
                                      spec=self.spec, vector=self.vector)

        elif ufunc_name=='true_divide':
            value = inputs[0] / inputs[1].value
            return self._get_quantity(quantity, value,
                                      spec=self.spec, vector=self.vector)
        elif ufunc_name=='left_shift':
            return Quantity(value=inputs[0] * inputs[1].value, spec=self.spec,
                        vector=self.vector)
        elif ufunc_name=='right_shift':
            return inputs[0] * inputs[1].value
        return NotImplemented
            
    


