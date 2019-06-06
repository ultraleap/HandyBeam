##  This is python reference code for the opencl kernel _hbk_sf_solver

## Imports

import numpy as np

## Global variables

tau = 6.283185307179586
recp_wavelength = 116.61807580174928


def hbk_sf_solver_ref(
        
    tx_array_element_descriptor,
    focal_x_coordinate, 
    focal_y_coordinate,
    focal_z_coordinate
    
    ):

    '''
    ---------------------------------------------
    hbk_sf_solver_ref(tx_array_element_descriptor,focal_x_coordinate,focal_y_coordinate,focal_z_coordinate)
    ---------------------------------------------
    This method determines the activation coefficients required to produce
    a focal point at a given point in space. 

    Parameters
    -----------
    
    tx_array_element_decriptor : array
            Numpy array containing information about each transducer
            in the array. 
    focal_x_coordinate : float
            x-coordinate of the desired focal point.
    focal_y_coordinate : float 
            y-coordinate of the desired focal point.
    focal_z_coordinate : float 
            z-coordinate of the desired focal point.

    '''

    # Loop through the transducers.

    for tx_idx in range(len(tx_array_element_descriptor)):

        tx_x = tx_array_element_descriptor[tx_idx,0]
        tx_y = tx_array_element_descriptor[tx_idx,1]
        tx_z = tx_array_element_descriptor[tx_idx,2]
    
        # Find the distance from the transducer to the focal point. 

        delta_x = focal_x_coordinate - tx_x
        delta_y = focal_y_coordinate - tx_y
        delta_z = focal_z_coordinate - tx_z

        distance = np.sqrt(delta_x * delta_x + delta_y * delta_y + delta_z * delta_z)

        # Calculate the position along the wavelength.

        full_wavelengths = distance * recp_wavelength

        wrapped_wavelength =  - (np.mod(full_wavelengths, 1) * tau)

        # Store the calculated amplitude and pressure in the tx_array_element_descriptor
        # data structure.

        tx_array_element_descriptor[tx_idx,10] = 1
        tx_array_element_descriptor[tx_idx,11] = - wrapped_wavelength 

         
         