Quick start
===========

Load the default units and unit systems:
::

    import unitty
    u = unitty.get_units()

Getting units
-------------

`unitty` supports attribute and string methods to get units.
::

    u.kg
    # 1 kg

    u['kg']
    # 1 kg

Strings can be complex, like this:
::

    u['kg/(s2.m)']


There are a few rules to formatting the strings:

* Use only one divide symbol ('/')
* Use only one pair of brackets in the dividend, if needed
* Use a period ('.') to signify multiplication
* Do not include an exponent symbol ('^'). For example, for square meters,
  write 'm2'.


Basic calculations
------------------

Use the units to get an input into a base unit system.
::

    v = 5 * u.ft
    v
    # 1.524


We get 1.524, which is in the defalut base unit for length, which is meters.
We can multiply and divide units in sensible ways:
::

    v2 = q = 5 * u.lbs / u.ft2
    v2
    # 24.4121

This gives 24.4121, which is in kg/m^2 (we'll omit power symbol and write this
as 'kg/m2').

Making quantities
-----------------

Now we'll create quantities like this:
::
    
    q = 5 << u.lbs / u.ft2
    q
    # 24.4121 kg/m2
    
    # Alternatively:
    q = 5 << u['lbs/ft2']
    
    val, s = q.in_sys()
    val
    # 24.4121
    s
    # 'kg/m2'
    
    q.str_in_sys()
    # 24.4121 kg/m2


Switching unit systems
----------------------

The Quantity `q` displays as '24.4121 kg/m2', since it's a `Quantity` that
includes unit information. Now, let's change our unit system to another
preloaded one and look at it again:
::
    
    unitty.set_system('US')
    q
    # 5 lbs/ft2
    
    val, s = q.in_sys()
    val
    # 4.999999999999999
    s
    # 'lbs/ft2'
    
    q.str_in_sys()
    # 5 lbs/ft2

Now, `q` shows as '5 lbs/ft2'. 

We can use the `in_sys` method to get the 
value and units in this new unit system. But it's still the same underlying
value, which we can see via:
::
    
    val, s = q.in_base()
    val
    # 24.4121
    s
    # 'kg/m2'
    
    q.str_in_base()
    # 24.4121 kg/m2

We can make a new Quantity while in this unit system:
::

    q2 = 7 << u.lbs / u.ft2
    q2
    # 7 lbs/ft2


Importantly, the value of q2 is still in base units:
::

    q2.str_in_base()
    # 34.177 kg/m2
    q2.value
    34.177


We can switch back to metric (the default unit system), and take a look at
out quantities again:
::
    
    unitty.set_system('metric')
    q
    # 24.4121 kg/m2
    q2
    0.34177 kg/cm2

Named quantity types
--------------------

Notice that in the above, q2 displays in different units. That's because by
default, it guesses the best available combination of units in the unit system
to display in a friendly way. Often, though, there are particular units
we want to display in, which depend on the unit system we want to us. 
For one-off cases, we can do this:
::

    val, s = q2.in_units(u['kg/m2'])
    val
    # 34.17699345
    s
    # 'kg/m2'


If we have many such quantities, we can do this automatically. We can define
some named quantity types in a csv file, like this one that we'll
call `example.csv`:

+---------------+-------------+------------+
| ref           | metric      | US         |
+===============+=============+============+
| widget_length | mm          | in         |
+---------------+-------------+------------+
| complex.value | kg.s2/m     | lbs.s2/ft  |
+---------------+-------------+------------+

Then we apply it like this:
::

    s = unitty.get_systems() # The object that looks after different unit systems
    s.set_refs('example.csv')


Now we can name the quantity types like this:
::

    q2.set_ref('complex.value')

A shorthand way is to add the 'ref' (quantity reference) when getting
the unit:
::

    q2 = 7 << u['lbs/ft2', 'complex.value']

Now, the display of the unit automatically matches the units we've specified.
::

    unitty.set_system('US')
    q2
    # 7 lbs/ft2
    
    unitty.set_system('metric')
    q2
    # 34.17699345 kg/(m2)
    
    val, s = q.in_sys()
    val
    # 34.17699345
    s
    # kg/(m2)

