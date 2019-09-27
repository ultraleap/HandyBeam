## Imports

import numpy as np
from handybeam.tx_array import TxArray

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
  
    '''DESCRIPTION HERE

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


def simple_linear(parent = None, element_count=16, element_pitch=7e-3):
    """1D line of elements, starting at xyz=0, along y, with given element_pitch

    Parameters
    ----------

    parent : handybeam.world.World
            the world to give to this array as parent
    element_count : int 
            count of elements.
    element_pitch : float 
            distance between elements
        
    """

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

    '''DESCRIPTION HERE

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

    '''DESCRIPTION HERE

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


def from_system_xml(parent=None, file=None):
    """
    attempt to load a description of the array from an "Acoustic Renderer" xml file.
    :param parent: set to local world.
    :param file: file name to load. Must be an "Acoustic Renderer" compatible xml file.
    :return:
    """
    import xml.etree.ElementTree as et

    this = TxArray(parent)

    try:
        tree = et.parse(file)

    except:
        print("XML parsing error")

    root = tree.getroot()

    no_transducers = 0

    for transducer in root.findall("./System/Transducers/Transducer"):
        no_transducers += 1

    this.tx_array_element_descriptor = np.zeros((no_transducers, 16), dtype=np.float32)

    for transducer in root.findall("./System/Transducers/Transducer"):
        element_id = int(transducer.get('Index'))
        x_pos = float(transducer.get('Xmm')) * 1e-3
        y_pos = float(transducer.get('Ymm')) * 1e-3
        z_pos = float(transducer.get('Zmm')) * 1e-3
        pol = transducer.get('ABX')

        if (pol == 'X'):
            # TODO: Check this works
            amp_ratio = 0.0

        else:
            amp_ratio = 1.0

        this.tx_array_element_descriptor[element_id, :] = \
            this.generate_tx_array_element(x=x_pos, y=y_pos, amplitude_ratio_setting=amp_ratio)

    return this


def build_sunflower_round(array_size=None, array_spacing=None, emitterfunc=None)

    """
    
    .. code-block:: matlab
    
        function output = build_sunflower_round(array_size, array_spacing, emitterfunc)
            % this function returns a focus_field object with a round sunflower arrangement with
            % given inputs.
            goldenRatio = (1+sqrt(5))/2;
            ga = 360/(goldenRatio^2);
            garad = ga*2*pi/360;
            num = 1:array_size;
            x = (array_spacing/2)*(4/pi)*sqrt(num).*sin(garad*num);
            y = (array_spacing/2)*(4/pi)*sqrt(num).*cos(garad*num);
            z = zeros(array_size,1)';
            emitterlocs = [x;y;z];
            emitternorms = [z;z;ones(array_size,1)'];
            emitteramps = ones(array_size,1);
            output = focus_field(emitterfunc, emitterlocs, emitternorms, emitteramps);
        end

    :param array_size: count of points to generate
    :param array_spacing: set to 0.0102 for Murata in U7; set to 0.0105 for Murata in dragonfly, 
    :param emitterfunc: most likely derelic, ignore
    :return: 
    """

    raise Exception('not translated from Matlab yet. Translate the code above.')