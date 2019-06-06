## Imports

import handybeam_core
import handybeam_core.opencl_wrappers.abstract_wrapper
import handybeam_core.translator_mixins
import handybeam_core.translator_mixins.xy_translator
import handybeam_core.translator_mixins.xyz_translator
import handybeam_core.tx_array
import handybeam_core.cl_system

## Class

class Translator(
                    handybeam_core.opencl_wrappers.abstract_wrapper.Wrapper,
                    handybeam_core.translator_mixins.xy_translator.XYTranslatorMixin,
                    handybeam_core.translator_mixins.xyz_translator.XYZTranslatorMixin
                ):

    '''
    ---------------------------------------------
    Translator
    ---------------------------------------------
    
    This is a wrapper class which inherits from the template wrapper class Wrapper and the 
    OpenCL translator mixin classes. An instance of this class is initialised when a translator
    object is initialised. 

    '''    

    def __init__(self,parent=None):
       
        ## TODO - Provide description and type for the handybeam world object.
        
        '''
        ---------------------------------------------
        __init__(parent)
        ---------------------------------------------
        
        This method intialises an instance of the Translator class. During the initialisation process,
        the compiled OpenCL translator kernels are assigned to the appropriate translator mixin classes.

        Parameters
        ----------

        parent : handybeam world object
            DESCRIPTION

        '''

        # Inherits the OpenCL wrappers - i.e. the Mixin classes

        super(Translator, self).__init__()

        self.parent = parent
        self.cl_system = handybeam_core.cl_system.OpenCLSystem(parent=self.parent)

        # Run the _register methods for each of mixin classes to initialise the high-performance opencl kernels.

        self._register_xy_translator()
        self._register_xyz_translator()
