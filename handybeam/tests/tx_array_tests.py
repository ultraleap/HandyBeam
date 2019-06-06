## Imports

import os
import sys
import inspect
import unittest

# Include path to handybeam directory

sys.path.append('../.')

## Class

class TxArrayTests(unittest.TestCase):

    def setUp(self):

        self.tx_array = None

    def tearDown(self):

        del self.tx_array
    
    def test_import(self):

        module_name = 'handybeam.tx_array'

        import handybeam.tx_array

        fail = False

        if module_name not in sys.modules:
            
            fail = True

        self.assertEqual(fail,False)


    def test_instance_creation(self):

        import handybeam.tx_array

        self.tx_array = handybeam.tx_array.TxArray()
        
        fail = True

        if isinstance(self.tx_array, handybeam.tx_array.TxArray):
            
            fail = False

        self.assertEqual(fail,False)


## Script 

if __name__ == '__main__':

    unittest.main()
