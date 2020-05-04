# -*- coding: utf-8 -*-
"""
Created on Fri May  1 11:52:42 2020

@author: Reuben
"""

settings = {
        'always_make_quantities': False
        }

from . import base
from . import system
from . import quantity
from . import unit

def init():
    global initialised, base
    quantity.set_systems(system.systems)
    quantity.set_units(base.units)
    initialised = True
    
init()

units = base.units
set_system = system.set_system

