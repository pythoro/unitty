# -*- coding: utf-8 -*-
"""
Created on Fri May  1 11:52:42 2020

@author: Reuben
"""

from . import base
from . import system
from . import quantity
from . import unit

def init():
    global initialised
    quantity.set_systems(system.systems)
    initialised = True
    
init()

units = base.units
set_system = system.set_system