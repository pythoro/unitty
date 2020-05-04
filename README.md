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

TODO

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


