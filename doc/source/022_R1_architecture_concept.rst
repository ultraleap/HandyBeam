.. todo::

    This is an unfinished document

R1 architecture
---------------

Before we continue, please briefly see :doc:`philosophy of API items - data, procedures, objects <023_api_principles>`

The top level items of interest are:

World
~~~~~

:py:class:`handybeam.world.World` contains description of the world's properties. Conceptu

* tx_array, and tx_element - describe the transmitter array, and the elements of the array respectively
* excitation_solver - container for procedures that set the amplitude and phase for tx_array
* xy_field and yz_field, both descend from abstract_field - describe how the acoustic field is sampled
* propagator - container for the compute engine that takes the world's description and populates(calculates) the field's samples
* `cxyz` is a specific kind of wave propagation engine: "Complex(frequency-domain) with orthogonal cube of pixels on XYZ". There could be more than one wave propagators, but for R1 I only have one.

![api structure](../img/architecture.png)

## Not mantained examples - might be using old API, but probably repairable:

* essentially, all other try* , basic*, devel* and HN* scripts are not mantained and might fall into obsolence due to the API development. When I release the "official" release, I will make sure that all the examples in the `examples` folder work, but any unofficial release is naturally a work-in-progress.

.. include:: footer_licence_note.rst

