"""cube.py contains Cube() sampler
This sampler inherits from CList sampler and contains a shortcut to create an cube (volume) of points.
This is usefull for volumetric (3D voxels) visualisations and analysis


"""
import numpy as np
from handybeam.samplers.clist_sampler import ClistSampler


class Cube(ClistSampler):
    def __init__(self,
                 world=None,
                 edgeXY=1000e-3,
                 edgeZ=500e-3,
                 samples_per_wavelength=3,
                 local_work_size=(128, 1, 1)):

        '''This method intialises an instance of the handybeam.samplers.cube.Cube class.

            usage: cube_sampler=handybeam.samplers.cube.Cube(world=world,edgeXY=1000e-3,edgeZ=500e-3,samples_per_wavelength=3)

            Parameters
            ----------

            world: instance of the world. In particular, provides wavelength. Default sampling is 3 samples per wavelength

            edgeXY: length of the edge of the cube along X or Y axes. Note that the extent is from -edgeXY/2 to +edgeXY/2

            edgeZ: length of the edge of the cube along Z axis.

            samples_per_wavelength: how many points to generate. The wavelength is taken from the world object.

            local_work_size : tuple
                    This sets the local work size for the GPU, not recommended to change unless the user
                    has experience with OpenCL and pyopencl.
        '''

        super(Cube, self).__init__(parent=world, local_work_size=local_work_size)

        self.coordinates = np.zeros((0, 3), dtype=np.float32)
        self.wavelength = self.world.medium_wavelength

        # create a sampling line, semi-circle around the array, to sample the field there
        tau = 2 * np.pi
        # store input parameters values
        self.edgeXY = edgeXY
        self.edgeZ = edgeZ
        self.samples_per_wavelength=samples_per_wavelength

        # calculate effects
        self.x0 = -self.edgeXY * 0.5
        self.y0 = -self.edgeXY * 0.5
        self.z0 = 0.0e-3
        self.xmax = self.edgeXY *0.5
        self.ymax = self.edgeXY * 0.5
        self.zmax = self.edgeZ

        self.no_points_xy = int(np.ceil(self.samples_per_wavelength*self.edgeXY/self.wavelength))
        self.no_points_z = int(np.ceil(self.samples_per_wavelength * self.edgeZ / self.wavelength))
        self.total_point_count = self.no_points_xy * self.no_points_xy * self.no_points_z

        # generate coordinate base
        self.xbase = np.linspace(self.x0, self.xmax, self.no_points_xy, endpoint=True)
        self.ybase = np.linspace(self.y0, self.ymax, self.no_points_xy, endpoint=True)
        self.zbase = np.linspace(self.z0, self.zmax, self.no_points_z, endpoint=True)

        self.dx = self.xbase[1] - self.xbase[0]
        self.dy = self.ybase[1] - self.ybase[0]
        self.dz = self.zbase[1] - self.zbase[0]

        self.x_mesh, self.y_mesh, self.z_mesh = np.meshgrid(self.xbase, self.ybase, self.zbase)
        self.x_list = self.x_mesh.ravel()
        self.y_list = self.y_mesh.ravel()
        self.z_list = self.z_mesh.ravel()

        self.add_sampling_points(self.x_list, self.y_list, self.z_list)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        txt = super(Cube, self).__str__()
        txt1 = f'{txt}. Cube with edgeXY={self.edgeXY * 1e3:0.1f}mm, edgeZ={self.edgeZ * 1e3:0.1f}mm'
        return txt1







