# -*- coding: utf-8 -*-
"""
Created on Fri May  1 11:20:07 2020

@author: Reuben
"""

import os
import ruamel.yaml as yaml

from . import base

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
        
    def unitise(self, val, base_type):
        return self._sys_dct[self._active].unitise(val, base_type)

    def base_unitise(self, val, type_vec):
        return self._sys_dct[self._active].base_unitise(val, type_vec)

    def unitise_typed(self, val, unit_type):
        return self._sys_dct[self._active].unitise_typed(val, unit_type)


class System():
    def __init__(self, dct):
        self._sys_dct = self._make_sys_dct(dct)
    
    def _make_sys_dct(self, dct):
        d = {}
        for unit_type, units_raw in dct.items():
            unit_dct = {}
            units_raw.reverse()
            for abbr in units_raw:
                if isinstance(abbr, list):
                    unit = base.units[abbr[1]]
                    mult = abbr[0] * unit.value
                    a = unit.abbr
                else:
                    unit = base.units[abbr]
                    mult = unit.value
                    a = abbr
                unit_dct[a] = mult
            d[unit_type] = unit_dct
        return d
    
    def calc_base_unit_type(self, unit_vec):
        unit_type = []
        for n, name in zip(unit_vec, base.units.base_types):
            name = '-' + name if n < 0 else name
            unit_type.extend([name]*int(abs(n)))
        return unit_type

    def _unitise_one(self, val, unit_type):
        div = False
        if unit_type.startswith('-'):
            div = True
            unit_type = unit_type[1:]
        if unit_type not in self._sys_dct:
            return val, unit_type
        d = self._sys_dct[unit_type]
        for abbr, mult in d.items():
            if val >= mult:
                break
        if div:
            return val * mult, '-' + abbr
        return val / mult, abbr

    def _base_unitise_one(self, val, unit_type):
        div = False
        if unit_type.startswith('-'):
            div = True
            unit_type = unit_type[1:]
        b = base.units.bases[unit_type]
        u = base.units[b]
        a = u.abbr
        if div:
            return val * u.value, '-' + u.abbr
        return val / u.value, u.abbr
    
    def unitise(self, val, base_type):
        new_val = val
        unit_type = []
        for u in base_type:
            new_val, ut = self._unitise_one(new_val, u)
            unit_type.append(ut)
        return new_val, unit_type
    
    def base_unitise(self, val, unit_vec):
        base_unit_type = self.calc_base_unit_type(unit_vec)
        new_val = val
        unit_type = []
        for u in base_unit_type:
            new_val, ut = self._base_unitise_one(new_val, u)
            unit_type.append(ut)
        return new_val, unit_type
    
    def unitise_typed(self, val, unit_type):
        out = val
        for u in unit_type:
            div = False
            if u.startswith('-'):
                div = True
            if div:
                out /= base.units[u].value
            else:
                out *= base.units[u].value
        return out
    

systems = Systems()        
active = systems.active
set_system = systems.set_system

