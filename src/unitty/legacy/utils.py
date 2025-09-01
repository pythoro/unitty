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
    """ Split out units from a string suffixed with units in square brackets
    
    Args:
        s (str): A string with units at the end in square brackets (e.g.
          'widget.length [mm]').
    
    Returns:
        tuple: The string with it's units stripped (e.g. 'widget.length'),
        and the unit string (e.g. 'mm').
    
    Examples:
    ::
        
        split_str('length ['mm'])
        # ('length', 'mm')
        
        split_str('a long string with spaces [W/m2]')
        # ('a long string with spaces', 'W/m2')
        
    """
    start = s.find('[')
    end = s.find(']')
    if start == -1 or end == -1:
        return None
    return s[:start].strip(), s[start+1:end].strip()

def str_to_unit(s):
    """ Return the unit within square brackets in a string
    
    Args:
        s (str): A string with units at the end in square brackets (e.g.
          'widget.length [mm]').
    
    Returns:
        Unit: The Unit instance corresponding to the string. If it is not
        already defined, unitty will attempt to derive it from the string.
    """
    ref, unitstr = split_str(s)
    if unitstr is None:
        unitstr = s
    return get_units()[unitstr]

def make_qty(s, val):
    """ Make a Quantity from a unit-containing string and a value
    
    Args:
        s (str): A string with units at the end in square brackets (e.g.
          'widget.length [mm]').
        val (int, float, arraylike): A value in the units indicated within
            the string, `s`. 
    
    Returns:
        Quantity: The Quantity specified by the value and units. The Quantity
        will have a reference set by the body of the string (e.g.
        'widget.length').
    """
    ref, unitstr = split_str(s)
    if unitstr is None:
        unitstr = s
    unit = get_units()[unitstr]
    q = val << unit
    q.set_ref(ref)
    return q

def add_unit(s, unit_str):
    """ Append a unit string within square brackets to a string
    
    Args:
        s (str): A string without units (e.g. 'widget.length').
        unit_str (str): The unit string to attach (e.g. 'mm')
        
    Returns:
        str: A string with units appneded in square brackets (e.g.
        'widget.length [mm]')
    """
    return s + ' [' + unit_str + ']'

def split_qty(q, name=None):
    """ Split a Quantity into a string with units appended and a value
    
    Args:
        q (Quantity): The quantity
        name (str): [Optional] The name to use for the string. If omitted,
            the name will default to the reference set in the Quantity. 
        
    Returns:
        tuple: A string with units suffixed in square brackets, and the value
        in those units. The units are selected through the currently active
        system, either automatically, or by those specified through 
        reference quantity types.
    """
    val, s = q.in_sys()
    if name is None and q._ref is not None:
        name = q._ref
    return add_unit(name, s), val

def transform_pair(s, val):
    """ Transform a string-value pair into the current unit system
    
    Args:
        s (str): A string with units at the end in square brackets (e.g.
          'widget.length [ft]').
        val (int, float, arraylike): The value in those units.
        
    Returns:
        tuple: A string with units in the current unit system (e.g.
        'widget.length [m]', plus the value expressed in those units.
    """
    try:
        q = make_qty(s, val)
        tup = split_qty(q)
    except:
        return s, val
    return tup
    
def transform_dict(dct):
    """ Transform a dictionary of values into the current unit system
    
    Args:
        dct (dict): Each key should be a name with units suffixed in square
            brackets (e.g. 'widget.length [mm]'). Each key should be the 
            magnitude of the quantity expressed in those units.
    
    Returns:
        dct (dict): A transformed dictionary, in which the keys have units
        in the current unit system and the values are automatically converted
        to match those units. Keys without unit information, or ones in which
        a conversion error arises, are returned unchanged.

    """
    tups = [transform_pair(k, v) for k, v in dct.items()]
    return {k: v for k, v in tups}

def transform_list_of_dicts(lst):
    """ Transform a list of dictionaries into the current unit system
    
    Args:
        lst (list): A list of dictionaries as for the :func:`transform_dict`
            function.
        
    Returns:
        list: A list of dictionaries, where each is the output of the 
        :func:`transform_dict` function.
        
    """
    return [transform_dict(dct) for dct in lst]

def transform_df(df):
    """ Transform a pandas dataframe into the current unit system
    
    Args:
        df (DataFrame): A pandas dataframe. Column names with units should
            have them within square brackets at the end of each name.
        
    Returns:
        DataFrame: A dataframe in which the column units have been changed
        into the current unit system and the table values have been changed
        into those new units.
        
    """
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


