# -*- coding: utf-8 -*-
"""
Created on Fri May  1 11:52:42 2020

@author: Reuben
"""

from . import base
from . import system
from . import quantity
from . import unit

initialised = False
def init():
    global initialised
    quantity.set_systems(system.systems)
    unit.set_base(base.base)
    initialised = True
    
if not initialised:
    init()

units = base.base.all_units()
set_system = system.set_active