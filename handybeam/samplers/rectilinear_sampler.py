"""
.. _rectilinear_sampler:

Module :mod:`handybeam.samplers.rectilinear_sampler`

File: :code:`rectilinear_sampler.py`

Holds the class :class:`handybeam.samplers.rectilinear_sampler.RectilinearSampler`

Original contributor: Salvador Catsis

"""
## Imports

import numpy as np
from pyquaternion import Quaternion
from handybeam .misc import copy_docstring
from handybeam .samplers.abstract_sampler import AbstractSampler
import handybeam .visualise

from handybeam.misc import handyround
from os import linesep
import warnings
warnings.warn('RectilinearSampler is deprecated, use CList sampler instead', DeprecationWarning)

## Global variables

tau = 2*np.pi

## Class


class RectilinearSampler(AbstractSampler):
    """ Takes the specification for a rectilinear sampling grid,
    creates a grid of points, and then enables sampling the acoustic field at these points.
    """

    def __init__(self,
                 parent=None,
                 normal_vector=np.array((0.0, 0.0, 1.0)),
                 parallel_vector=None,
                 up_vector=np.array((0.0, 1.0, 0.0)),
                 origin=np.array((0.0, 0.0, 200.0e-3)),
                 grid_spacing_per_wavelength=0.2,
                 grid_spacing_per_m=None,
                 grid_extent_around_origin_x=200e-3,
                 grid_extent_around_origin_y=200e-3,
                 local_work_size=(1, 1, 1),
                 align_grid_size_to_gpu=64
                 ):

        """Initialises an instance of the RectilinearSampler class.

        Parameters
        ----------

        parent : handybeam.world.World
                  This is an instance of the handybeam world class.
        normal_vector : numpy array
                  This is the vector normal to the desired sampling grid.
        up_vector : numpy array
                  This is a vector parallel to the desired sampling grid. It orients the grid in 3D space.
                  e.g. `np.array((0.0, 1.0, 0.0))`
        parallel_vector : numpy array
                  obsolete: use "up_vector"
                  e.g. `np.array((0.0, 1.0, 0.0))`
        origin : numpy array
                  This is a vector specifying the origin of the sampling grid.
        grid_spacing_per_wavelength : float
                  This specifies the grid spacing as a fraction of the medium wavelength.
        grid_spacing_per_m : float
                  This specifies the grid spacing in meters.
        grid_extent_around_origin_x : float
                  This specifies the distance between the origin of the sampling grid and the edge along the
                  x-axis.
        grid_extent_around_origin_y : float
                  This specifies the distance between the origin of the sampling grid and the edge along the
                  y-axis.
        local_work_size : tuple
                  This sets the local work size for the GPU, not recommended to change unless the user
                  has experience with OpenCL and pyopencl.
        align_grid_size_to_gpu : int
                  if set to true, the precise sampling density will be adjusted so that the count of pixels is a multiply of 256. This increases overall throughput of the GPU
        """
        warnings.warn('RectilinearSampler is deprecated, use CList sampler instead', DeprecationWarning)
        super(RectilinearSampler, self).__init__()

        self.parent = parent
        self.normal_vector = normal_vector
        if parallel_vector is not None:
            raise Exception('parallel_vector is obsolete, use "up_vector" instead')
        self.up_vector = up_vector
        self.vector_2 = None
        self.origin = origin
        self.local_work_size = local_work_size

        if grid_spacing_per_m is None:
            self.delta = grid_spacing_per_wavelength * self.parent.medium_wavelength
        else:
            self.delta = grid_spacing_per_m

        # print((2*grid_extent_around_origin_x)/self.delta)
        self.N_x = handyround((2*grid_extent_around_origin_x)/self.delta, align_grid_size_to_gpu)
        self.N_y = handyround((2*grid_extent_around_origin_y)/self.delta, align_grid_size_to_gpu)
        # print(self.N_x)

        self.x_lim = None
        self.y_lim = None
        self.vx1 = None
        self.vy1 = None
        self.vz1 = None
        self.x0 = None
        self.y0 = None
        self.z0 = None
        self.vx2 = None
        self.vy2 = None
        self.vz2 = None
        self.grid_extent_around_origin_x =  grid_extent_around_origin_x
        self.grid_extent_around_origin_y = grid_extent_around_origin_y

        self.transducer_count = self.parent.tx_array.element_count

        self.pressure_field = np.zeros((self.N_x, self.N_y, 1), dtype=np.complex)
        self.coordinates = np.zeros((self.N_x, self.N_y, 3), dtype=np.float32)
        self.coefficient_matrix = np.zeros((256, 256), dtype=np.complex)
        self.generate_propagation_parameters()
        self.find_rect_grid_area()
        # create u,v coordinates around the x0,y0,z0
        self.coordinates_u = np.linspace(-self.grid_extent_around_origin_x/2,self.grid_extent_around_origin_x/2, self.N_x)
        self.coordinates_v = np.linspace(-self.grid_extent_around_origin_y / 2, self.grid_extent_around_origin_y/2, self.N_y)

    @property
    def extent(self):
        """ extent as for use in imshow(extent=this.extent)

        :return: a tuple suitable to give to imshow
        """
        return (
            -self.grid_extent_around_origin_x,
            self.grid_extent_around_origin_x,
            -self.grid_extent_around_origin_y,
            self.grid_extent_around_origin_y)

    def find_rect_grid_area(self):

        '''This method finds the area of the requested sampling grid.

        '''

        self.area = (self.N_x - 1) * (self.N_y - 1) * np.power(self.delta,2)

    def generate_propagation_parameters(self):

        '''This method finds the parameters to pass to the opencl kernel to correctly
        define the sampling grid. 

        '''
        # Find the unit normal vector to the plane. 

        unit_normal = (1/np.linalg.norm(self.normal_vector))*self.normal_vector
            
        # Define the quaternion required to rotate the parallel vector by an angle of pi/2. 

        quaternion = Quaternion(axis=[unit_normal[0], unit_normal[1], unit_normal[2]], angle = tau/4)

        # Rotate the up vector to get a new vector which is perpendicular to the normal and the parallel vector.

        self.vector_2 = quaternion.rotate(self.up_vector)
            
        # Find the norm of these vectors.

        up_vector_norm = np.linalg.norm(self.up_vector)
        vector_2_norm = np.linalg.norm(self.vector_2)
            
        # Find the unit vectors.

        unit_up_vector = (1/up_vector_norm)*self.up_vector

        unit_vector_2 = (1/vector_2_norm)*self.vector_2

        # Compute the angle between these vectors to check that is equal to pi/2.

        angle_1 = int(np.round(np.rad2deg(np.arccos(np.dot(unit_up_vector, unit_vector_2))), 1))

        # Compute the angle between each of these vectors and the normal to ensure that they parameterise the plane perpendicular to the noromal.

        angle_2 = int(np.round(np.rad2deg(np.arccos( np.dot(self.up_vector, self.normal_vector) / (up_vector_norm*vector_2_norm))), 1))
        angle_3 = int(np.round(np.rad2deg(np.arccos( np.dot(self.vector_2, self.normal_vector) / (up_vector_norm*vector_2_norm))), 1))

        # Throw error if they are not.

        if np.bitwise_or(angle_1 != 90,  np.bitwise_or(int(angle_2) != 90, int(angle_3) != 90)):

            raise Exception('Could not parameterise the requested sampling grid correctly!')

        self.x_lim = np.float32(self.N_x/2) 
        self.y_lim = np.float32(self.N_y/2) 
        self.vx1 = np.float32(self.up_vector[0])
        self.vy1 = np.float32(self.up_vector[1])
        self.vz1 = np.float32(self.up_vector[2])
        self.x0 = np.float32(self.origin[0])
        self.y0 = np.float32(self.origin[1])
        self.z0 = np.float32(self.origin[2])
        self.vx2 = np.float32(np.round(self.vector_2[0], 4))
        self.vy2 = np.float32(np.round(self.vector_2[1], 4))
        self.vz2 = np.float32(np.round(self.vector_2[2], 4))

    def propagate(self,
                  print_performance_feedback=False,
                  local_work_size=None):
        """Calls the rect_propagator to propagate the acoustic field to
        the desired sampling points.

        Parameters
        ----------

        print_performance_feedback : boolean
                Boolean value determining whether or not to output the GPU performance.
        local_work_size : tuple or None
                Tuple e.g. (1,1,1) - set to use that work unit size.
                Note that correct setting require in-depth understanding of the GPU properties. Do not change away from (1,1,1) unless you know what You are doing.

        """

        if local_work_size is None:
            local_work_size = self.local_work_size

        kernel_output = self.parent.propagator.rect_propagator(    
                                                            self.parent.tx_array,
                                                            self.N_x,
                                                            self.N_y,
                                                            self.delta,
                                                            self.x0, self.y0, self.z0,
                                                            self.vx1, self.vy1, self.vz1,
                                                            self.vx2, self.vy2, self.vz2,
                                                            local_work_size=local_work_size,
                                                            print_performance_feedback=print_performance_feedback
                                                        )
                         
        self.coordinates = kernel_output[:, :, 0:3]
        self.pressure_field = kernel_output[:, :, 3] + np.complex(0, 1)*kernel_output[:, :, 4]

    def __repr__(self):
        """ links to self.__str__()"""
        return self.__str__()

    def __str__(self):
        return "RectilinearSampler: {}x{} points, spacing {:0.5f}mm".format(self.N_x,self.N_y,self.delta*1e3)
   