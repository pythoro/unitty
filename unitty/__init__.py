# -*- coding: utf-8 -*-
"""
Created on Fri May  1 11:52:42 2020

@author: Reuben
"""

settings = {
        'always_make_quantities': False
        }

units = None
systems = None

def get_units():
    return units

def get_systems():
    return systems

def get_system():
    return systems.active

from . import base
from . import system
from . import quantity
from . import unit

def setup(units_fname=None, units_raw=None, sys_fname=None, sys_raw=None):
    global units, systems
    units = base.Units(fname=units_fname, raw=units_raw)
    systems = system.Systems(fname=sys_fname, raw=sys_raw)
    return units, systems
    
setup()

    