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

the :code:`tx_element_array_descriptor_a` data structure is intended to be a compact description of a set of radiators to be placed in the world for purpose of energising the acoustic field.



From python's point of view, the data set is a numpy array of size :code:`tx_count` x 16 and type :code:`numpy.float32`

.. code-block:: python

    tx_element_array_descriptor_a = np.zeros((tx_count, 16), np.float32)

The 1st dimension corresponds to each new transducer; the 2nd dimension are the fields.

The fields are best described by looking at the source of the :code:`handybeam.tx_element.TxElement().v1_property_vector` below:


Usage in the source code
~~~~~~~~~~~~~~~~~~~~~~~~

Python side
^^^^^^^^^^^

in :code:`tx_element.py` :

.. code-block:: python

    @property
    def v1_property_vector(self):
        """ get/set the transducer property vector formatted for the high performance propagator

        :return: a ((1, 16), dtype=np.float) numpy array with values filled in.
        """
        q = np.zeros((1, 16), dtype=np.float)
        q.fill(np.NaN)
        q[0, 0] = self.x
        q[0, 1] = self.y
        q[0, 2] = self.z
        q[0, 3] = self.xnormal
        q[0, 4] = self.ynormal
        q[0, 5] = self.znormal
        q[0, 6] = self.directivity_phase_poly1_c1
        q[0, 7] = self.directivity_amplitude_poly2_c0
        q[0, 8] = self.directivity_amplitude_poly2_c1
        q[0, 9] = self.directivity_amplitude_poly2_c2
        q[0, 10] = self.amplitude_ratio_setting
        q[0, 11] = self.phase_setting
        # q[12]=np.NaN
        # q[13]=np.NaN
        # q[14]=np.NaN
        # q[15]=np.NaN
        return q


In the version 1.0, the kernel launcher assembles the :code:`tx_element_array_descriptor_a`
from :class:`handybeam.tx_element.TxElement`. Note that this approach is due to be refactored:
:code:`tx_element_array_descriptor_a` will be a property of a :code:`handybeam.tx_array.TxArray` instance,
and that will become the primary authority. The :code:`handybeam.tx_element.TxElement`
will become a browser-editor-visualizer only for the data.



in :code:`clist.py` :


.. code-block:: python

    tx_count = len(tx_element_list)
    tx_element_array_descriptor_a = np.zeros((tx_count, 16), np.float32)
    # marshall the pythonic descriptor into CL-ic descriptor
    # format - R1 format of : [x,y,z,xnormal,ynormal,znormal,dpc1,dac0,dac1,dac2,amp,phase,NaN,NaN,NaN,NaN] * TxCount
    for tx_idx in range(tx_count):
        element_descriptor = tx_element_list[tx_idx].v1_property_vector
        tx_element_array_descriptor_a[tx_idx, :] = element_descriptor


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