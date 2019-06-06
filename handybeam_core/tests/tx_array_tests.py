## Imports

import os
import sys
import inspect
import unittest

# Include path to handybeam_core directory

sys.path.append('../.')

## Class

class TxArrayTests(unittest.TestCase):

    def setUp(self):

        self.tx_array = None

    def tearDown(self):

        del self.tx_array
    
    def test_import(self):

        module_name = 'handybeam_core.tx_array'

        import handybeam_core.tx_array

        fail = False

        if module_name not in sys.modules:
            
            fail = True

        self.assertEqual(fail,False)


    def test_instance_creation(self):

        import handybeam_core.tx_array

        self.tx_array = handybeam_core.tx_array.TxArray()
        
        fail = True

        if isinstance(self.tx_array,handybeam_core.tx_array.TxArray):
            
            fail = False

        self.assertEqual(fail,False)


## Script 

if __name__ == '__main__':

    unittest.main()
