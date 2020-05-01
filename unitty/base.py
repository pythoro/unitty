# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 18:15:23 2020

@author: Reuben
"""

import os
import ruamel.yaml as yaml

from .unit import Unit_Factory, Units, Unit

root = os.path.dirname(os.path.abspath(__file__))


class Base():
    def __init__(self, fname=None):
        self.units = {}
        self.bases = {}
        self.load(fname)
    
    def load(self, fname=None):
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
        
    def _derive_m(self, units, dct):
        num = 1.0
        den = 1.0
        if 'num' in dct:
            for unit in dct['num']:
                u = units[unit]
                num *= u.mult
        if 'den' in dct:
            for unit in dct['den']:
                u = units[unit]
                den *= u.mult
        return num/den
    
    def make_type_spec(self, type_num, type_den):
        if len(type_num) == 0:
            num = '1'
        else:
            num = ' * '.join(type_num)
        if len(type_den) == 0:
            return num
        elif len(type_den) == 1:
            den = ' * '.join(type_den)
        else:
            den = '(' + ' * '.join(type_den) + ')'            
        return num + ' / ' + den
    
    def _make_unit(self, units, unit_type, abbr, v):
        if len(v) != 3:
            raise ValueError('Unit ' + abbr + ' incorrectly specified.')
        mult, base, name = v
        if isinstance(base, dict):
            m = self._derive_m(units, base)
        elif isinstance(base, str):
            u_base = self.units[base]
            m = u_base.mult
            assert u_base.unit_type == unit_type
        elif isinstance(base, (int, float)):
            m = base
        u = Unit(abbr, mult * m, unit_type, name)
        self.safe_set(units, abbr, u)
    
    def _make_type_dct(self, dct):
        units = self.units
        for unit_type, d in dct.items():
            for abbr, v in d.items():
                if abbr == '_base':
                    base_abbr = v[0]
                    self.bases[unit_type] = base_abbr
                    v[0] = 1.0
                    self._make_unit(units, unit_type, base_abbr, v)
                else:
                    self._make_unit(units, unit_type, abbr, v)

    def __getitem__(self, abbr):
        return self.units[abbr]

    def __getattr__(self, abbr):
        if abbr not in ['units', 'bases'] and abbr in self.units:
            return self.units[abbr]
        else:
            return self.__getattribute__(abbr)
    
    

base = Base()
units = base


        
    