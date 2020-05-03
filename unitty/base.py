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
    
    def new(self, abbr, value, unit_vec, unit_type, name, base_type):
        if abbr in self.units:
            raise KeyError(abbr + ' is already defined.')
        else:
            u = Unit(abbr, value, unit_vec, unit_type, name, base_type)
        self.safe_set(self.units, abbr, u)
        
        # Now make the corresponding inverse ('negative') unit
        if unit_type is not None:
            ut = ['-' + ut for ut in unit_type]
            bt = ['-' + bt for bt in base_type]
        else:
            ut = None
            bt = base_type
        uneg = Unit(abbr, 1/value, -unit_vec, ut, name, bt)
        self.safe_set(self.units, '-' + abbr, uneg)
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
        self.units = {}
        self.bases = {}
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
        
    def _derive(self, unit_type):
        us = [self[u] for u in unit_type]
        unit_vec = np.sum([u.unit_vec for u in us], axis=0)
        value = np.prod([u.value for u in us])
        return value, unit_vec
        
    def _make_unit(self, units, unit_type, abbr, v):
        value, derivation, name = v
        if not isinstance(derivation, list):
            derivation = [derivation]
        m, unit_vec = self._derive(derivation)
        self.new(abbr, value * m, unit_vec, [abbr], name, [unit_type])
    
    def _make_type_dct(self, dct):
        units = self.units
        for unit_type, d in dct.items():
            if isinstance(d, list):
                self._make_base_types(d)
                continue
            for abbr, v in d.items():
                if abbr == '_base':
                    base_abbr = v
                    self.bases[unit_type] = base_abbr
                else:
                    self._make_unit(units, unit_type, abbr, v)

    def __getitem__(self, abbr):
        if abbr in self.units:
            return self.units[abbr]
        raise KeyError(abbr + ' not defined')

    def __getattr__(self, abbr):
        if abbr not in ['units', 'bases'] and abbr in self.units:
            return self.units[abbr]
        else:
            return self.__getattribute__(abbr)
    
    

units = Units()


        
    