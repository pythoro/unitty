# -*- coding: utf-8 -*-
"""
Created on Fri May  1 11:52:26 2020

@author: Reuben

The Quantity class combines a magnitude with dimensional information that gives
that magnitude meaning. Quantity objects wrap a value with information about
the dimensions. The value can be a scalar or array.

Quantities are always expressed in terms of other quantities, with the 
exception of *base dimensions* like length, time, mass, etc. `unitty` imposes
no restrictions on what these base dimensions are. They may also include
derived base dimensions, such as force or pressure. Quantities defined
by derived base dimensions will understand the underlying dimensionality 
that defines them, but also their preferred expression of
force, pressure, etc.

"""

from . import settings, get_active, get_units, get_systems
import numpy as np

from collections import namedtuple

Quantity_Tuple = namedtuple('Quantity_Tuple', ['value', 'units'])

class Quantity():
    """ The core object that combines magnitude and dimensional information.
    
    Args:
        value (int, float, arraylike) : A float representing the magnitude of
            the quantity in terms of base dimensions (length, time, mass, etc)
            spec: A list of signed integers. For simple units, there will be
            only one integer. For compound units (e.g. m/s), there will be
            more than one. The integers correspond to other Quantities.
            Positive integers indicate the are multiplied, while negative
            integers indicate they are divided.
        vector (ndarray): Each base dimensions is independent, and the exponent
            for each base dimension is represented as a number. This vectore is
            an array of such numbers for all base dimensions. This allows quick
            and robust dimensionality checking.
        abbr (str): [optional] The abbreviation of the Quantity (usually
                 for Units)
        name (str): [optional] The name of the Quantity (usually for Units)
        parent (str): [optional] The name of the Units instance it belongs to.
            This is important, since otherwise the spec doesn't make any sense.
        
    Note:
        Normally, Quantities would only be created automatically or from
        other Quantities, not directly by the user.
        
"""
    
    def __init__(self, value, spec, vector, abbr=None, name=None,
                 parent=None):
        self.value = value
        self.spec = spec
        self.vector = vector
        self.abbr = abbr
        self.name = name
        self._parent = get_active() if parent is None else parent
        self._ref = None
        
    def set_units(self, unit):
        """ Set the units for this quantity 
        
        Args:
            unit (Quantity): A Quantity or Unit instance.
        """
        if any(unit.vector != self.vector):
            raise ValueError('Incompatible quantity type')
        self.spec = unit.spec
        self.abbr = unit.abbr if unit.abbr is not None else None
        self.name = unit.name if unit.name is not None else None
                
    def set_ref(self, ref):
        """ Set the reference name for this quantity 
        
        Args:
            ref (str): The reference name
        """
        self._ref = ref
        
    def in_units(self, unit=None):
        """ Express the Quantity in particular units 
        
        Args:
            unit (Unit): [Optional] The units to express this Quantity in. If
                omitted, the Quantity will be expressed in the units in which
                it was defined.
        
        Returns:
            Quantity_Tuple: A value and unit string tuple.
        """
        if unit is not None:
            if any(unit.vector != self.vector):
                raise ValueError('Incompatible quantity type')
            spec = unit.spec
        else:
            spec = self.spec
        tup = get_systems(self._parent).unitise_typed(self.value, spec)
        return Quantity_Tuple(*tup)

    def str_in_units(self, unit=None):
        """ Format the result from :meth:`in_units` into string 
        
        Args:
            unit (Unit): [Optional] The units to express this Quantity in. If
                omitted, the Quantity will be expressed in the units in which
                it was defined.
        
        Returns:
            str: A string showing the value and units of the Quantity.
            
        """
        return self._to_str(*self.in_units(unit))

    def by_ref(self):
        """ Express the Quantity in units specified by a reference name
                
        Returns:
            Quantity_Tuple: A value and unit string tuple.
            
        Note:
            The value and unit string returned will depend on which
            unit system is active. Named references must specify units
            for the active system (See :meth:`system.Systems.set_refs`).
        """
        tup = get_systems(self._parent).by_ref(self.value, self._ref)
        return Quantity_Tuple(*tup)

    def in_sys(self):
        """ Express the Quantity in units specified by the active system.
        
        Returns:
            Quantity_Tuple: A value and unit string tuple.
            
        Note:
            The value and unit string returned will depend on which
            unit system is active. See the :mod:`system` module.
        """
        if self._ref is not None:
            tup = get_systems(self._parent).by_ref(self.value, self._ref)
        if self._ref is None or tup is None:
            tup = get_systems(self._parent).unitise(self.value, self.spec)
        return Quantity_Tuple(*tup)

    def str_in_sys(self):
        """ Format the result from :meth:`in_sys` into string 
        
        Returns:
            str: A string showing the value and units of the Quantity.
            
        """
        return self._to_str(*self.in_sys())

    def in_base(self, dimensional=False):
        """ Express the Quantity in base units.
        
        Returns:
            Quantity_Tuple: A value and unit string tuple.
            
        Note:
            The value and unit string returned will *not* depend on which
            unit system is active.
        """
        tup = get_systems(self._parent).base_unitise(self.value, self.vector,
                         dimensional)
        return Quantity_Tuple(*tup)

    def str_in_base(self, dimensional=False):
        """ Format the result from :meth:`in_base` into string 
        
        Returns:
            str: A string showing the value and units of the Quantity.
            
        """
        return self._to_str(*self.in_base(dimensional))
    
    def in_dimensions(self):
        return self.in_base(dimensional=True)

    def str_in_dimensions(self):
        return self.str_in_base(dimensional=True)
    
    def _to_str(self, value, spec):
        if isinstance(value, np.ndarray):
            f = str(value)
        else:
            f = '{:0.6g}'.format(value)
        return f + ' ' + spec
    
    def __str__(self):
        return self.str_in_sys()
    
    def __repr__(self):
        return self.str_in_sys()

    def _get_quantity(self, quantity, value, spec, vector):
        if settings['always_make_quantities']:
            return Quantity(value=value, spec=spec, vector=vector,
                            parent=self._parent)
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
                        vector=self.vector, parent=self._parent)

    def __sub__(self, other):
        quantity = isinstance(other, Quantity)
        if not quantity:
            raise NotImplementedError('Quantity instances can only be added '
                                      + 'to Quantity instances.')
        if quantity:
            if any(other.vector != self.vector):
                raise ValueError('Incompatible units.')
        return Quantity(self.value - other.value, spec=self.spec,
                        vector=self.vector, parent=self._parent)

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
                        vector=vector, parent=self._parent)

    def _div(self, other):
        spec = self.spec.copy()
        spec.extend([-u for u in other.spec])
        vector = self.vector - other.vector
        return Quantity(value=self.value / other.value, spec=spec,
                        vector=vector, parent=self._parent)

    def _pow(self, other):
        new = self
        if other % 1 != 0:
            raise ValueError('Units can only be raised to integer powers.')
        for n in range(other - 1):
            new = new._mul(self)
        return new
            
    def __rlshift__(self, other):
        quantity = isinstance(other, Quantity)
        if quantity:
            return self._mul(other)
        return Quantity(value=self.value * other, spec=self.spec,
                        vector=self.vector, parent=self._parent)
    
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
                        vector=self.vector, parent=self._parent)
        elif ufunc_name=='right_shift':
            return inputs[0] * inputs[1].value
        return NotImplemented
            
    


