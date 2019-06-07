## Imports

import os
import sys
import inspect
import unittest

# Include path to handybeam directory

sys.path.append('../.')

## Class

class TranslatorTests(unittest.TestCase):

    def setUp(self):

        self.translator = None

    def tearDown(self):

        del self.translator
    
    def test_import(self):

        module_name = 'handybeam.translator'

        import handybeam.translator

        fail = False

        if module_name not in sys.modules:
            
            fail = True

        self.assertEqual(fail,False)

    def test_instance_creation(self):

        import handybeam.translator

        self.translator = handybeam.translator.Translator()
        
        fail = True

        if isinstance(self.translator, handybeam.translator.Translator):
            
            fail = False

        self.assertEqual(fail,False)

## Script 

if __name__ == '__main__':

    unittest.main()
