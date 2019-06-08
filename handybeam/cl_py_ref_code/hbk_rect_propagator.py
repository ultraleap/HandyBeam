##  This is python reference code for the opencl kernel _hbk_rect_grid_sampler

## Imports

import numpy as np

## Global variables

tau = 6.283185307179586
medium_wavelength = 0.008575
recp_transducer_nan_size = medium_wavelength
medium_frequency = 40000
medium_wavenumber = tau / medium_wavelength

def hbk_rect_propagator_ref(   
        
    tx_array_element_descriptor,
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
    v2z,
    tx_count,    
    ):

    '''
    ---------------------------------------------
    hbk_rect_propagator_ref(tx_array_element_descriptor,x_lim,y_lim,delta,x0,y0,z0,v1x,v1y,v1z,v2x,v2y,v2z,tx_count)
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
    tx_array_element_decriptor : array
                    Numpy array containing information about each transducer
                   in the array. 
    sampling_point_list : list
                    List containing the coordinates of the sampling point.
    tx_count : int
                    Number of transducers in the array.
    '''

    # This first section is about generating the rectilinear sampling grid coordinates.
    # Please find more detail in hbk_rect_grid_sampler.py

    N_x = x_lim * 2

    x_points = []
    y_points = []
    z_points = []

    pressure_re = 0
    pressure_im = 0

    for idx_x in range(N_x):

        for idx_y in range(N_x):

            pixel_x_coordinate = v1x*delta*(idx_x-x_lim) + v2x*delta*(idx_y-y_lim) + x0
            pixel_y_coordinate = v1y*delta*(idx_x-x_lim) + v2y*delta*(idx_y-y_lim) + y0
            pixel_z_coordinate = v1z*delta*(idx_x-x_lim) + v2z*delta*(idx_y-y_lim) + z0

            # This first section is about propagating the acoustic field on to the
            # generated hexagonal sampling grid coordinates.
              
                # Initialise the real and imaginary components of the acoustic pressure.

            pressure_re = 0
            pressure_im = 0

            # Loop through the transducers.
            for tx_idx in range(0,tx_count):

                # Unpack the tx_array_element_descriptor data structure to obtain
                # necessary information about the transducers.

                # Transducer position coordinates.

                tx_x = tx_array_element_descriptor[tx_idx,0]
                tx_y = tx_array_element_descriptor[tx_idx,1]
                tx_z = tx_array_element_descriptor[tx_idx,2]

                # Vectors normal to the transducers.

                tx_xnormal = tx_array_element_descriptor[tx_idx,3]
                tx_ynormal = tx_array_element_descriptor[tx_idx,4]
                tx_znormal = tx_array_element_descriptor[tx_idx,5]

                # Coefficients describing the polynomial that models the amplitude and
                # phase directivity of the transducers.

                directivity_phase_poly1_c1 = tx_array_element_descriptor[tx_idx,6]
                directivity_amplitude_poly2_c0 = tx_array_element_descriptor[tx_idx,7]
                directivity_amplitude_poly2_c1 = tx_array_element_descriptor[tx_idx,8]
                directivity_amplitude_poly2_c2 = tx_array_element_descriptor[tx_idx,9]

                # Amplitude and phase of the transducers.

                tx_amp = tx_array_element_descriptor[tx_idx,10]
                tx_phase = tx_array_element_descriptor[tx_idx,11]

                # Calculate the distance from the sampling point to the transducer.

                delta_x = pixel_x_coordinate - tx_x
                delta_y = pixel_y_coordinate - tx_y
                delta_z = pixel_z_coordinate - tx_z

                # Find the reciprocal distance.

                recp_distance = 1/np.sqrt(delta_x*delta_x + delta_y*delta_y + delta_z*delta_z)

                # If the sampling point is inside a transducer then do not sample.

                if (recp_transducer_nan_size<recp_distance):

                    pressure_re = float('nan')
                    pressure_im = float('nan')

                # Find the cosine of the angle between the vector connected the transducer and the point
                # and the normal to the transducer.

                cosine_of_angle_to_normal =  ( delta_x*tx_xnormal + delta_y*tx_ynormal + delta_z * tx_znormal ) * recp_distance

                # If the sampling point is behind the transducer then do not sample.

                if (cosine_of_angle_to_normal<0.0):

                    pressure_re = float('nan')
                    pressure_im = float('nan')

                # Calculate the phase distance shift.

                phase_distance_shift =  tau  * medium_wavenumber * (1.0 / recp_distance)

                # Unwrap the phase distance shift.

                phase_distance_shift_wrapped = np.mod(phase_distance_shift, tau)

                # Calculate the amplitude drop due to distance.

                amplitude_distance_drop = recp_distance * medium_wavelength

                ca = 1.0 - cosine_of_angle_to_normal

                # Calculate the phase change due to phase directivity.

                directivity_phase = directivity_phase_poly1_c1 * ca

                # Calculate the amplitude drop due to amplitude directivity.
                ca2 = ca*ca
                directivity_amplitude_drop =                    \
                            directivity_amplitude_poly2_c0          \
                        + directivity_amplitude_poly2_c1 * ca     \
                        + directivity_amplitude_poly2_c2 * ca2

                # Find the amplitude and phase generated by this transducer at the given sampling point.

                rx_amplitude = tx_amp   * amplitude_distance_drop * directivity_amplitude_drop
                rx_phase     = tx_phase + phase_distance_shift_wrapped  + directivity_phase

                # Accumulate the results.

                pressure_re = pressure_re + np.cos(rx_phase) * rx_amplitude
                pressure_im = pressure_im + np.sin(rx_phase) * rx_amplitude

            # Add the sampling coordinate to the lists.

            x_points.append(pixel_x_coordinate)
            y_points.append(pixel_y_coordinate)
            z_points.append(pixel_z_coordinate)

            # Add the real and imaginary components of the complex acoustic pressure to the lists.

            pressure_re.append(pressure_re)
            pressure_im.append(pressure_im)
        

        x_points.append(pixel_x_coordinate)
        y_points.append(pixel_y_coordinate)
        z_points.append(pixel_z_coordinate)
        pressure_re.append(pressure_re)
        pressure_im.append(pressure_im)