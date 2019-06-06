## Imports

import os
import sys
import inspect
import unittest
import numpy as np

# Include path to handybeam_core directory

sys.path.append('../.')

## Class

class TranslatorMixinsTests(unittest.TestCase):

    def setUp(self):

        self.xy_translator_mixin = None
        self.xyz_translator_mixin = None

    def tearDown(self):

        del self.xy_translator_mixin
        del self.xyz_translator_mixin
    
    def test_import(self):

        module_name_1 = 'handybeam_core.translator_mixins'
        module_name_2 = 'handybeam_core.translator_mixins.xy_translator'
        module_name_3 = 'handybeam_core.translator_mixins.xyz_translator'

        import handybeam_core.translator_mixins
        import handybeam_core.translator_mixins.xy_translator
        import handybeam_core.translator_mixins.xyz_translator

        fail = False

        if module_name_1 not in sys.modules or module_name_2 not in sys.modules or module_name_3 not in sys.modules:
            
            fail = True

        self.assertEqual(fail,False)


    def test_instance_creation(self):

        import handybeam_core.translator_mixins.xy_translator
        import handybeam_core.translator_mixins.xyz_translator

        self.xy_translator_mixin = handybeam_core.translator_mixins.xy_translator.XYTranslatorMixin()
        self.xyz_translator_mixin = handybeam_core.translator_mixins.xyz_translator.XYZTranslatorMixin()
        
        fail = True

        if np.logical_and(isinstance(self.xy_translator_mixin,handybeam_core.translator_mixins.xy_translator.XYTranslatorMixin),
                          isinstance(self.xyz_translator_mixin,handybeam_core.translator_mixins.xyz_translator.XYZTranslatorMixin)) :
            
            fail = False

        self.assertEqual(fail,False)
        
## Script 

if __name__ == '__main__':

    unittest.main()
