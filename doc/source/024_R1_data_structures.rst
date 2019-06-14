:doc:`index`

===============
Data structures
===============

This chapter describes the data structures that are critical to the high performance operation of the OpenCL/CUDA kernels.

Some data structures will have a pythonic browser-editor class, however, for highest possible performance,
it might be necessary to edit them directly.

This description will also come handy when writing new OpenCL kernels

tx_element_array_descriptor_a
_____________________________

Introduction
~~~~~~~~~~~~

the tx_element_array_descriptor_a_ data structure is intended to be a compact description of a set of radiators to be placed in the world for purpose of energising the acoustic field.

It is used primarily in the :class:`handybeam.tx_array.TxArray`, and for benefit of :class:`handybeam.solver.Solver`

From python's point of view, the data set is a numpy array of size :code:`tx_count` x 16 and type :code:`numpy.float32`

.. code-block:: python

    tx_element_array_descriptor_a = np.zeros((tx_count, 16), np.float32)

The 1st dimension corresponds to each new transducer; the 2nd dimension are the fields.

The data could be shortly described as :code:`xyznnnddddap____` where:

* xyz - xyz location of the radiator. naturalily :code:`(0,0,0)` is the origin.
* nnn - xyz vector of *normal* of the radiator. set to :code:`(0,0,1)` for z-oriented
* dddd - 4 components for the transducer directivity model. set to :code:`(0,1,0,0)` for omini-directional behaviour.
* a - the amplitude ratio setting. By convention, goes from zero to unity, but negative and large values will also work. it is called "ratio" because the directivity model should contain the absolute scaling of the transducer output capability.
* p - phase setting in radians.
* :code:`____` - 4x NaNs. They are these mostly for data chunk alignment, but could also be used in the future for something.


The fields are best described by looking at the source of the :meth:`handybeam.tx_array.TxArray.generate_tx_array_element` below:


Usage in the source code
~~~~~~~~~~~~~~~~~~~~~~~~

Python side
^^^^^^^^^^^

in :code:`tx_array.py` :

.. code-block:: python

    tx_single_element_descriptor = np.zeros((1, 16), dtype=np.float32)
    tx_single_element_descriptor.fill(np.float32(np.NaN))
    tx_single_element_descriptor[0, 0] = np.float32(x)
    tx_single_element_descriptor[0, 1] = np.float32(y)
    tx_single_element_descriptor[0, 2] = np.float32(z)
    tx_single_element_descriptor[0, 3] = np.float32(xnormal)
    tx_single_element_descriptor[0, 4] = np.float32(ynormal)
    tx_single_element_descriptor[0, 5] = np.float32(znormal)
    tx_single_element_descriptor[0, 6] = np.float32(directivity_phase_poly1_c1)
    tx_single_element_descriptor[0, 7] = np.float32(directivity_amplitude_poly2_c0)
    tx_single_element_descriptor[0, 8] = np.float32(directivity_amplitude_poly2_c1)
    tx_single_element_descriptor[0, 9] = np.float32(directivity_amplitude_poly2_c2)
    tx_single_element_descriptor[0, 10] = np.float32(amplitude_ratio_setting)
    tx_single_element_descriptor[0, 11] = np.float32(phase_setting)
    tx_single_element_descriptor[0, 12] = np.float32(np.NaN)
    tx_single_element_descriptor[0, 13] = np.float32(np.NaN)
    tx_single_element_descriptor[0, 14] = np.float32(np.NaN)
    tx_single_element_descriptor[0, 15] = np.float32(np.NaN)


.. note:: Historical note

    In the version 1.0, the kernel launcher assembles the :code:`tx_element_array_descriptor_a`
    from :class:`handybeam.tx_element.TxElement`. Note that this approach is due to be refactored:
    :code:`tx_element_array_descriptor_a` will be a property of a :code:`handybeam.tx_array.TxArray` instance,
    and that will become the primary authority. The :code:`handybeam.tx_element.TxElement`
    will become a browser-editor-visualizer only for the data.





OpenCL side
^^^^^^^^^^^

in :code:`_handybeam1kernel_clist.cl` :

.. code-block:: c

    unsigned int tx_pointer_base = 16 * tx_idx;
    float tx_x = cl_tx_element_array_descriptor_a[tx_pointer_base + 0];
    float tx_y = cl_tx_element_array_descriptor_a[tx_pointer_base + 1];
    float tx_z = cl_tx_element_array_descriptor_a[tx_pointer_base + 2];

    float tx_xnormal = cl_tx_element_array_descriptor_a[tx_pointer_base + 3];
    float tx_ynormal = cl_tx_element_array_descriptor_a[tx_pointer_base + 4];
    float tx_znormal = cl_tx_element_array_descriptor_a[tx_pointer_base + 5];

    float directivity_phase_poly1_c1 = cl_tx_element_array_descriptor_a[tx_pointer_base + 6];

    float directivity_amplitude_poly2_c0 = cl_tx_element_array_descriptor_a[tx_pointer_base + 7];
    float directivity_amplitude_poly2_c1 = cl_tx_element_array_descriptor_a[tx_pointer_base + 8];
    float directivity_amplitude_poly2_c2 = cl_tx_element_array_descriptor_a[tx_pointer_base + 9];

    float tx_amp = cl_tx_element_array_descriptor_a[tx_pointer_base + 10];
    float tx_phase = cl_tx_element_array_descriptor_a[tx_pointer_base + 11];


sampling_point_list
_____________________

:code:`sampling_point_list` is a list of coordinates of points/pixels/samples
for the :code:`handybeam.sampler_point_list.SamplerPointList` class, and the :code:`handybeam.propagators.cxyz.CXYZ` propagator.


Again, the usage is best described by implemented code:

in :code:`_handybeam1kernel_clist.cl` :

.. code-block:: c

    unsigned int sampling_point_pointer=3*sampling_point_idx;
    float pixel_x_coordinate=(float)sampling_point_list[sampling_point_pointer+0];
    float pixel_y_coordinate=(float)sampling_point_list[sampling_point_pointer+1];
    float pixel_z_coordinate=(float)sampling_point_list[sampling_point_pointer+2];

in :code:`clist.py` :

.. code-block:: python

    sampling_point_list=np.zeros((0, 3), dtype=np.float32),



p - the pressure field
______________________

The :code:`p` or :code:`field` data structure is used for storing complex-valued pressure field.

.. todo::

    refactor to make it clear that there can be several types of field information used:

    * complex-valued field - pressure at given frequency
    * real-valued field - real pressure in given time instant
    * real-valued field - absolute field intensity, could be in decibels re 20uPa


At this time, it is most relevant to note that the data is a flat list of values. For each 'pixel' of the field (as in :code:`sampling_point_list`) there is one value.

Note that currently, the value complex (two single-precision floats) but it could be made to be real or log-scale, half precision, or double precision later on.

from C/OpenCL/CUDA side it looks like this:

in :code:`_handybeam1kernel_clist` :


.. code-block:: c

    unsigned int output_pointer_base = 2 * sampling_point_idx ; // address in the buffer to use
    // The factor of (uint)2 comes from the fact that I need to store both imaginary and real parts.
    cl_field[output_pointer_base+0] = pressure_re;  // store real-part of the complex pressure value
    cl_field[output_pointer_base+1] = pressure_im;  // store imaginary-part of the complex pressure value


from the python side, it looks like this:

in :code:`clist.py` :

.. code-block:: python

    sampling_point_count = sampling_point_list.shape[0]
    field = np.zeros((sampling_point_count), dtype=np.complex64)



.. include:: footer_licence_note.rst