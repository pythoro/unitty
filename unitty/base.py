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


LENGTH = 0
TIME = 1
TEMPERATURE = 2
MASS = 3
CURRENT = 4
SUBSTANCE = 5
LUMINOSITY = 6
MONEY = 7


class Units():
    def __init__(self, fname=None):
        self.load(fname)
    
    def new(self, abbr, value, unit_vec, unit_type, name):
        if abbr in self.units:
            raise KeyError(abbr + ' is already defined.')
        else:
            u = Unit(abbr, value, unit_vec, unit_type, name)
        self.safe_set(self.units, abbr, u)
        
        # Now make the corresponding inverse ('negative') unit
        if unit_type is not None:
            ut = ['-' + ut for ut in unit_type]
        else:
            ut = None
        uneg = Unit(abbr, 1/value, -unit_vec, ut, name)
        self.safe_set(self.units, '-' + abbr, uneg)
        return u
    
    def _make_bases(self):
        def vec(ind):
            a = np.zeros(8)
            a[ind] = 1
            return a
        self.new('length', 1.0, vec(LENGTH), None, 'length')
        self.new('time', 1.0, vec(TIME), None, 'time')
        self.new('temperature', 1.0, vec(TEMPERATURE), None, 'temperature')
        self.new('mass', 1.0, vec(MASS), None, 'mass')
        self.new('current', 1.0, vec(CURRENT), None, 'current')
        self.new('substance', 1.0, vec(SUBSTANCE), None, 'substance')
        self.new('luminosity', 1.0, vec(LUMINOSITY), None, 'luminosity')
        self.new('money', 1.0, vec(MONEY), None, 'money')
    
    def load(self, fname=None):
        self.units = {}
        self.bases = {}
        self._make_bases()
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
        self.new(abbr, value * m, unit_vec, derivation, name)
    
    def _make_type_dct(self, dct):
        units = self.units
        for unit_type, d in dct.items():
            for abbr, v in d.items():
                print(abbr)
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


        
    