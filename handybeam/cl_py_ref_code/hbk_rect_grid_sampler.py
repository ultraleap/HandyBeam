##  This is python reference code for the opencl kernel _hbk_rect_grid_sampler.

def hbk_rect_grid_sampler_ref( 
        
    x_lim,
    y_lim,
    delta,
    x0,
    y0,
    z0,
    v1x,
    v1y,
    v1z,
    v2x,
    v2y,
    v2z
    
    ):

    '''
    ---------------------------------------------
    hbk_rect_grid_sampler_ref( x_lim,y_lim,delta,x0,y0,z0,v1x,v1y,v1z,v2x,v2y,v2z)
    ---------------------------------------------
    This method generates a rectilinear grid of sampling points in a given orientation and
    with a given origin. 

    Parameters
    ------------
    
    x_lim : float / int 
            x limit of the rectilinear grid.
    y_lim : float / int
            y limit of the rectilinear grid.
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
            
    '''

    # Set limits of the rectilinear sampling grid coordinates. 
     
    N_x = x_lim * 2

    # Initialise list of sampling grid coordinates.
    x_points = []
    y_points = []
    z_points = []

    for idx_x in range(N_x):

        for idx_y in range(N_x):

            # Step a jump delta along the unit vectors defining the plane on which the sampling grid is defined.
            
            x_points.append(v1x*delta*(idx_x-x_lim) + v2x*delta*(idx_y-y_lim) + x0)
            y_points.append(v1y*delta*(idx_x-x_lim) + v2y*delta*(idx_y-y_lim) + y0)
            z_points.append(v1z*delta*(idx_x-x_lim) + v2z*delta*(idx_y-y_lim) + z0)

          
