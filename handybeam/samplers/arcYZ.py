"""arcYZ.py contains arcYZ() sampler
this sampler inherits from CList sampler and contains a shortcut to create an arc above the array

usage: arc_sampler=handybeam.samplers.arcYZ(world=world,radius=radius)

where:
    world: instance of the world. In particular, provides wavelength. Default sampling is 3 samples per wavelength
    radius: radius of the arc, in meters.

"""
import numpy as np
from handybeam.samplers.clist_sampler import ClistSampler


class arcYZ(ClistSampler):

    def __init__(self,
                 world=None,
                 radius=100e-3,
                 points_per_wavelength=3,
                 local_work_size=(128, 1, 1)):

        '''This method intialises an instance of the arcYZ class.

                Parameters
                ----------

                parent : handybeam_core.world.World
                        This is an instance of the handybeam world class.
                local_work_size : tuple
                        This sets the local work size for the GPU, not recommended to change unless the user
                        has experience with OpenCL and pyopencl.

        '''

        super(arcYZ, self).__init__(parent=world, local_work_size=local_work_size)

        self.coordinates = np.zeros((0, 3), dtype=np.float32)
        wavelength = self.world.medium_wavelength

        # create a sampling line, semi-circle around the array, to sample the field there
        tau = 2 * np.pi
        # store input parameters values
        self.radius = radius
        self.points_per_wavelength = points_per_wavelength

        # calculate effects
        self.arc_length = tau * self.radius
        self.point_count = np.ceil(points_per_wavelength * self.arc_length / wavelength)
        self.distance_between_points = self.arc_length/self.point_count

        self.sampler_angles = np.linspace(-tau / 4, tau / 4, num=self.point_count, endpoint=True)

        self.ys = np.sin(self.sampler_angles) * radius
        self.zs = np.cos(self.sampler_angles) * radius
        self.xs = np.zeros(self.ys.shape)
        self.add_sampling_points(self.xs, self.ys, self.zs)

    def __str__(self):
        txt = super(arcYZ, self).__str__()
        txt1 = f'{txt1} - arc shape, radius = {self.radius*1e3:0.1f}mm'
        return txt1

    def __repr__(self):
        """links to self.__str__()"""
        return self.__str__()

