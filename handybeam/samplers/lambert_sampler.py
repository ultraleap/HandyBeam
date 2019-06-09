"""
.. _lambert_sampler:

Module :mod:`handybeam.samplers.lambert_sampler`

File: :code:`lambert_sampler.py`

Holds the class :class:`handybeam.samplers.lambert_sampler.LambertSampler`

Original contributor: Salvador Catsis

"""

## Imports

import numpy as np
from handybeam.misc import copy_docstring
from handybeam.samplers.abstract_sampler import AbstractSampler
import handybeam.visualise
## Global variables

tau = 2*np.pi
root_2 = 1.4142135623730951


## Class

class LambertSampler(AbstractSampler):

    '''This is the lambert sampling grid class. It takes the specification for a
    lambert sampling array and then samples the acoustic field at these points.

    '''

    def __init__(self,
                parent = None,
                origin = np.array((0,0,0)),
                required_resolution = 12e-3, 
                radius = 50e-3,
                local_work_size = (1,1,1)):


        '''This method intialises an instance of the LambertSampler class.

        Parameters
        ----------

        parent : handybeam.world.World
                This is an instance of the handybeam world class. 
        origin : numpy array
                This is a vector specifying the origin of the sampling grid.
        required_resolution : float 
                This specifies the resolution of the lambert sampling grid, it changes
                the number of sampling points.
        radius : float
                This specifies radius of the hemispherical sampling grid. 
        local_work_size : tuple
                This sets the local work size for the GPU, not recommended to change unless the user
                has experience with OpenCL and pyopencl.
        '''

        super(LambertSampler,self).__init__()

        self.parent = parent
        self.origin = origin
        self.radius = np.float32(radius)
        self.local_work_size = local_work_size
        
        self.no_points_required = np.ceil((tau*radius)/required_resolution)
        self.density = (2*root_2) / self.no_points_required
        self.N = len(np.arange(-1,1,self.density))
        
        self.x0 = origin[0]
        self.y0 = origin[1]
        self.z0 = origin[2]
        
        self.normal_vector = np.array((0,0,-1))
        self.parallel_vector = np.array((0,1,0))
        self.vector_2 = np.array((1,0,0))

        self.pressure_field = np.zeros((self.N,self.N,1),dtype = np.complex)
        self.coordinates = np.zeros((self.N,self.N,3),dtype = np.float32)

    def propagate(self,print_performance_feedback = False):

        '''This method calls the lamb_propagator to propagate the acoustic field to
        the desired sampling points.

        Parameters
        ----------

        print_performance_feedback : boolean
                Boolean value determining whether or not to output the GPU performance.

        '''

        kernel_output = self.parent.propagator.lamb_propagator(
                                                            self.parent.tx_array,
                                                            self.radius,
                                                            self.N,
                                                            self.density,
                                                            self.x0,self.y0,self.z0,
                                                            local_work_size = self.local_work_size,
                                                            print_performance_feedback = print_performance_feedback
                                                        )
                                                        
        self.pressure_field= kernel_output[:,:,3] + np.complex(0,1) * kernel_output[:,:,4]
        self.coordinates = kernel_output[:,:,0:4]
 