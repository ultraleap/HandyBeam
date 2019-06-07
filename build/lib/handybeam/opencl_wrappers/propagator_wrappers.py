## Imports

import handybeam
import handybeam.opencl_wrappers.abstract_wrapper
import handybeam.propagator_mixins
import handybeam.propagator_mixins.clist_propagator
import handybeam.propagator_mixins.rect_propagator
import handybeam.propagator_mixins.hex_propagator
import handybeam.propagator_mixins.lamb_propagator
import handybeam.tx_array
import handybeam.cl_system


## Global variables

## Class

class Propagator(      

                    handybeam.opencl_wrappers.abstract_wrapper.Wrapper,
                    handybeam.propagator_mixins.clist_propagator.ClistPropMixin,
                    handybeam.propagator_mixins.rect_propagator.RectPropMixin,
                    handybeam.propagator_mixins.hex_propagator.HexPropMixin,
                    handybeam.propagator_mixins.lamb_propagator.LambPropMixin
                    
                ):

    '''
    ---------------------------------------------
    Propagator
    ---------------------------------------------
    
    This is a wrapper class which inherits from the template wrapper class Wrapper and the 
    OpenCL propagator mixin classes. An instance of this class is initialised when a world
    object is initialised. 

    '''

    def __init__(self,parent=None):

        ## TODO - Provide description and type for the handybeam world object.

        '''
        ---------------------------------------------
        __init__(parent)
        ---------------------------------------------
        
        This method intialises an instance of the Propagator class. During the initialisation process,
        the compiled OpenCL propagator kernels are assigned to the appropriate propagator mixin classes.

        Parameters
        ----------

        parent : handybeam world object
            DESCRIPTION

        '''

        # Inherits the OpenCL wrappers - i.e. the mixin classes

        super(Propagator, self).__init__()

        self.parent = parent
        self.cl_system = handybeam.cl_system.OpenCLSystem(parent = self.parent)

        # Run the _register methods for each of mixin classes to initialise the high-performance opencl kernels.

        self._register_clist_propagator()
        self._register_rect_propagator()
        self._register_hex_propagator()
        self._register_lamb_propagator()

