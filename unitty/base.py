# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 18:15:23 2020

@author: Reuben
"""

import os
import ruamel.yaml as yaml

from .unit import Unit, Units

root = os.path.dirname(os.path.abspath(__file__))


class Base():
    def __init__(self, fname=None):
        self.load(fname)
    
    def load(self, fname=None):
        raw = self._load_raw(fname)
        self._type_dct = self._make_type_dct(raw)
        self._unit_dct = self._make_unit_dct(self._type_dct)
    
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
    
    def _make_type_dct(self, dct):
        out = {}
        for unit_type, d in dct.items():
            if unit_type not in out:
                out[unit_type] = {}
            unit_dct = out[unit_type]
            for unit, v in d.items():
                if unit == '_base':
                    self.safe_set(unit_dct, v, 1.0)
                if isinstance(v, list):
                    mult, base = v
                    self.safe_set(unit_dct, unit, unit_dct[base] * mult)
                else:
                    self.safe_set(unit_dct, unit, v)
        return out
    
    def _make_unit_dct(self, type_dct):
        out = {}
        for unit_type, d in type_dct.items():
            for unit, v in d.items():
                if unit != '_base':
                    self.safe_set(out, unit, {'mult': v, 'unit_type': unit_type})
        return out

    def __getitem__(self, key):
        return self._unit_dct[key]['mult']

    def __getattr__(self, key):
        if key != '_unit_dct' and key in self._unit_dct:
            return self._unit_dct[key]['mult']
        else:
            return self.__getattribute__(key)
        
    def mult(self, key):
        return self._unit_dct[key]['mult']
    
    def get_unit(self, key):
        d = self._unit_dct[key]
        return Unit(key, d['mult'], d['unit_type'])
    
    def all_units(self):
        return Units({k: self.get_unit(k) for k in self._unit_dct.keys()})

base = Base()



        
    