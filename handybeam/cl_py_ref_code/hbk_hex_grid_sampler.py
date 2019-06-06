##  This is python reference code for the opencl kernel _hbk_hex_grid_sampler.

## Imports

import numpy as np

def hbk_hex_grid_sampler_ref( 

    side_length,
    delta,
    x0,
    y0,
    z0,
    v1x,
    v1y,
    v1z,
    v2x,v2y,v2z,
    lower_limit,
    upper_limit
    
    ):


    '''
    ---------------------------------------------
    hbk_hex_grid_sampler_ref( side_length,delta,x0,y0,z0,v1x,v1y,v1z,v2x,v2y,v2z,lower_limit,upper_limit)
    ---------------------------------------------
    This method generates a hexagonal grid of sampling points in a given orientation and
    with a given origin. 

    Parameters
    ----------

    side_length : float / int
            Side length of the hexagonal grid.
    delta : float
            Distance between sampling points in the grid.
    x0 : float
            x-coordinate of the origin of the grid.
    y0 : float
            y-coordinate of the origin of the grid.
    z0 : float
            z-coordinate of the origin of the grid.
    v1x : float
            x-component of the unit vector parallel to the grid.
    v1y : float
            y-component of the unit vector parallel to the grid.
    v1z : float
            z-component of the unit vector parallel to the grid.
    v2x : float
            x-component of the unit vector parallel to the grid 
            and perpendicular to the unit vector specfied by (v1x,v1y,v1z).
    v2y : float 
            y-component of the unit vector parallel to the grid
            and perpendicular to the unit vector specfied by (v1x,v1y,v1z).
    v2z : float 
            z-component of the unit vector parallel to the grid
            and perpendicular to the unit vector specfied by (v1x,v1y,v1z).
    lower_limit : float / int
            This is a variable used to generate the hexagonal grid.
    uppwer_limit : float / int
            This is a variable used to generate the hexagonal grid. 

    '''

    # This method first creates a rhombus and then cuts out the required regions
    # to generate a hexagonal sampling grid.

    # Set the grid length of the rhombus.

    grid_length = np.int32(2*side_length - 1)

    # Initialise lists for the sampling grid coordinates. 

    x_points = []
    y_points = []
    z_points = []

    # Loop through the rhombus grid.

    for idx_x in range(0,grid_length):
        
        idx_x += 1

        for idx_y in range(0,grid_length):

            idx_y += 1

            index_sum = idx_x + idx_y 

            # Remove certain points from the rhombus to create hexagonal sampling grid.
            lower_compare = index_sum < lower_limit
            upper_compare = index_sum > upper_limit

            if np.bitwise_or(lower_compare,upper_compare):

                pass

            else:
                
                # Step a jump delta along the unit vectors defining the plane on which the sampling grid is defined.
                
                x_points.append(v1x*delta*(idx_x-side_length) + v2x*delta*(idx_y-side_length) + x0)
                y_points.append(v1y*delta*(idx_x-side_length) + v2y*delta*(idx_y-side_length) + y0)
                z_points.append(v1z*delta*(idx_x-side_length) + v2z*delta*(idx_y-side_length) + z0)


