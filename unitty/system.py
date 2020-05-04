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

    def unitise_typed(self, val, spec):
        return self._sys_dct[self._active].unitise_typed(val, spec)


class System():
    def __init__(self, dct):
        self._sys_dct = self._make_sys_dct(dct)
    
    def _make_sys_dct(self, dct):
        d = {}
        for spec, units_raw in dct.items():
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
            d[base.units._ind(spec)] = unit_dct
        return d
    
    def calc_base_spec(self, vector):
        spec = []
        for n, name in zip(vector, base.units.base_types):
            i = base.units._ind(name)
            if n > 0:
                spec.extend([i]*int(abs(n)))
            else:
                spec.extend([-i]*int(abs(n)))
        return spec

    def _unitise_one(self, val, spec):
        if abs(spec) not in self._sys_dct:
            return val, spec
        d = self._sys_dct[abs(spec)]
        div = spec < 0
        trials = []
        i_vals = []
        for i, mult in d.items():
            if div:
                trials.append(val * mult)
                i_vals.append(-i)
            else:
                trials.append(val / mult)
                i_vals.append(i)
        a = [max(abs(v), 1/abs(v)) for v in trials]
        ind = a.index(min(a))
        return trials[ind], i_vals[ind]

    def _base_unitise_one(self, val, spec):
        div = False
        if spec < 0:
            div = True
        base_type_i = abs(base.units._base_types[spec][0]) # length, force, etc
        if base_type_i in base.units.bases:
            b = base.units.bases[base_type_i] # m, N etc
        else:
            b = base_type_i
        u = base.units.get_by_index(b)
        if div:
            return val * u.value, -b
        return val / u.value, b
    
    def unitise(self, val, spec):
        new_val = val
        out_spec = []
        base_types = base.units._base_types
        base_type = [t for bt in spec for t in base_types[bt]]
        for u in base_type:
            new_val, ut = self._unitise_one(new_val, u)
            out_spec.append(ut)
        return new_val, out_spec
    
    def base_unitise(self, val, vector):
        base_spec = self.calc_base_spec(vector)
        new_val = val
        spec = []
        for u in base_spec:
            new_val, ut = self._base_unitise_one(new_val, u)
            spec.append(ut)
        return new_val, spec
    
    def unitise_typed(self, val, spec):
        out = val
        for u in spec:
            out /= base.units.get_by_index(u).value
        return out
    

systems = Systems()        
active = systems.active
set_system = systems.set_system

