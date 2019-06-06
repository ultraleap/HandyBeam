## Imports

import numpy as np
from handybeam_core.tx_array import TxArray

## Global variables

__default_USX_element_spacing = 10.3e-3
__default_UHEV1_element_spacing = 10.47e-3
default_amplitude = 1.0
default_phase = 0.0
default_directivity_cos_power = 3.376
_tx_array_library__default_USX_element_spacing = 10.3e-3
_tx_array_library__default_UHEV1_element_spacing = 10.47e-3
_tx_array_library__default_amplitude = 1.0
_tx_array_library__default_phase = 0.0
_tx_array_library__default_directivity_cos_power = 3.376

## Functions

def single_element(parent = None):
  
    '''
    ---------------------------------------------
    single_element(parent)
    ---------------------------------------------
        
    DESCRIPTION HERE

    Parameters
    ----------

    parent : handybeam world
            DESCRIPTION HERE
        
    '''

    this = TxArray(parent)
    this.name = 'most basic single point'
    this.is_frequency_enabled = True
    this.tx_array_element_descriptor = this.generate_tx_array_element(amplitude_ratio_setting=1.0)
    
    return this

def simple_linear(parent = None,element_count=16, element_pitch = 7e-3):

    '''
    ---------------------------------------------
    simple_linear(parent, element_count, element_pitch)
    ---------------------------------------------
        
    DESCRIPTION HERE

    Parameters
    ----------

    parent : handybeam world
            DESCRIPTION HERE
    element_count : int 
            DESCRIPTION HERE
    element_pitch : float 
            DESCRIPTION HERE
        
    '''

    this = TxArray(parent)
    this.name = 'a line of elements, starting at xyz=0, along y, spaced by {:0.1f}mm'.format(element_pitch*1e3)

    this.tx_array_element_descriptor = np.zeros((element_count, 16), dtype=np.float32)

    half_length = (element_count*element_pitch)/2

    for array_element_iy in range(element_count):
       
        # add an element at that indexed location
        element_idx = array_element_iy

        loc_x = 0
        loc_y = (array_element_iy-(element_pitch/2)+0.5) * element_pitch - half_length

        this.tx_array_element_descriptor[element_idx, :] = \
        this.generate_tx_array_element(x=loc_x, y=loc_y, amplitude_ratio_setting=1.0)


    return this

def USX(parent = None):

    '''
    ---------------------------------------------
    USX(parent)
    ---------------------------------------------
        
    DESCRIPTION HERE

    Parameters
    ----------

    parent : handybeam world
            DESCRIPTION HERE
        
    '''
   
    return rectilinear(parent,
                            element_count_x=16,
                            element_count_y=16,
                            element_pitch_x=__default_USX_element_spacing,
                            element_pitch_y=__default_USX_element_spacing)

def rectilinear(parent = None,element_count_x=16, element_count_y=16, element_pitch_x=7e-3, element_pitch_y=7e-3):

    '''
    ---------------------------------------------
    rectilinear(parent,element_count_x,element_count_y,element_pitch_x, element_pitch_y)
    ---------------------------------------------
        
    DESCRIPTION HERE

    Parameters
    ----------

    parent : handybeam world
            DESCRIPTION HERE
    element_count_x : int
            DESCRIPTION HERE
    element_count_y : int
            DESCRIPTION HERE
    element_pitch_x : float
            DESCRIPTION HERE
    element_pitch_y : float
            DESCRIPTION HERE
        
    '''
    this = TxArray(parent)

    total_element_count = element_count_x * element_count_y

    this.tx_array_element_descriptor = np.zeros((total_element_count, 16), dtype=np.float32)

    for array_element_iy in range(element_count_y):
        for array_element_ix in range(element_count_x):
            # add an element at that indexed location
            element_idx = array_element_iy*element_count_x+array_element_ix

            loc_x = (array_element_ix-(element_count_x/2)+0.5) * element_pitch_x
            loc_y = (array_element_iy-(element_count_y/2)+0.5) * element_pitch_y

            this.tx_array_element_descriptor[element_idx, :] = \
                this.generate_tx_array_element(x=loc_x, y=loc_y, amplitude_ratio_setting=1.0)

            # print('at B,{},{},{}'.format(array_element_iy,array_element_ix,this.tx_array_element_descriptor_a.dtype))

    this.name = 'fully sampled rectilinear, parametrized with element_count={}; '.format(
        element_count_x * element_count_y)

    return this
