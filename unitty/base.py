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
        self._type_dct, self.bases = self._make_type_dct(raw)
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
        bases = {}
        for unit_type, d in dct.items():
            if unit_type not in out:
                out[unit_type] = {}
            unit_dct = out[unit_type]
            for unit, v in d.items():
                if len(v) != 3:
                    raise ValueError('Unit ' + unit + ' incorrectly specified.')
                mult, base, name = v
                if unit == '_base':
                    dct_2 = {'mult': 1.0, 'name': name}
                    bases[unit_type] = base
                    self.safe_set(unit_dct, base, dct_2)
                else:
                    dct_2 = {'mult': unit_dct[base]['mult'] * mult,
                             'name': name}
                    self.safe_set(unit_dct, unit, dct_2)
        return out, bases
    
    def _make_unit_dct(self, type_dct):
        out = {}
        for unit_type, d in type_dct.items():
            for unit, d2 in d.items():
                dct = dict(d2)
                dct['unit_type'] = unit_type
                if unit != '_base':
                    self.safe_set(out, unit, dct)
        return out

    def __getitem__(self, abbr):
        return self._unit_dct[abbr]['mult']

    def __getattr__(self, abbr):
        if abbr != '_unit_dct' and abbr in self._unit_dct:
            return self._unit_dct[abbr]['mult']
        else:
            return self.__getattribute__(abbr)
        
    def mult(self, abbr):
        return self._unit_dct[abbr]['mult']
    
    def get_unit(self, abbr):
        d = self._unit_dct[abbr]
        return Unit(abbr, **d)
    
    def all_units(self):
        return Units({k: self.get_unit(k) for k in self._unit_dct.keys()})

base = Base()



        
    