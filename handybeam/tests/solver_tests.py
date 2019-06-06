## Imports

import os
import sys
import inspect
import unittest

# Include path to handybeam directory

sys.path.append('../.')

## Class

class SolverTests(unittest.TestCase):

    def setUp(self):

        self.solver = None

    def tearDown(self):

        del self.solver
    
    def test_import(self):

        module_name = 'handybeam.solver'

        import handybeam.solver

        fail = False

        if module_name not in sys.modules:
            
            fail = True

        self.assertEqual(fail,False)

    def test_instance_creation(self):

        import handybeam.solver

        self.solver = handybeam.solver.Solver()
        
        fail = True

        if isinstance(self.solver, handybeam.solver.Solver):
            
            fail = False

        self.assertEqual(fail,False)

## Script 

if __name__ == '__main__':

    unittest.main()
