.. todo::

    Add content from `Rob's write-up <https://developer.ultrahaptics.com/knowledgebase/science-phased-arrays/>`_


:doc:`index`

==========
Philosophy
==========

The purpose is what defines us
------------------------------


.. code-block:: python

    "The purpose of computer simulations is to reduce the total cost of doing the job, not to increase it"

    -- Richard O''Leary, University of Strathclyde, c.a. 2011


Why HandyBeam?
--------------

As of 2018, we really do not know what reality REALLY is - as far as we know, we might never know.
But, we can make models. The usefulness of the models is that they can help to explain the past and predict the future.

Models range from simple, empirical closed-form equations like Newton's :code:`Force = Mass * acceleration` ,
through to finite-element models (FEM) that require equation-solving with millions of unknowns.

Accuracy, and therefore the usefulness of many of the models, are often compute bound.
A more accurate solution can be produced at the cost of performing a greater number of computations.
However, these computations bear a cost in terms of hardware, energy and, most importantly, time.
Hence, there still exists a market for building simplified models of reality;
ones that capture just enough of the complexity of real phenomena, but at the same time, are computably affordable.

The HandyBeam approach
----------------------

HandyBEAM R1 is a software package that, in it's core, implements the continuous-wave (monochromatic, single-frequency)
form of the Huygens principle of wave propagation in homogeneous media.

This ultra-simplified propagation model enables obtaining quick estimates of pressure field shape,
beam width, side lobe amplitude, and more -- suitable for use in beamforming research,
NDT/NDE, acoustics research and education.

The algorithm is decomposed in such a way that each thread of the GPU or OpenMP
calculates the pressure value for a single point in space (single pixel) only.
This allows all the computations to progress in parallel, as the pressure for any given pixel is completely
and solely defined by the properties of the radiators and the media.
Hence, there is no need for communication between the threads. This approach also happens to match well with the
hardware structure of the GPU, providing excellent performance.


This approach is admittedly less accurate than other published methods, but the advantage is
in its low computation cost, and consequently, short design cycles.

History
-------

HandyBeam is partially based on technology developed in `The University of Strathclyde <https://www.strath.ac.uk/research/subjects/electronicelectricalengineering/instituteforsensorssignalscommunications/centreforultrasonicengineering/>`_  - see the source code `published on GitHub <https://github.com/CentreForUltrasonicEngineering/cueBeam_EngD>`_ . The development of cueBeam stopped in approximately 2012, with only minor corrections afterwards.

The development of HandyBeam started in 2018, with first public release in 2019.

The entire software has been rewrited from scratch as a OpenCL kernel, loaded via :code:`pyopencl` package into the python interpreter.



.. include:: footer_licence_note.rst

