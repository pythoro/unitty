# -*- coding: utf-8 -*-
"""
Created on Mon May 11 20:58:06 2020

@author: Reuben

The namespace module contains groups of Unit, Units, Systems, and System
instances that work together. It allows multiple groups to be loaded
concurrently, which is probably not usually needed.

Each set of Units, Quantity, Systems, and System objects are designed to be
instantiated in groups through the :func:`setup` function. This is called
if required to set up the default units.

"""

Units = None # Replaced by real class
Systems = None  # Replaced by real class

active = None
container = {}

def _inject(Units_cls, Systems_cls):
    """ Inject these classes to prevent circular dependency """
    global Units, Systems
    Units = Units_cls
    Systems = Systems_cls

def _ensure_exists(group=None):
    """ Sets up the default group if needed"""
    group = active if group is None else group
    if group is None:
        setup('default')
        group = 'default'
    return group
    

def get_units(group=None):
    """ Get the Units instance 
    
    Args:
        group (str): [Optional] The name of the group. If None, returns the
        Units instance from the currently active group.
        
    Returns:
        Units: A Units instance.
        
    """
    group = _ensure_exists(group)
    return container[group]['units']

def get_systems(group=None):
    """ Get the Systems instance 
    
    Args:
        group (str): [Optional] The name of the group. If None, returns the
        Systems instance in the currently active group.
        
    Returns:
        Systems: A Systems instance.
    """
    group = _ensure_exists(group)
    return container[group]['systems']

def get_system(group=None):
    """ Get the currently active System instance 
    
    Args:
        group (str): [Optional] The name of the group. If None, returns the
            currently active System instance from the currently active group.
        
    Returns:
        Systems: A Systems instance.
    """
    group = _ensure_exists(group)
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
    group = _ensure_exists(group)
    systems = get_systems(group)
    systems.set_active(sys_name)

def setup(group='default',
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
    units = Units(fname=units_fname, raw=units_raw)
    container[group]['units'] = units
    systems = Systems(fname=sys_fname, raw=sys_raw)
    container[group]['systems'] = systems
    

