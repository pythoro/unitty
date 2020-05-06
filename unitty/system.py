# -*- coding: utf-8 -*-
"""
Created on Fri May  1 11:20:07 2020

@author: Reuben
"""

import os
import ruamel.yaml as yaml
import numpy as np
import pprint
from . import get_units, get_active

root = os.path.dirname(os.path.abspath(__file__))


class Systems():
    def __init__(self, fname=None, raw=None):
        self._qids = {}
        self._units = get_units(get_active())
        if fname is None and raw is None:
            fname = os.path.join(root, 'systems') + '.yaml'
        raw = self._load_raw(fname) if raw is None else raw
        self.load(raw)
    
    def load(self, raw):
        self._sys_dct = self._make_sys_dct(raw)
        for name in self._sys_dct.keys():
            self._active = name
            break

    def _load_raw(self, fname):
        with open(fname, 'r') as f:
            raw = yaml.safe_load(f)
        return raw
    
    def _make_sys_dct(self, raw):
        return {n: System(dct) for n, dct in raw.items()}
    
    def set_active(self, name):
        self._active = name
    
    @property
    def active(self):
        return self._sys_dct[self._active]
        
    def unitise(self, val, utype):
        return self._sys_dct[self._active].unitise(val, utype)

    def base_unitise(self, val, type_vec):
        return self._sys_dct[self._active].base_unitise(val, type_vec)

    def unitise_typed(self, val, spec):
        return self._sys_dct[self._active].unitise_typed(val, spec)

    def set_qids(self, source):
        if isinstance(source, str):
            if source.endswith('.csv'):
                data = np.genfromtxt(source, delimiter=',', dtype='str')
                headers = data[0]
                body = data[1:]
                dct = {}
                for row in body:
                    dct[row[0]] = {k: v for k, v in zip(headers[1:], row[1:])}
        elif isinstance(source, dict):
            dct = source
        self._qids = dct
        
    def by_qid(self, val, qid):
        unit_str = self._qids[qid][self._active]
        u = self._units[unit_str]
        value = val / u.value
        return value, unit_str


class System():
    def __init__(self, dct):
        self._units = get_units(get_active())
        self._sys_dct = self._make_sys_dct(dct)
    
    def __str__(self):
        d = {self._units.str(k): [self._units.str(v) for v in val]
                        for k, val in self._sys_dct.items()}
        return pprint.pformat(d)
    
    def __repr__(self):
        return self.__str__()
    
    def _make_sys_dct(self, dct):
        d = {}
        for spec, units_raw in dct.items():
            unit_dct = {}
            for abbr in units_raw:
                if isinstance(abbr, list):
                    unit = self._units[abbr[1]]
                    mult = abbr[0] * unit.value
                    a = self._units._ind(unit.abbr)
                else:
                    unit = self._units[abbr]
                    mult = unit.value
                    a = self._units._ind(abbr)
                unit_dct[a] = mult
            d[self._units._ind(spec)] = unit_dct
        return d
    
    def calc_utypes(self, vector):
        utypes = []
        for n, name in zip(vector, self._units.utypes):
            i = self._units._ind(name)
            if n > 0:
                utypes.extend([i]*int(abs(n)))
            else:
                utypes.extend([-i]*int(abs(n)))
        return utypes

    def _unitise_one(self, val, utype):
        if abs(utype) not in self._sys_dct:
            return val, utype
        d = self._sys_dct[abs(utype)]
        div = utype < 0
        trials = []
        i_vals = []
        for i, mult in d.items():
            if div:
                trials.append(val * mult)
                i_vals.append(-i)
            else:
                trials.append(val / mult)
                i_vals.append(i)
        a = []
        for v in trials:
            num = np.mean(np.abs(np.atleast_1d(v)))
            den = np.mean(10/np.abs(np.atleast_1d(v)))
            a.append(np.max((num, den)))
        ind = a.index(min(a))
        return i_vals[ind]

    def _base_unitise_one(self, val, spec):
        div = False
        if spec < 0:
            div = True
        utype_i = abs(self._units._utypes[spec]) # length, force, etc
        if utype_i in self._units.bases:
            b = self._units.bases[utype_i] # m, N etc
        else:
            b = utype_i
        u = self._units.get_by_index(b)
        if div:
            return val * u.value, -b
        return val / u.value, b
    
    def unitise(self, val, spec):
        new_val = val
        out_spec = []
        utypes = self._units._utypes
        utype = [utypes[s] for s in spec]
        for u, s in zip(utype, spec):
            ut = self._unitise_one(new_val, u)
            new_val = new_val / self._units.get_by_index(ut).value
            out_spec.append(ut)
        s = self._units.str_spec(out_spec)
        return new_val, s
    
    def base_unitise(self, val, vector):
        base_spec = self.calc_utypes(vector)
        new_val = val
        spec = []
        for u in base_spec:
            new_val, ut = self._base_unitise_one(new_val, u)
            spec.append(ut)
        s = self._units.str_spec(spec)
        return new_val, s
    
    def unitise_typed(self, val, spec):
        out = val
        for u in spec:
            out /= self._units.get_by_index(u).value
        s = self._units.str_spec(spec)
        return out, s
    
