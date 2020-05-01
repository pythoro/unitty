# -*- coding: utf-8 -*-
"""
Created on Fri May  1 11:20:07 2020

@author: Reuben
"""

import os
import ruamel.yaml as yaml

from .base import base

root = os.path.dirname(os.path.abspath(__file__))


class Systems():
    def __init__(self, fname=None):
        self.load(fname)
    
    def load(self, fname=None):
        raw = self._load_raw(fname)
        self._sys_dct = self._make_sys_dct(raw)
        for name in self._sys_dct.keys():
            self._active = name
            break

    def _load_raw(self, fname=None):
        if fname is None:
            fname = os.path.join(root, 'systems') + '.yaml'
        with open(fname, 'r') as f:
            raw = yaml.safe_load(f)
        return raw
    
    def _make_sys_dct(self, raw):
        return {n: System(dct) for n, dct in raw.items()}
    
    def set_system(self, name):
        self._active = name
    
    @property
    def active(self):
        return self._sys_dct[self._active]
        
    def unitise(self, val, unit_type):
        return self._sys_dct[self._active].unitise(val, unit_type)


class System():
    def __init__(self, dct):
        self._sys_dct = self._make_sys_dct(dct)
    
    def _make_sys_dct(self, dct):
        d = {}
        for unit_type, units_raw in dct.items():
            mults = []
            units = []
            for abbr in units_raw:
                if isinstance(abbr, list):
                    unit = base[abbr[1]]
                    mults.append(abbr[0] * unit.value)
                    units.append(abbr[1])
                else:
                    unit = base[abbr]
                    mults.append(unit.value)
                    units.append(abbr)
            mults.reverse()
            units.reverse()
            d[unit_type] = {'units': units, 'mults': mults}
        return d
    
    def unitise(self, val, unit_type):
        if unit_type is None:
            return val, None
        try:
            d = self._sys_dct[unit_type]
        except KeyError:
            raise KeyError('unit type "' + unit_type + '" not recognised.')
        for (unit, mult) in zip(d['units'], d['mults']):
            if val >= mult:
                break
        return val / mult, unit


systems = Systems()        
active = systems.active
set_system = systems.set_system

