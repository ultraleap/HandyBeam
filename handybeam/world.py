"""
.. _world:


.. ===============================
   module :mod:`handybeam.world`
   ===============================

Describes the virtual world, in which the acoustic propagation occurs.

Holds a description of things like:

* Environment properties, like wave velocity, temperature, e.t.c.

    * Note, over time i might extend this with pressure and temperature

* The list of samplers (objects that describe how to sample the acoustic field)

* The transmitter array (object that describes the Tx Array)

* The propagator (object that holds the propagation engine, and compute resources)

.. TODO::

    Replace all "if print feedback" with a logging module.
    Time to grow up.
    See `this tutorial <https://docs.python.org/3/howto/logging-cookbook.html>`_

.. TODO::

    remove .creation_text and depreciate RememberInstanceCreationInfo altogether.

"""
 

# # Imports

import numpy as np
import handybeam.bugcatcher
import handybeam.tx_array_library
import handybeam.opencl_wrappers.propagator_wrappers
from handybeam.remember_instance_creation_info import RememberInstanceCreationInfo
from os import linesep
# # Global variables

__license__ = "Apache 2.0"

tau = 2*np.pi
"""the tau constant. It really should get implemented into numpy."""

# # Class


class World(RememberInstanceCreationInfo):
    """ Root elements of the simulated universe

    Contains what is needed to quickly serve typical use cases for HandyBeam.

    Example use:

    .. code-block:: python

        world=handybeam.world.World()
        world.tx_array = handybeam.tx_array_library.rectilinear(parent = world)
        rectilinear_sampler = world.add_sampler(handybeam.samplers.rectilinear_sampler.RectilinearSampler(parent=world))

    .. note::

        Note that OpenCL kernels are compiled with sound velocity and frequency as constants. This is for performance purposes.


    Attributes:
        sound_velocity (numpy.float): Sound velocity. Set only via creating a new world.
        frequency (numpy.float): fundamental frequency of operation for the transmitter array. Set only via creating a new world.
        medium_wavelength (numpy.float): computed wavelength for this world. constant.
        medium_wavenumber (numpy.float): computed wavenumber for this world. constant.
        samplers (list[handybeam.samplers.*]): list of the field sampler objects.
        tx_array (handybeam.tx_array.TxArray): the transmitter array object.
        propagator (handybeam.opencl_wrappers.propagator_wrappers.Propagator): the object that holds the OpenCL code for calculating (propagating) the acoustic field.
        platform (int): OpenCL platform ID
        device (int): OpenCL device ID


    """

    def __init__(self, frequency=40000, sound_velocity=343, use_device=0, use_platform=0):
        """ instance constructor.

        Upon creation, add an example array, initialize the propagator, and have no samplers.

        the user must add a field sampler.

        At one point, I tried to make it to auto-give itself a default sampler,
        but that resulted in circular references. Possibly I can find a workaround to that later on.
        """
        super().__init__()
        self.sound_velocity = sound_velocity
        self.frequency = frequency
        self.medium_wavelength = np.float32(self.sound_velocity / self.frequency)
        self.medium_wavenumber = 1 / self.medium_wavelength
        self.samplers = []
        self.device = use_device
        self.platform = use_platform
        self.tx_array = handybeam.tx_array_library.USX(parent=self)
        self.propagator = handybeam.opencl_wrappers.propagator_wrappers.Propagator(parent=self,use_device = self.device, use_platform = self.platform)

    def add_sampler(self, sampler=None):
        """ Adds a new field sampler to the world

        .. code-block:: python

            rectilinear_sampler = world.add_sampler(handybeam.samplers.rectilinear_sampler.RectilinearSampler(parent=world))

        :param handybeam.samplers.* sampler:
            the sampler instance to add

        :return:
            handle to the new sampler instance

        """
        if sampler is None:

            raise RuntimeError('No sampling grid provided.')
        
        # Add the new field at the end of the list

        self.samplers.append(sampler)

        # Set parent of sampling grid.

        self.samplers[-1].set_parent(self)

        # Give reference back to the caller.

        return self.samplers[-1]

    def propagate(self, print_performance_feedback=False):
        """ Shortcut: Ask all the field samplers to execute it's propagator

        calls :code:`sampler.propagate(...)` of each sampler in the samplers list

        :param print_performance_feedback: if set to True, will print feedback to console
        :return: Nothing
        """

        for sampler in self.samplers:
            sampler.propagate(print_performance_feedback=print_performance_feedback) 

    def visualise(self, colour_scale=None):
        """ Shortcut: Ask all the field samplers to execute it's visualizer

        calls :code:`sampler.visualize(...)` for all samplers in the samplers list

        :param color_scale: if set, use that color scale. Usefull if you want all the plots to use a common color scale.
        """
        
        for sampler in self.samplers:
            sampler.visualise(colour_scale=colour_scale)

    def __str__(self):
        """ returns a short info about this world."""
        #txt = f"{self.creation_text}{linesep}handybeam.world.World() with "
        txt = f"handybeam.world.World() with "
        txt = f"{txt}sound velocity of {self.sound_velocity:0.1f}m/s, "
        txt = f"{txt}frequency {self.frequency * 1e-3:0.1f}kHz, "
        txt = f"{txt}medium_wavelength of {self.medium_wavelength * 1e3:0.3f}mm, "
        txt = f"{txt}wavenumber {self.medium_wavenumber:0.3f}, {len(self.samplers)} sampler(s). "
        for idx, sampler in enumerate(self.samplers):
            txt = f"{txt}Sampler {idx}: {str(sampler)}"

        if self.tx_array is not None:
            txt = f"{txt}{linesep}Tx array: {self.tx_array}"
        return txt

    def __repr__(self):
        """ links back to __str__()"""
        return self.__str__()

    def _repr_html_(self):
        """ builds a html version of the repr. Displays some basic properties about this world instance.

        :return: Jupyter/IPython uses this
        """
        txt = f"<em>handybeam.world.World</em> object with following properties, "
        txt = f"{txt}rendered for You in genuine html table form:"
        txt = f"{txt}<table><tr><th>Property</th><th>Value</th></tr>"
        txt = f"{txt}<tr><td>wave velocity</td><td>{self.sound_velocity:0.1f} m/s</td></tr>"
        txt = f"{txt}<tr><td>frequency</td><td>{self.frequency * 1e-3:0.1f} kHz</td></tr>"
        txt = f"{txt}<tr><td>wavelength</td><td>{self.medium_wavelength * 1e3:0.3f} mm</td></tr>"
        txt = f"{txt}<tr><td>wavenumber</td><td>{self.medium_wavenumber:0.3f} waves/m</td></tr>"
        txt = f"{txt}</table>"

        if self.tx_array is not None:
            txt = f"{txt}{linesep}<p><b>Tx array:</b> {self.tx_array}</p>"
        else:
            txt = f"{txt}{linesep}<p><b>No Tx Array attached. Attach at least one Tx Array.</b></p>"

        if not self.samplers:
            txt = f"{txt}<p><b>No field samplers. Attach at least one field sampler.</b></p>"

        for idx, sampler in enumerate(self.samplers):
            txt = f"{txt}<p><b>field sampler {idx}</b>: {str(sampler)}</p>"

        #  txt = txt+"<p>{}</p>".format(self.__str__())
        #  txt = txt + "<p></p><p>this is a html version of <em>self.__str__()</em>"
        return txt


