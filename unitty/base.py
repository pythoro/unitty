# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 18:15:23 2020

@author: Reuben

The base module for the Units class, which creates and contains a full
working set of units.

"""

import os
import ruamel.yaml as yaml
import numpy as np

from .unit import Unit

root = os.path.dirname(os.path.abspath(__file__))



class Units():
    """ Container for and creator of Unit instances. 
    
    Args:
        fname (str): [Optional] An input definition file in yaml format. If 
            both fname and raw are omitted, the default units are loaded.
        raw (dict): [Optional] If passed, while fname is left as None, 
            this data will be used to create the units.
            
    A Units instance stores a set of indices to convert between integers 
    and strings, along with a dictionary of Unit instances. The reason for
    storing the indices is because Quantity instances use integers for their
    specification (spec).
    
    Each Unit instance is keyed by its abbreviation (e.g. 'mm')
    and has a match inverse (e.g. '1/mm' Unit instance that prefixes that
    abbreviation with a '-' (e.g. '-m'). The index number of an inverse unit
    is the negative of the normal unit (e.g. if 'mm' is 13, '-mm' would be
    -13). To avoid a lot
    of string manipulation, unitty specifies units and quantities with 
    signed integers. The indices in the Units class helps those integers map
    to the right units.
    
    It's the job of the Units class to load in the
    specified units and set up the units, vectors, and indices for them.
                
    """
    def __init__(self, fname=None, raw=None):
        if fname is None and raw is None:
            fname = os.path.join(root, 'units') + '.yaml'
        raw = self._load_raw(fname) if raw is None else raw
        self.load(raw)
    
    def _ind(self, s):
        """ Get the index of a string """
        if s in self._ind_dct:
            return self._ind_dct[s]
        index = len(self._num_dct) // 2 + 1
        self._num_dct[index] = s
        self._ind_dct[s] = index
        self._num_dct[-index] = '-' + s
        self._ind_dct['-' + s] = -index
        return index
    
    def str(self, ind):
        """ Return the string for an index number """
        return self._num_dct[ind]
            
    def _new(self, index, value, vector, spec, name, utype):
        """ Internal creation of one unit """
        abbr = self.str(index)
        if abbr in self.units:
            raise KeyError(abbr + ' is already defined.')
        self._utypes[index] = utype
        u = Unit(value=value, spec=spec, vector=vector, abbr=abbr, name=name)
        self.safe_set(self.units, abbr, u)
        return u
    
    def new(self, index, value, vector, spec, name, utype):
        """ Create a new unit 
        
        
        TODO: Use of the index here is unnecessary. Could replace with 
        the abbreviation.
        
        """ 
        u = self._new(index, value, vector, spec, name, utype)
        # Now make the corresponding inverse ('negative') unit
        spec = [-s for s in spec]
        self._new(-index, 1/value, -vector, spec, name, -utype)
        return u
    
    def _make_utypes(self, types):
        """ Make the base types (length, time, etc) 
        
        Args:
            types (list[str]): A list of base type strings. These can be
                anything, but the base units need to refer to them.
                
        """
        self.utypes = types
        def vec(ind):
            a = np.zeros(len(types))
            a[ind] = 1
            return a
        for i, t in enumerate(types):
            index = self._ind(t)
            self.new(index, 1.0, vec(i), [index], t, index)
    
    def _clear(self):
        self.units = {} # The unit instances
        self.bases = {} # The base units for time, length, etc
        self._utypes = {} # the length, time etc for given id
        self._num_dct = {} # The attr for given index
        self._ind_dct = {} # the index for given attr
        
    def load(self, dct):
        self._clear()
        self._make_type_dct(dct)
    
    def _load_raw(self, fname):
        with open(fname, 'r') as f:
            raw = yaml.safe_load(f)
        return raw
    
    def safe_set(self, unit_dct, key, val):
        if key in unit_dct:
            raise KeyError(key + ' already defined.')
        else:
            unit_dct[key] = val
        
    def _derive(self, spec):
        us = [self[u] for u in spec]
        vector = np.sum([u.vector for u in us], axis=0)
        value = np.prod([u.value for u in us])
        return value, vector
        
    def _make_unit(self, units, utype, index, v):
        if len(v) == 4:
            value, derivation, name, dct = v
        else:
            dct = None
            value, derivation, name = v
        if not isinstance(derivation, list):
            derivation = [derivation]
        m, vector = self._derive(derivation)
        spec = [index]
        val = value * m
        self.new(index, val, vector, spec, name, utype)
        if dct is not None and 'SI_prefixes' in dct:
            self._make_si_prefixed(dct, index, val, vector, spec, name, utype)
    
    def _make_si_prefixed(self, dct, index, val, vector, spec, name, utype):
        names = ['yotta', 'zetta', 'exa', 'peta', 'tera', 'giga', 'mega',
                 'kilo', 'hecto', 'deca', 'deci', 'centi', 'milli', 'micro',
                 'nano', 'pico', 'femto', 'atto', 'zepto', 'yocto']
        symbols = ['Y', 'Z', 'E', 'P', 'T', 'G', 'M', 'k', 'h', 'da', 'd',
                   'c', 'm', 'u', 'n', 'p', 'f', 'a', 'z', 'y']
        mults = [1.e+24, 1.e+21, 1.e+18, 1.e+15, 1.e+12, 1.e+09, 1.e+06, 1.e+03,
                 1.e+02, 1.e+01, 1.e-01, 1.e-02, 1.e-03, 1.e-06, 1.e-09, 1.e-12,
                 1.e-15, 1.e-18, 1.e-21, 1.e-24]
        abbr = self.str(index)
        for n, s, m in zip(names, symbols, mults):
            if s not in dct['SI_prefixes']:
                continue
            prefixed = s + abbr
            prefixed_name = n + name
            i = self._ind(prefixed)
            v = val * m
            self.new(i, v, vector, spec, prefixed_name, utype)
    
    def _make_type_dct(self, dct):
        units = self.units
        for utype_str, d in dct.items():
            if utype_str=='base_types':
                self._make_utypes(d)
                present = {k: False for k in self._utypes.keys() if k > 0}
                continue
            utype = self._ind(utype_str)
            present[utype] = True
            for abbr_str, v in d.items():
                if abbr_str == '_base':
                    # Set the base for the utype
                    self.bases[utype] = self._ind(v)
                else:
                    index = self._ind(abbr_str)
                    self._make_unit(units, utype, index, v)
        if not all(present.values()):
            for k, v in present.items():
                if v is not True:
                    break
            raise ValueError('Type ' + self.str(k) 
                    + ' missing from specification.')

    def __getitem__(self, abbr):
        if isinstance(abbr, tuple):
            u = self.from_str(abbr[0])
            u.set_ref(abbr[1])
            return u
        if abbr in self.units:
            return self.units[abbr]
        return self.from_str(abbr)

    def __getattr__(self, abbr):
        if abbr not in ['units', 'bases'] and abbr in self.units:
            return self.units[abbr]
        else:
            return self.__getattribute__(abbr)
    
    def get_by_index(self, i):
        return self.units[self._num_dct[i]]
    
    def str_spec(self, spec):
        if spec is None:
            return 'base'
        elif len(spec)==0:
            return 'dimensionless'
        num = [i for i in spec if i > 0]
        den = [-i for i in spec if i < 0]
        def f(v, c):
            if c == 1:
                return v
            else:
                return v + str(c)
        def process(lst):
            out = [self._num_dct[i] for i in lst]    
            out.sort()
            d = {v: out.count(v) for v in out}
            return [f(v, c) for v, c in d.items()]
        num = process(num)
        den = process(den)
        s_num = '1' if len(num) == 0 else '.'.join(num)
        n = len(den)
        if n == 0:
            return s_num
        elif n == 1:
            return s_num + '/' + den[0]
        else:
            return s_num + '/(' + '.'.join(den) + ')'

    def spec_from_str(self, s, sep=','):
        if s is None or s in ['', 'dimensionless']:
            return []
        slash_count = s.count('/')
        open_bracket_count = s.count('(')
        close_bracket_count = s.count(')')
        if s.count('-') > 0:
            raise ValueError('Unit string  "' + str(s) + '" invalid: ' +
                             'negatives are not allowed.')
        if s.count('^') > 0:
            raise ValueError('Unit string  "' + str(s) + '" invalid: ' +
                             'power symbols ("^") should be omitted.')
        if open_bracket_count != close_bracket_count:
            raise ValueError('Unit string  "' + str(s) + '" does not have ' +
                             'a matching number of open and close brackets.')
        if open_bracket_count > 1:
            raise ValueError('Unit string  "' + str(s) + '" invalid. Only ' +
                             'one set of brackets in the denominator is ' +
                             'allowed.')
        if slash_count > 1:
            raise ValueError('Unit string "' + str(s) + '" is invalid. They ' +
                             'can have at most one divide symbol.')
        elif slash_count == 1:
            num, den = s.split('/')
            num = num.strip(' ()')
            den = den.strip(' ()')
        else:
            num = s.strip(' ()')
            den = ''
        if num in ['1', '1.0']:
            num = ''
            
        def process(st):
            if len(st) == 0:
                return []
            out = []
            st = st.replace(' ', '.')
            lst = st.split('.')
            for item in lst:
                if item in self._ind_dct:
                    out.append(self._ind_dct[item])
                    continue
                n = 1
                if item[-1].isnumeric():
                    n = int(item[-1])
                    item = item[:-1]
                if item in self._ind_dct:
                    for i in range(n):
                        out.append(self._ind_dct[item])
                    continue
                raise ValueError('Unit "' + str(item) + '" not recognised.')
            return out

        num_lst = process(num)
        den_lst = process(den)
        den_lst = [-s for s in den_lst]
        return num_lst + den_lst

    def from_str(self, s):
        if s in self.units:
            return self.units[s]
        spec = self.spec_from_str(s)
        index = self._ind(s)
        units = [self.get_by_index(i) for i in spec]
        vector = np.sum([u.vector for u in units], axis=0)
        value = np.prod([u.value for u in units])
        name = s
        utype = 0
        return self.new(index, value, vector, spec, name, utype)
        
    