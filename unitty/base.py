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
    def __init__(self, fname=None):
        self.load(fname)
    
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
        
    def _add_base_type(self, i, base_type):
        self._add_base_type[i] = base_type
    
    def new(self, abbr, value, vector, spec, name, base_type):
        if abbr in self.units:
            raise KeyError(abbr + ' is already defined.')
        spec = [self._ind(u) for u in spec]
        index = self._ind(abbr)
        index_base = [self._ind(b) for b in base_type]
        self._base_types[index] = index_base
        u = Unit(abbr, value, vector, spec, name)
        self.safe_set(self.units, abbr, u)
        # Now make the corresponding inverse ('negative') unit
        ut = [-u for u in spec]
        uneg = Unit(abbr, 1/value, -vector, ut, name)
        self.safe_set(self.units, '-' + abbr, uneg)
        index = self._ind('-' + abbr)
        self._base_types[index] = [-b for b in index_base]
        return u
    
    def _make_base_types(self, types):
        self.base_types = types
        def vec(ind):
            a = np.zeros(len(types))
            a[ind] = 1
            return a
        for i, t in enumerate(types):
            self.new(t, 1.0, vec(i), [t], t, [t])
    
    def load(self, fname=None):
        self.units = {} # The unit instances
        self.bases = {} # The base units for time, length, etc
        self._base_types = {} # the length, time for given id
        self._num_dct = {} # The attr for given index
        self._ind_dct = {} # the index for given attr
        raw = self._load_raw(fname)
        self._make_type_dct(raw)
    
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
        
    def _make_unit(self, units, spec, abbr, v):
        value, derivation, name = v
        if not isinstance(derivation, list):
            derivation = [derivation]
        m, vector = self._derive(derivation)
        self.new(abbr, value * m, vector, [abbr], name, [spec])
    
    def _make_type_dct(self, dct):
        units = self.units
        for spec, d in dct.items():
            if isinstance(d, list):
                self._make_base_types(d)
                continue
            for abbr, v in d.items():
                if abbr == '_base':
                    base_abbr = v
                    self.bases[self._ind(spec)] = self._ind(base_abbr)
                else:
                    self._make_unit(units, spec, abbr, v)

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


        
    