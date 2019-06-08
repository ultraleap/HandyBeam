:doc:`index`

#######################
OpenCL kernel : "clist"
#######################

************
Introduction
************

This OpenCL kernel calculates the complex acoustic field pressure for given inputs:

* Description of transmitters (transducers)
* Description of environment
* A list of XYZ points in space where the complex acoustic field pressure is to be calculated

Signature is as follows:

.. code-block:: none

    __kernel void _handybeam1kernel_clist(
        __global const float *cl_TxArrayDescriptor1,
        unsigned int tx_count,
        __global float *sampling_point_list,
        unsigned int sampling_point_list_count,
        __global float *cl_field, // output buffer: pressure field p, into an on-device write-able buffer
        float medium_wavenumber,
        float transducer_nan_size
        )



.. include:: footer_licence_note.rst

