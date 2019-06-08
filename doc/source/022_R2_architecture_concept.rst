.. todo::

    This is an unfinished document



:doc:`index`

==========================
R2 Architecture -- concept
==========================

Introduction
------------

HandyBeam R1 was loosely based on the University of Strathclyde's cueBeam, plus my efforts to switch from Matlab to Python.

Having the experience of doing that, the current concept for R2 is to decouple the existing objects a bit, and rely on flat data structures more.

.. Note::

    Only primary and most important methods are intended to be listed here. Helper methods are to be documented from within the autodoc.


Objects
-------

* World
* TxArray - multi types
* Sampler - multi types

Depreciated objects

* TxElement. Experience shows that doing operations on lists of objects was the slowest part of HandyBeam R1, obstructing research efforts. For R2, it will be replaced with a flat buffer (ndarray) of parameters.

Data structures
---------------

* FrequencyModeArray - full description of a location, phase and amplitude of elements in array, for single-frequency transmission
* TypicalTxDirectivity - descriptor of per-element directivity of a transducer. Intended to be common to all transducers in the array.

* SampledFieldXYZ - list of coordinates for sampling
* SampledFieldComplex - basic list of results from sampling the acoustic field at locations of SampledFieldXYZ
* SampledFieldSPL - same format as SampledFieldComplex, but with values already converted to Sound Pressure Level (SPL) - to save the effort on the CPU side

Procedures -- primary
---------------------

* Solve excitation for single focal point - Jurek's basic method
* Solve excitation for multiple focal points - UH's eigenvalue power iteration method
* Solve excitation for surface - Sal's method

Notes
-----

No notes at this time.

.. include:: footer_licence_note.rst

