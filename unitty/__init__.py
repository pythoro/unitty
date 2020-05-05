# -*- coding: utf-8 -*-
"""
Created on Fri May  1 11:52:42 2020

@author: Reuben
"""

settings = {
        'always_make_quantities': False
        }

active = None
container = {}

def get_units(name=None):
    name = active if name is None else name
    return container[name]['units']

def get_systems(name=None):
    name = active if name is None else name
    return container[name]['systems']

def get_system(name=None):
    name = active if name is None else name
    return container[name]['systems'].active

def get_active():
    return active

def set_system(sys_name, name=None):
    name = active if name is None else name
    systems = get_systems(name)
    systems.set_active(sys_name)

from . import base
from . import system
from . import quantity
from . import unit

def setup(name, units_fname=None, units_raw=None, sys_fname=None, sys_raw=None):
    global active
    container[name] = {}
    active = name
    units = base.Units(fname=units_fname, raw=units_raw)
    container[name]['units'] = units
    systems = system.Systems(fname=sys_fname, raw=sys_raw)
    container[name]['systems'] = systems
    
    
setup('default')

    