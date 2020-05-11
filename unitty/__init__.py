# -*- coding: utf-8 -*-
"""
Created on Fri May  1 11:52:42 2020

@author: Reuben

This section provides an overview of how the `unitty` package works.

Quantities and Units classes
============================

The foundational class in unitty is the Quantity. A Unit is a special type 
of Quantity that also has an abbreviation and name. Units also display a 
little differenty. 

Each Quantity contains:
    
* **value:** A float representing the magnitude of the quantity in terms of 
  base dimensions (length, time, mass, etc)
* **spec:** A list of signed integers. For simple units, there will be only one
  integer. For compound units (e.g. m/s), there will be more than one.
  The integers correspond to other Quantities. Positive 
  integers indicate the are multiplied, while negative integers indicate 
  they are divided.
* **vector:** Each base dimensions is independent, and the exponent for each
  base dimension is represented as a number. This vectore is an array
  of such numbers for all base dimensions. This allows quick and robust
  dimensionality checking.
* **abbr [optional]:** The abbreviation of the Quantity (usually for Units)
* **name [optional]:** The name of the Quantity (usually for Units)
* **parent [optional]:** The name of the Units instance it belongs to. This is
  important, since otherwise the spec doesn't make any sense.

    
The Units class
===============

A Units instance contains all of the Units that you might want to work with
at the same time. The Units class holds:

* The Unit instances
* Mappings between string abbreviations for those units and the integers that 
  match them.
* A mapping of the base type (length, time, etc) for each unit.

The System class
================

This class contains information about a particular unit system. It is
responsible for processing a given Quantity to give the correct
value and unit string for that unit system. The magnitudes in all Quantity
instances correspond to the base dimensions, and systems allow different
those magnitudes to be expressed in different units. For example, 
1 'length' might be expressed as 1 meter in the metric system, but 3.28083
feet in the imperial US system.

System instances contain information about:

* The preferred units to use in the system for each base type. For example,
  the length dimension in the metric system might use um, mm, m, and km. 
  A US system might specifiy units of inch, ft, and mile for length.
* How to apply the preferred units to express Quantities in those units.

The Systems class
=================

The Systems class contains all the different systems that you might want to
switch between. It is provides a way to set up those different systems
from specification files.

Systems instances know which system is active, and direct methods to
express quantities to methods in that active system.

Functions
=========

`unitty` provides a number of api functions. These are documented below. Each
set of Units, Quantity, Systems, and System objects are designed to be
instantiated in groups through the :func:`setup` function. 

"""

settings = {
        'always_make_quantities': False
        }

active = None
container = {}

def get_units(group=None):
    """ Get the Units instance 
    
    Args:
        group (str): [Optional] The name of the group. If None, returns the
        Units instance from the currently active group.
        
    Returns:
        Units: A Units instance.
        
    """
    group = active if group is None else group
    return container[group]['units']

def get_systems(group=None):
    """ Get the Systems instance 
    
    Args:
        group (str): [Optional] The name of the group. If None, returns the
        Systems instance in the currently active group.
        
    Returns:
        Systems: A Systems instance.
    """
    group = active if group is None else group
    return container[group]['systems']

def get_system(group=None):
    """ Get the currently active System instance 
    
    Args:
        group (str): [Optional] The name of the group. If None, returns the
        currently active System instance from the currently active group.
        
    Returns:
        Systems: A Systems instance.
    """
    group = active if group is None else group
    return container[group]['systems'].active

def get_active():
    """ Return a string of the currently active group """
    return active

def set_system(sys_name, group=None):
    """ Make the named unit system active
    
    Args:
        sys_name (str): The name of the unit system to activate
        group (str): [Optional] The name of the group. The unit system is
        set within the Systems instance of that group. Defaults to the 
        currently active group.
    
    """
    group = active if group is None else group
    systems = get_systems(group)
    systems.set_active(sys_name)

from . import base
from . import system
from . import quantity
from . import unit
from . import utils

def setup(group,
          units_fname=None,
          units_raw=None,
          sys_fname=None,
          sys_raw=None):
    """ Setup a new group of Units, Systems, and System instances
    
    Args:
        group (str): The name of the group
        units_fname (str): [Optional] The filename of the input file to use
        for the Units class. If omitted, the default is loaded.
        units_raw (dict): [Optional] A dictionary of unit data to use. If 
        given, units_fname should not be given.
        sys_fname (str): [Optional] The filename of the input file to use
        for the Systems class. If omitted, the default is loaded.
        sys_raw (dict): [Optional] A dictionary of data to use for the unit
        systems. If given, sys_fname should not be given.
        
    """
    global active
    container[group] = {}
    active = group
    units = base.Units(fname=units_fname, raw=units_raw)
    container[group]['units'] = units
    systems = system.Systems(fname=sys_fname, raw=sys_raw)
    container[group]['systems'] = systems
    
try:
    setup('default')
except:
    pass

    