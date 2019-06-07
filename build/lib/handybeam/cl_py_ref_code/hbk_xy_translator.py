##  This is python reference code for the opencl kernel _hbk_xy_translator

## Global variables

tau = 6.283185307179586
wavenumber = 732.7329916341719

def hbk_xy_translator_ref(
    
    tx_array_element_descriptor,
    x_translate,
    y_translate,
    plane_height_recp
    
    ):

    '''
    ---------------------------------------------
    hbk_xy_translator_ref(tx_array_element_descriptor, x_translate,y_translate,plane_height_recp)
    ---------------------------------------------
    This method translates a focal point, set of focal points or a haptic surface by a specified amount
    'x_translate' in the x-axis and 'y_translate' in the y-axis using beam steering.

    Parameters
    ----------
    tx_array_element_decriptor : array
                Numpy array containing information about each transducer
                in the array. 
    x_translate: float
                Distance in m to translate the focal point, set of focal points or haptic surface by in the x-axis.
    y_translate: float 
                Distance in m to translate the focal point, set of focal points or haptic surface by in the y-axis.
    plane_height: float
                Distance from z = 0 to the xy-plane where the focal points are intended to be. 
    
    '''
 
    # Loop through the transducers.

    for tx_idx in range(len(tx_array_element_descriptor)):

        # Get the x,y coordinate of the transducer.

        tx_x = tx_array_element_descriptor[tx_idx,0]
        tx_y = tx_array_element_descriptor[tx_idx,1]
    
        # Get the phase of the transducer. 

        tx_phase = tx_array_element_descriptor[tx_idx,11]
        
        # Determine the angle to steer with in x-axis (using approx for arctan).

        alpha_x = x_translate * plane_height_recp

        # Determine the angle to steer with in y-axis (using approx for arctan).
            
        alpha_y = y_translate * plane_height_recp

        # Determine the sin of the angle to steer with in x-axis (using approx for sin).

        beta_x = alpha_x

        # Determine the sin of the angle to steer with in y-axis (using approx for sin).

        beta_y = alpha_y

        # Determine the required change in phase to shift the focal point. 

        delta_phase_x = wavenumber * beta_x * tx_x

        delta_phase_y = wavenumber * beta_y * tx_y
           
        # Store this change of phase in the tx_array_element_descriptor data structure.
        tx_array_element_descriptor[tx_idx,11] = tx_phase + delta_phase_x + delta_phase_y
           
        