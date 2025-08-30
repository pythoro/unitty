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

`unitty` provides a number of functions. These are documented in the 
namespace module. 

"""

settings = {
        'always_make_quantities': False
        }

from . import namespace
from .namespace import get_units, get_systems, get_system, get_active, \
    set_system, setup
from . import base
from . import system
from . import quantity
from . import unit
from . import utils

# Inject dependencies
namespace._inject(base.Units, system.Systems)
    