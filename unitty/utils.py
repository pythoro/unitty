# -*- coding: utf-8 -*-
"""
Created on Thu May  7 10:54:00 2020

@author: Reuben

The :mod:`utils` module contains helper functions to allow users to quickly
process input or output data, automatically converting between units as
required.

"""

from . import get_units

def split_str(s):
    start = s.find('[')
    end = s.find(']')
    if start == -1 or end == -1:
        return None
    return s[:start].strip(), s[start+1:end].strip()

def str_to_unit(s):
    ref, unitstr = split_str(s)
    if unitstr is None:
        unitstr = s
    return get_units()[unitstr]

def make_qty(s, val):
    ref, unitstr = split_str(s)
    if unitstr is None:
        unitstr = s
    unit = get_units()[unitstr]
    q = val << unit
    q.set_ref(ref)
    return q

def add_unit(s, unit_str):
    return s + ' [' + unit_str + ']'

def split_qty(q, name=None):
    val, s = q.in_sys()
    if name is None and q._ref is not None:
        name = q._ref
    return add_unit(name, s), val

def transform_pair(s, val):
    try:
        q = make_qty(s, val)
        tup = split_qty(q)
    except:
        return s, val
    return tup
    
def transform_dict(dct):
    tups = [transform_pair(k, v) for k, v in dct.items()]
    return {k: v for k, v in tups}

def transform_list_of_dicts(lst):
    return [transform_dict(dct) for dct in lst]

def transform_df(df):
    ''' Pandas dataframe '''
    df2 = df.copy()
    cols = list(df.columns)
    dct = {k: df2[k].mean() for k in cols}
    transformed = transform_dict(dct)
    df2.columns = transformed.keys()
    new_unit_values = [str_to_unit(k).value for k in transformed.keys()]
    old_unit_values = [str_to_unit(k).value for k in cols]
    ratios = [old/new for old, new in zip(old_unit_values, new_unit_values)]
    transformed = {k: ratios[i] for i, k in enumerate(transformed.keys())}
    for k, v in transformed.items():
        df2[k] = df2[k] * v
    return df2


# Add dictionaries, and lists of dictionaries.