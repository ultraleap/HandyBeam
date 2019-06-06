##  This is python reference code for the opencl kernel _hbk_lamb_grid_sampler.

## Imports

import numpy as np

root_2 = 1.4142135623730951
tau = 6.283185307179586
medium_wavelength = 0.008575

def hbk_lamb_grid_sampler_ref(
        
    required_resolution,
    radius,
    N, 
    x0, 
    y0,
    z0
    
    ):
         
    '''
    ---------------------------------------------
    hbk_lamb_grid_sampler_ref( required_resolution,radius,N,x0,y0,z0)
    ---------------------------------------------
    This method generates a hemispherical grid of sampling points 
    using the lambert projection. 
    
    Parameters
    -----------

    required_resolution : float
            Distance between sampling points in the grid.
    x0 : float 
            x-coordinate of the origin of the grid.
    y0 : float 
            y-coordinate of the origin of the grid.
    z0 : float 
            z-coordinate of the origin of the grid.
    radius : float 
            Radius of the hemisphere defining the lambert projection. 
    
    '''

    no_points_required = np.ceil((tau*radius)/required_resolution)
    density = (2*root_2) / no_points_required
    N = len(np.arange(-1,1,density))

    # Initialise lists to store the sampling grid coordinates.

    x_points = []
    y_points = []
    z_points = []

    # Perform the lambert equi-area projection to generate hemispherical 
    # sampling points. 

    for idx_x in range(N):

        for idx_y in range(N):

            x_base = (-1 + density * idx_x ) * root_2
            y_base = (-1 + density * idx_y ) * root_2
            
            rho = np.sqrt(x_base * x_base + y_base * y_base)
            c = 2 * np.arcsin(0.5*rho)

            phi = np.arcsin(np.cos(c)) / rho
            l = np.arctan2( (x_base * np.sin(c)), -y_base*np.sin(c))
            cos_phi = np.cos(phi)

            lambert_x = radius * np.sin(phi)
            lambert_y = radius * np.cos(l) * cos_phi
            lambert_z = radius * np.sin(l) * cos_phi


            if lambert_z < 0:

                pixel_x_coordinate = float('nan')
                pixel_y_coordinate = float('nan')
                pixel_z_coordinate = float('nan')

            else:

                pixel_x_coordinate = lambert_x + x0
                pixel_y_coordinate = lambert_y + y0
                pixel_z_coordinate = lambert_z + z0
