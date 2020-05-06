# unitty

Unitty (pronounced 'unity') provides units when you need them, not when you
don't. It's based on a phiolosophy that:

* Units are useful for inputs
* Units are useful for outputs (e.g. reports, plots)
* Calculations are done in SI units, so units are not needed unless checking.
* Unittests are used to encompass dimensional checks. Dimensional checks
themselves are insufficient.
* Quantities are named adequately in the code (e.g. 'area', 'length', 'mass').
The kind of quantity they represent is clear from their names, and so 
representing it elsewhere is typically redundant. 

Unitty provides a flexible, lightweight package to:

* Automatically switch outputs to a different unit system using a single 
command, while keeping meaningful units (e.g. for force, pressure, etc.).
This capability was a core reason to write unitty.
* Apply units intuitively.
* Convert numbers to and from different units.
* Fully customise units and unit systems. The user needs full flexibility
of the systems and units used.
* Bundle values with units into quantities for downstream use (e.g. reports,
plots).
* Not lock the user into objects with units attached. By default, units
are not attached to calculation objects - the results are simply floats or
arrays. This behaviour can be changed automatically to do dimensional
checks during unittesting. 
* Use meaningful units (e.g. for force, pressure, etc.) while also allowing
dimensionality reduction and checking. Automatic dimensionality reduction 
in some other packages can be frustrating.

It is built on the idea that units provide scale factors to convert numbers
to and from values in SI base units. Since SI base units all have magnitudes of
1.0, unit information need not be in the calculations themselves.

## Quick start

Load the default units and unit systems:

```python

import unitty
u = unitty.get_units()

```

### Basic calculations

Use the units to get an input into a base unit system:

```python

v = 5 * u.ft
v
# 1.524
```

We get 1.524, which is in the defalut base unit for length, which is meters.
We can multiply and divide units in sensible ways:

```python
v2 = q = 5 * u.lbs / u.ft2
v2
# 24.4121
```

This gives 24.4121, which is in kg/m^2 (we'll omit power symbol and write this
as 'kg/m2').

### Making quantities

Now we'll create quantities like this:

```python

q = 5 << u.lbs / u.ft2
q
# 24.4121 kg/m2

val, s = q.in_sys()
val
# 24.4121
s
# 'kg/m2'

q.str_in_sys()
# 24.4121 kg/m2

```

### Switching unit systems

The Quantity `q` displays as '24.4121 kg/m2', since it's a `Quantity` that
includes unit information. Now, let's change our unit system to another
preloaded one and look at it again:

```python

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

```

Now, `q` shows as '5 lbs/ft2'. 

We can use the `in_sys` method to get the 
value and units in this new unit system. But it's still the same underlying
value, which we can see via:

```python

val, s = q.in_base()
val
# 24.4121
s
# 'kg/m2'

q.str_in_base()
# 24.4121 kg/m2

```

We can make a new Quantity while in this unit system:

```python

q2 = 7 << u.lbs / u.ft2
q2
# 7 lbs/ft2

```

Importantly, the value of q2 is still in base units:

```python

q2.str_in_base()
# 34.177 kg/m2
q2.value
34.177

```

We can switch back to metric (the default unit system), and take a look at
out quantities again:

```python

unitty.set_system('metric')
q
# 24.4121 kg/m2
q2
0.34177 kg/cm2

```

### Unit display

Notice that in the above, q2 displays in different units. That's because by
default, it guesses the best available combination of units in the unit system
to display in a friendly way. Sometimes, we want to set the units, so we can
do this:

```python

q2
0.34177 kg/cm2

```


## Alternatives

Several other packages might be better suited to your particular needs. Here
are some to consider, along with some notes. It is believed that none of
these other packages allow to automatically switch outputs between unit
systems with a single command.

* numericalunits: Units are values. Simple.
* astropy.units: Great, but locks units into calculation values - can't get
back to simple floats or arrays.
* sympy.physics.units: Solid.
* pint: A very powerful units package.
* unyt: An excellent and capable package.
* quantiphy: Seems a bit awkward to use.
* Buckingham: A bit awkward to use.
* DimPy: Very old.
* Magnitude: Clunky to use.
* Python-quantities: A good package.
* physipy: Another good package
* SciMath Units: Large range of units.
* cf_units: Suggested replacement of old udunitspy package. Clunky.
* Units
* Unum
* quantities
* physical-quantities
* parampy
* pynbody
* misu
* pysics


