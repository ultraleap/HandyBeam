## Imports

import os
import sys
import inspect
import unittest

# Include path to handybeam  directory

sys.path.append('../.')

## Class

class WorldTests(unittest.TestCase):

    def setUp(self):

        self.world = None

    def tearDown(self):

        del self.world
    
    def test_import(self):

        module_name = 'handybeam.world'

        import handybeam.world

        fail = False

        if module_name not in sys.modules:
            
            fail = True

        self.assertEqual(fail,False)

    def test_instance_creation(self):

        import handybeam.world

        self.world = handybeam.world.World()
        
        fail = True

        if isinstance(self.world, handybeam.world.World):
            
            fail = False

        self.assertEqual(fail,False)

        

## Script 

if __name__ == '__main__':

    unittest.main()
