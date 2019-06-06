## Imports

import os
import sys
import inspect
import unittest

# Include path to handybeam_core directory

sys.path.append('../.')

## Class

class TranslatorTests(unittest.TestCase):

    def setUp(self):

        self.translator = None

    def tearDown(self):

        del self.translator
    
    def test_import(self):

        module_name = 'handybeam_core.translator'

        import handybeam_core.translator

        fail = False

        if module_name not in sys.modules:
            
            fail = True

        self.assertEqual(fail,False)

    def test_instance_creation(self):

        import handybeam_core.translator

        self.translator = handybeam_core.translator.Translator()
        
        fail = True

        if isinstance(self.translator, handybeam_core.translator.Translator):
            
            fail = False

        self.assertEqual(fail,False)

## Script 

if __name__ == '__main__':

    unittest.main()
