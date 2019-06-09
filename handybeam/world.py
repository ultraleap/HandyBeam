"""
.. _world:

===============================
module :code:`handybeam.world`
===============================

Describes the virtual world, in which the acoustic propagation occurs.

Holds a description of things like:

* Environment properties, like wave velocity, temperature, e.t.c.

    * Note, over time i might extend this with pressure and temperature

* The list of samplers (objects that describe how to sample the acoustic field)

* The transmitter array (object that describes the Tx Array)

* The propagator (object that holds the propagation engine, and compute resources)

"""
 

## Imports

import numpy as np
import handybeam.bugcatcher
import handybeam.tx_array_library
import handybeam.opencl_wrappers.propagator_wrappers

## Global variables 

__license__ = "Apache 2.0"
tau = 2*np.pi

## Class

class World():
    """ Root descriptor of the simulated universe

        Contains what is needed to quickly serve typical use cases for HandyBeam

        Example use:

        .. code-block:: python

            world=handybeam.world.World()

        .

        .. todo:: (?)field_yz=world.add_field(handybeam.yz_field.YZ_field())

    """

    def __init__(self, frequency=40000, sound_velocity=343,use_device=0,use_platform=0):
        """ instance constructor.

                Upon creation, add an example array, initialize the propagator, and have no samplers.

                the user must add a field sampler.

                At one point, I tried to make it to auto-give itself a default sampler,
                but that resulted in circular references. Possibly I can find a workaround to that later on.
        """

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

            sampler_yz = world.add_sampler(handybeam.samplers.RectilinearSampler())

        .. TODO:: check if the above is correct -- samplers have changed!

        :param sampler: the sampler instance to add
        :return: handle to the new sampler instance

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


