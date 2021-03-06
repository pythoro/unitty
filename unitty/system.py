# -*- coding: utf-8 -*-
"""
Created on Fri May  1 11:20:07 2020

@author: Reuben

This module is responsible for the unit systems desired by the user. Quantities
all share the same underlying base dimensions. For example, a meter and a 
foot both share the underlying length dimension, although they represent 
different scaling factors.

A unit system indicates what kinds of units the user would like to use for
given types of dimensions. For example, in the length dimension, the metric
unit system would specify units like millimeter, meter, and kilometer. On the
other hand, the US imperial system would specify units such as inch, foot, 
and mile. 

Unitty allows unit systems to be switched on the fly. This is made possible
by the Systems class, which contains a number of System classes and keeps 
track of which one is currently active.

Normally, the user would not instantiate Systems or System objects directly,
but would use api functions.

"""

import os
import ruamel.yaml as yaml
import numpy as np
import pprint
from . import get_units, get_active

root = os.path.dirname(os.path.abspath(__file__))


class Systems():
    """ Manage multiple unit systems and allow switching between them
    
    Args:
        fname (str): [Optional] The yaml file from which to read in systems
            information. If omitted when raw is omitted, the defaults are
            loaded.
        raw (dict): [Optional] If passed when fname is omitted, this
            data is used to initialise the instance. See the :meth:`load`
            method for details on structure.
    
    """
    def __init__(self, fname=None, raw=None):
        self._refs = {}
        self._units = get_units(get_active())
        if fname is None and raw is None:
            fname = os.path.join(root, 'systems') + '.yaml'
        raw = self._load_raw(fname) if raw is None else raw
        self.load(raw)
    
    def load(self, raw):
        """ Load raw data 
        
        Args:
            raw (dict): A dictionary containing keys for all base dimensions
            specified in the current Units instance (e.g. length, time). See
            notes for details.
            
        Notes:
            The input must be a dictionary containing keys for all base
            dimensions specified in the current Units instance (e.g. length,
            time). The corresponding values must be lists of units to use
            for those dimensions. Unless otherwise directed (e.g. by
            named references), the unit that results in a value closest to 10
            will be used for a given dimension.
            
        Example:
            Here's a simple example::
                
                raw = {'metric':
                            {'length': ['mm', 'm'', 'km'],
                             'mass': ['g', 'kg', 'tonne']},
                       'US':
                            {'length': ['in', 'ft', 'mile'],
                             'mass': ['USoz', 'lbs']}}
            
        """
        self._sys_dct = self._make_sys_dct(raw)
        for name in self._sys_dct.keys():
            self._active = name
            break

    def _load_raw(self, fname):
        with open(fname, 'r') as f:
            raw = yaml.safe_load(f)
        return raw
    
    def _make_sys_dct(self, raw):
        return {n: System(dct) for n, dct in raw.items()}
    
    def set_active(self, name):
        """ Set the currently active system 
        
        Args:
            name (str): The system name. 
            
        """
        self._active = name
    
    @property
    def active(self):
        """ Return the active system
        
        Returns:
            System: The active system.
        """
        return self._sys_dct[self._active]
        
    def unitise(self, val, spec):
        """ Express a value in units specified by the active system.
        
        Args:
            val (float, arraylike): The value with respect to base dimensions
                like length, time, etc.
            spec (list[int]): A list of integers corresponding to the units
                in which val is defined. These are used to indicate 
                the dimensionality.
        
        Returns:
            tuple: A value and unit string tuple.
            
        Notes:
            The value and unit string returned will depend on which
            unit system is active. See the :mod:`system` module.
            
            The spec is used because it is sometimes more desirable to
            expressed a value in derived dimensions (e.g. force), rather 
            than base dimensions (for force, this would be a combination of
            length, time, and distance). 
        """
        return self._sys_dct[self._active].unitise(val, spec)

    def base_unitise(self, val, vector, dimensional=False):
        return self._sys_dct[self._active].base_unitise(val, vector,
                            dimensional)

    def unitise_typed(self, val, spec):
        return self._sys_dct[self._active].unitise_typed(val, spec)

    def set_refs(self, source):
        if isinstance(source, str):
            if source.endswith('.csv'):
                data = np.genfromtxt(source, delimiter=',', dtype='str')
                headers = data[0]
                body = data[1:]
                dct = {}
                for row in body:
                    dct[row[0]] = {k: v for k, v in zip(headers[1:], row[1:])}
        elif isinstance(source, dict):
            dct = source
        self._refs = dct
        
    def by_ref(self, val, ref):
        if ref not in self._refs:
            return None
        unit_str = self._refs[ref][self._active]
        u = self._units[unit_str]
        value = val / u.value
        return value, unit_str


class System():
    def __init__(self, dct):
        self._units = get_units(get_active())
        self._sys_dct = self._make_sys_dct(dct)
    
    def __str__(self):
        d = {self._units.str(k): [self._units.str(v) for v in val]
                        for k, val in self._sys_dct.items()}
        return pprint.pformat(d)
    
    def __repr__(self):
        return self.__str__()
    
    def _make_sys_dct(self, dct):
        d = {}
        for spec, units_raw in dct.items():
            unit_dct = {}
            for abbr in units_raw:
                if isinstance(abbr, list):
                    unit = self._units[abbr[1]]
                    mult = abbr[0] * unit.value
                    a = self._units._ind(unit.abbr)
                else:
                    unit = self._units[abbr]
                    mult = unit.value
                    a = self._units._ind(abbr)
                unit_dct[a] = mult
            d[self._units._ind(spec)] = unit_dct
        return d
    
    def calc_utypes(self, vector):
        utypes = []
        for n, name in zip(vector, self._units.utypes):
            i = self._units._ind(name)
            if n > 0:
                utypes.extend([i]*int(abs(n)))
            else:
                utypes.extend([-i]*int(abs(n)))
        return utypes

    def _unitise_one(self, val, utype):
        if abs(utype) not in self._sys_dct:
            return val, utype
        d = self._sys_dct[abs(utype)]
        div = utype < 0
        trials = []
        i_vals = []
        for i, mult in d.items():
            if div:
                trials.append(val * mult)
                i_vals.append(-i)
            else:
                trials.append(val / mult)
                i_vals.append(i)
        a = []
        for v in trials:
            num = np.mean(np.abs(np.atleast_1d(v)))
            den = np.mean(10/np.abs(np.atleast_1d(v)))
            a.append(np.max((num, den)))
        ind = a.index(min(a))
        return i_vals[ind]

    def _base_unitise_one(self, val, spec, dimensional=False):
        div = False
        if spec < 0:
            div = True
        utype_i = abs(self._units._utypes[spec]) # length, force, etc
        if not dimensional and utype_i in self._units.bases:
            b = self._units.bases[utype_i] # m, N etc
        else:
            b = utype_i
        u = self._units.get_by_index(b)
        if div:
            return val * u.value, -b
        return val / u.value, b
    
    def unitise(self, val, spec):
        new_val = val
        out_spec = []
        utypes = self._units._utypes
        utype = [utypes[s] for s in spec]
        for u, s in zip(utype, spec):
            ut = self._unitise_one(new_val, u)
            new_val = new_val / self._units.get_by_index(ut).value
            out_spec.append(ut)
        s = self._units.str_spec(out_spec)
        return new_val, s
    
    def base_unitise(self, val, vector, dimensional=False):
        base_spec = self.calc_utypes(vector)
        new_val = val
        spec = []
        for u in base_spec:
            new_val, ut = self._base_unitise_one(new_val, u, dimensional)
            spec.append(ut)
        s = self._units.str_spec(spec)
        return new_val, s
    
    def unitise_typed(self, val, spec):
        out = val
        for u in spec:
            out /= self._units.get_by_index(u).value
        s = self._units.str_spec(spec)
        return out, s
    
