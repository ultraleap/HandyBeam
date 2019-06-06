## Imports

import os
import sys
import inspect
import unittest

# Include path to handybeam directory

sys.path.append('../.')

## Class

class SolverMixinsTests(unittest.TestCase):

    def setUp(self):

        self.solver_mixin = None

    def tearDown(self):

        del self.solver_mixin
    
    def test_import(self):

        module_name_1 = 'handybeam.solver_mixins'
        module_name_2 = 'handybeam.solver_mixins.single_focus_solver'


        import handybeam.solver_mixins
        import handybeam.solver_mixins.single_focus_solver


        fail = False

        if module_name_1 not in sys.modules or module_name_2 not in sys.modules:
            
            fail = True

        self.assertEqual(fail,False)

    def test_instance_creation(self):

        import handybeam.solver_mixins.single_focus_solver

        self.solver_mixin = handybeam.solver_mixins.single_focus_solver.SFSolverMixin()
        
        fail = True

        if isinstance(self.solver_mixin, handybeam.solver_mixins.single_focus_solver.SFSolverMixin):
            
            fail = False

        self.assertEqual(fail,False)


## Script 

if __name__ == '__main__':

    unittest.main()
