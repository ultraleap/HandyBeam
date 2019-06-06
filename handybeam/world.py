"""
.. _world:

===================
world
===================

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

__license__ = "CC BY-NC-SA 4.0"
tau = 2*np.pi

## Class

class World():

    '''
    ---------------------------------------------
    World
    ---------------------------------------------
    
    DESCRIPTION HERE

    '''

    def __init__(self,frequency = 40000,sound_velocity = 343):

        '''
        
        ---------------------------------------------
        __init__(frequency,sound_velocity)
        ---------------------------------------------

        This method initialises an instance of the world class.

        Parameters
        ----------

        frequency : int / float
                DESCRIPTION HERE
        sound_velocity : int / float
                DESCRIPTION HERE
  
        '''

        self.sound_velocity = sound_velocity
        self.frequency = frequency
        self.medium_wavelength =  np.float32(self.sound_velocity / self.frequency)
        self.medium_wavenumber = 1 / self.medium_wavelength
        self.samplers = []
        self.tx_array = handybeam.tx_array_library.USX(parent = self)
        self.propagator =  handybeam.opencl_wrappers.propagator_wrappers.Propagator(parent=self)

    def add_sampler(self,sampler = None):

        '''
        ---------------------------------------------
        add_sampler(self,sampler)
        ---------------------------------------------
        
        DESCRIPTION HERE

        Parameters
        ----------

        sampler : handybeam sampler
                DESCRIPTION HERE
  
        '''
        if sampler is None:

            raise RuntimeError('No sampling grid provided.')
        
        # Add the new field at the end of the list

        self.samplers.append(sampler)

        # Set parent of sampling grid.

        self.samplers[-1].set_parent(self)

        # Give reference back to the caller.

        return self.samplers[-1]

    def propagate(self,print_performance_feedback = False):
        
        '''
        ---------------------------------------------
        propagate(self,print_performance_feedback)
        ---------------------------------------------
        
        DESCRIPTION HERE

        Parameters
        ----------

        print_performance_feedback : Boolean
                DESCRIPTION HERE
  
        '''
        # This function asks all sampling grids to propagate.

        for sampler in self.samplers:
            sampler.propagate(print_performance_feedback=print_performance_feedback) 

    def visualise(self, colour_scale=None):
       
        '''
        ---------------------------------------------
        visualise(self,colour_scale)
        ---------------------------------------------
        
        DESCRIPTION HERE

        Parameters
        ----------

        colour_scale : NOT SURE
                DESCRIPTION HERE
  
        '''
        
        for sampler in self.samplers:
            sampler.visualise(colour_scale=colour_scale)
