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

* Convert numbers to and from different units
* Create derivative units
* Automatically switch outputs to a different unit system, without changing
any code.
* Bundle values together with units for downstream use (e.g. reports, plots). 

It is built on the idea that units provide scale factors to convert numbers
to and from values in SI base units. Since SI base units all have magnitudes of
1.0, unit information need not be in the calculations themselves.

## Quick start


## Alternatives

Several other packages might be better suited to your particular needs. Here
are some to consider:

* numericalunits: Units and dimensional analysis compatible with everything
* pint: Define, operate and manipulate physical quantities.
* quantiphy: Pairs numbers and units.
* astropy.units
* Buckingham
* DimPy
* Magnitude
* Python-quantities
* Scalar
* Scientific.Physics.PhysicalQuantities
* SciMath
* sympy.physics.units
* udunitspy
* Units
* Unum
