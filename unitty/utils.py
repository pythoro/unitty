# -*- coding: utf-8 -*-
"""
Created on Thu May  7 10:54:00 2020

@author: Reuben
"""

from . import get_units

def split_str(s):
    start = s.find('[')
    end = s.find(']')
    if start == -1 or end == -1:
        return None
    return s[:start].strip(), s[start+1:end].strip()

def str_to_unit(s):
    _, unitstr = split_str(s)
    if unitstr is None:
        unitstr = s
    return get_units()[unitstr]

def make_qty(s, val):
    unit = str_to_unit(s)
    return val << unit

def add_unit(s, unit_str):
    return s + ' [' + unit_str + ']'

def split_qty(name, q):
    val, s = q.in_sys()
    return add_unit(name, s), val

# Add dictionaries, and lists of dictionaries.