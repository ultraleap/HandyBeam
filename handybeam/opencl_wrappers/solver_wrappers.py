## Imports

import handybeam
import handybeam.opencl_wrappers.abstract_wrapper
import handybeam.solver_mixins
import handybeam.solver_mixins.single_focus_solver
import handybeam.tx_array
import handybeam.cl_system

## Class

class Solver(
                handybeam.opencl_wrappers.abstract_wrapper.Wrapper,
                handybeam.solver_mixins.single_focus_solver.SFSolverMixin
            ):

    '''
    ---------------------------------------------
    Solver
    ---------------------------------------------
    
    This is a wrapper class which inherits from the template wrapper class Wrapper and the 
    OpenCL solver mixin classes. An instance of this class is initialised when a solver
    object is initialised. 

    '''    

    def __init__(self, parent=None, use_device = 2, use_platform = 0):

        ## TODO - Provide description and type for the handybeam world object.

        '''
        ---------------------------------------------
        __init__(parent)
        ---------------------------------------------
        
        This method intialises an instance of the Solver class. During the initialisation process,
        the compiled OpenCL solver kernels are assigned to the appropriate solver mixin classes.

        Parameters
        ----------

        parent : handybeam world object
            DESCRIPTION

        '''
       
        # Inherits the OpenCL wrappers - i.e. the mixin classes

        super(Solver, self).__init__()
        
        self.parent = parent
        self.cl_system = handybeam.cl_system.OpenCLSystem(parent = self.parent,use_device = self.parent.device, use_platform = self.parent.platform)

        # Run the _register methods for each of mixin classes to initialise the high-performance OpenCL kernels.

        self._register_single_focus_solver()
