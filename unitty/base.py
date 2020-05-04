# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 18:15:23 2020

@author: Reuben
"""

import os
import ruamel.yaml as yaml
import numpy as np

from .unit import Unit

root = os.path.dirname(os.path.abspath(__file__))



class Units():
    _autoload = True
    
    def __init__(self, fname=None):
        if self._autoload or fname is not None:
            raw = self._load_raw(fname)
            self.load(raw)
    
    def _ind(self, s):
        if s in self._ind_dct:
            return self._ind_dct[s]
        index = len(self._num_dct) + 1
        self._num_dct[index] = s
        self._ind_dct[s] = index
        self._num_dct[-index] = '-' + s
        self._ind_dct['-' + s] = -index
        return index
    
    def str(self, ind):
        return self._num_dct[ind]
            
    def _new(self, index, value, vector, spec, name, utype):
        abbr = self.str(index)
        if abbr in self.units:
            raise KeyError(abbr + ' is already defined.')
        self._utypes[index] = utype
        u = Unit(value=value, spec=spec, vector=vector, abbr=abbr, name=name)
        self.safe_set(self.units, abbr, u)
        return u
    
    def new(self, index, value, vector, spec, name, utype):
        u = self._new(index, value, vector, spec, name, utype)
        # Now make the corresponding inverse ('negative') unit
        spec = [-s for s in spec]
        self._new(-index, 1/value, -vector, spec, name, -utype)
        return u
    
    def _make_utypes(self, types):
        self.utypes = types
        def vec(ind):
            a = np.zeros(len(types))
            a[ind] = 1
            return a
        for i, t in enumerate(types):
            index = self._ind(t)
            self.new(index, 1.0, vec(i), [index], t, index)
    
    def _clear(self):
        self.units = {} # The unit instances
        self.bases = {} # The base units for time, length, etc
        self._utypes = {} # the length, time etc for given id
        self._num_dct = {} # The attr for given index
        self._ind_dct = {} # the index for given attr
        
    def load(self, dct):
        self._clear()
        self._make_type_dct(dct)
    
    def _load_raw(self, fname=None):
        if fname is None:
            fname = os.path.join(root, 'units') + '.yaml'
        with open(fname, 'r') as f:
            raw = yaml.safe_load(f)
        return raw
    
    def safe_set(self, unit_dct, key, val):
        if key in unit_dct:
            raise KeyError(key + ' already defined.')
        else:
            unit_dct[key] = val
        
    def _derive(self, spec):
        us = [self[u] for u in spec]
        vector = np.sum([u.vector for u in us], axis=0)
        value = np.prod([u.value for u in us])
        return value, vector
        
    def _make_unit(self, units, utype, index, v):
        value, derivation, name = v
        if not isinstance(derivation, list):
            derivation = [derivation]
        m, vector = self._derive(derivation)
        spec = [index]
        self.new(index, value * m, vector, spec, name, utype)
    
    def _make_type_dct(self, dct):
        units = self.units
        for utype_str, d in dct.items():
            utype = self._ind(utype_str)
            if isinstance(d, list):
                self._make_utypes(d)
                continue
            for abbr_str, v in d.items():
                if abbr_str == '_base':
                    # Set the base for the utype
                    self.bases[utype] = self._ind(v)
                else:
                    index = self._ind(abbr_str)
                    self._make_unit(units, utype, index, v)

    def __getitem__(self, abbr):
        if abbr in self.units:
            return self.units[abbr]
        raise KeyError(str(abbr) + ' not defined')

    def __getattr__(self, abbr):
        if abbr not in ['units', 'bases'] and abbr in self.units:
            return self.units[abbr]
        else:
            return self.__getattribute__(abbr)
    
    def get_by_index(self, i):
        return self.units[self._num_dct[i]]
    
    def str_spec(self, spec):
        if spec is None:
            return 'base'
        elif len(spec)==0:
            return 'dimensionless'
        num = [i for i in spec if i > 0]
        den = [-i for i in spec if i < 0]
        def f(v, c):
            if c == 1:
                return v
            else:
                return v + str(c)
        def process(lst):
            out = [units._num_dct[i] for i in lst]    
            out.sort()
            d = {v: out.count(v) for v in out}
            return [f(v, c) for v, c in d.items()]
        num = process(num)
        den = process(den)
        s_num = '1' if len(num) == 0 else '.'.join(num)
        n = len(den)
        if n == 0:
            return s_num
        elif n == 1:
            return s_num + '/' + den[0]
        else:
            return s_num + '/(' + '.'.join(den) + ')'

units = Units()


        
    