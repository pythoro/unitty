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
                    a = base.units._ind(unit.abbr)
                else:
                    unit = base.units[abbr]
                    mult = unit.value
                    a = base.units._ind(abbr)
                unit_dct[a] = mult
            d[base.units._ind(unit_type)] = unit_dct
        return d
    
    def calc_base_unit_type(self, unit_vec):
        unit_type = []
        for n, name in zip(unit_vec, base.units.base_types):
            i = base.units._ind(name)
            if n > 0:
                unit_type.extend([i]*int(abs(n)))
            else:
                unit_type.extend([-i]*int(abs(n)))
        return unit_type

    def _unitise_one(self, val, unit_type, div=False):
        if abs(unit_type) not in self._sys_dct:
            return val, unit_type
        d = self._sys_dct[abs(unit_type)]
        for i, mult in d.items():
            if not div and (val/mult > 1e-2 and val/mult < 1e2):
                break
            if div and (val*mult > 1e-2 and val*mult < 1e2):
                break
        if div:
            return val * mult, -i
        return val / mult, i

    def _base_unitise_one(self, val, unit_type):
        div = False
        if unit_type < 0:
            div = True
        base_type_i = abs(base.units._base_types[unit_type][0]) # length, force, etc
        if base_type_i in base.units.bases:
            b = base.units.bases[base_type_i] # m, N etc
        else:
            b = base_type_i
        u = base.units.get_by_index(b)
        if div:
            return val * u.value, -b
        return val / u.value, b
    
    def unitise(self, val, unit_type):
        new_val = val
        out_unit_type = []
        base_types = base.units._base_types
        base_type = [t for bt in unit_type for t in base_types[bt]]
        num = [u for u in base_type if u > 0]
        den = [u for u in base_type if u < 0]
        for u in num:
            new_val, ut = self._unitise_one(new_val, u)
            out_unit_type.append(ut)
        for u in den:
            new_val, ut = self._unitise_one(new_val, u, div=True)
            out_unit_type.append(ut)
        return new_val, out_unit_type
    
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
            out /= base.units.get_by_index(u).value
        return out
    

systems = Systems()        
active = systems.active
set_system = systems.set_system

