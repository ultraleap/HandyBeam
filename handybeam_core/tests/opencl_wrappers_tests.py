## Imports

import os
import sys
import inspect
import unittest

# Include path to handybeam_core directory

sys.path.append('../.')

## Class

class OpenclWrappersTests(unittest.TestCase):

    def setUp(self):

        self.propagator_wrapper = None
        self.solver_wrapper = None
        self.translator_wrapper = None

    def tearDown(self):

        del self.propagator_wrapper
        del self.solver_wrapper
        del self.translator_wrapper
    
    def test_import(self):

        module_name_1 = 'handybeam_core.opencl_wrappers'
        module_name_2 = 'handybeam_core.opencl_wrappers.propagator_wrappers'
        module_name_3 = 'handybeam_core.opencl_wrappers.solver_wrappers'
        module_name_4 = 'handybeam_core.opencl_wrappers.translator_wrappers'


        import handybeam_core.opencl_wrappers
        import handybeam_core.opencl_wrappers.propagator_wrappers
        import handybeam_core.opencl_wrappers.solver_wrappers
        import handybeam_core.opencl_wrappers.translator_wrappers


        fail = False

        if  module_name_1 not in sys.modules or \
            module_name_2 not in sys.modules or \
            module_name_3 not in sys.modules or \
            module_name_4 not in sys.modules :
                        
            fail = True

        self.assertEqual(fail,False)

    def test_instance_creation(self):

        import handybeam_core.opencl_wrappers.propagator_wrappers
        import handybeam_core.opencl_wrappers.solver_wrappers
        import handybeam_core.opencl_wrappers.translator_wrappers

        self.propagator_wrapper = handybeam_core.opencl_wrappers.propagator_wrappers.Propagator()
        self.solver_wrapper = handybeam_core.opencl_wrappers.solver_wrappers.Solver()
        self.translator_wrapper = handybeam_core.opencl_wrappers.translator_wrappers.Translator()

        fail = True

        if isinstance(self.propagator_wrapper,handybeam_core.opencl_wrappers.propagator_wrappers.Propagator)     and \
           isinstance(self.solver_wrapper, handybeam_core.opencl_wrappers.solver_wrappers.Solver)             and \
           isinstance(self.translator_wrapper, handybeam_core.opencl_wrappers.translator_wrappers.Translator):
            
            fail = False

        self.assertEqual(fail,False)



## Script 

if __name__ == '__main__':

    unittest.main()
