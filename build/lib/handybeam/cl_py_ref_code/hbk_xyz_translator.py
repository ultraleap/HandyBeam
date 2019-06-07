##  This is python reference code for the opencl kernel _hbk_xyz_translator

## Imports

import numpy as np

## Global variables

tau = 6.283185307179586
wavenumber = 732.7329916341719

def hbk_xyz_translator_ref(
        
    tx_array_element_descriptor, 
    focal_x_coordinate,
    focal_y_coordinate,
    focal_z_coordinate,
    x_translate,
    y_translate,
    z_translate
    
    ):

    '''
    ---------------------------------------------
    hbk_xyz_translator_ref(tx_array_element_descriptor, focal_x_coordinate,focal_y_coordinate,focal_z_coordinate,x_translate,y_translate,z_translate)    
    ---------------------------------------------
    
    This method translates a focal point, set of focal points or a haptic surface by a specified amount
    'x_translate' in the x-axis, 'y_translate' in the y-axis and 'z_translate' 
    in the z-axis.

    Parameters
    ----------
    tx_array_element_decriptor : array
                Numpy array containing information about each transducer
                in the array. 
    focal_x_coordinate : float
            x-coordinate of the desired focal point.
    focal_y_coordinate : float 
            y-coordinate of the desired focal point.
    focal_z_coordinate : float 
            z-coordinate of the desired focal point.
    x_translate: float
                Distance in m to translate the focal point, set of focal points or haptic surface by in the x-axis.
    y_translate: float 
                Distance in m to translate the focal point, set of focal points or haptic surface by in the y-axis.
    z_translate: float 
                Distance in m to translate the focal point, set of focal points or haptic surface by in the y-axis.
    
    '''
    
    # Loop through the transducers 

    for tx_idx in range(len(tx_array_element_descriptor)):

        tx_x = tx_array_element_descriptor[tx_idx,0]
        tx_y = tx_array_element_descriptor[tx_idx,1]
        tx_z = tx_array_element_descriptor[tx_idx,2]

        tx_phase = tx_array_element_descriptor[tx_idx,11]

        # Find distance from transducer to focal point.

        delta_x = focal_x_coordinate - tx_x
        delta_y = focal_y_coordinate - tx_y
        delta_z = focal_z_coordinate - tx_z

        recp_original_distance = 1/np.sqrt(delta_x * delta_x + delta_y * delta_y + delta_z * delta_z)

        # Calculate phase change required to shift the focal point to 
        # desired location. 

        delta_phase = - wavenumber * (delta_x * x_translate + delta_y * y_translate + delta_z * z_translate) * recp_original_distance

        # Store the result in the tx_array_element_descriptor data structure.

        tx_array_element_descriptor[tx_idx,11] = tx_phase + delta_phase 
           