## Imports

import os
import sys
import inspect
import unittest

# Include path to handybeam_core directory

sys.path.append('../.')

## Class

class SolverTests(unittest.TestCase):

    def setUp(self):

        self.solver = None

    def tearDown(self):

        del self.solver
    
    def test_import(self):

        module_name = 'handybeam_core.solver'

        import handybeam_core.solver

        fail = False

        if module_name not in sys.modules:
            
            fail = True

        self.assertEqual(fail,False)

    def test_instance_creation(self):

        import handybeam_core.solver

        self.solver = handybeam_core.solver.Solver()
        
        fail = True

        if isinstance(self.solver,handybeam_core.solver.Solver):
            
            fail = False

        self.assertEqual(fail,False)

## Script 

if __name__ == '__main__':

    unittest.main()
