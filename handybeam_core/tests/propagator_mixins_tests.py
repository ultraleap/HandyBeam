## Imports

import os
import sys
import inspect
import unittest

# Include path to handybeam_core directory

sys.path.append('../.')

## Class

class PropagatorMixinsTests(unittest.TestCase):

    def setUp(self):

        self.clist_propagator = None
        self.hex_propagator = None
        self.lamb_propagator = None
        self.rect_propagator = None

    def tearDown(self):

        del self.clist_propagator
        del self.hex_propagator
        del self.lamb_propagator
        del self.rect_propagator
    
    def test_import(self):

        module_name_1 = 'handybeam_core.propagator_mixins'
        module_name_2 = 'handybeam_core.propagator_mixins.clist_propagator'
        module_name_3 = 'handybeam_core.propagator_mixins.hex_propagator'
        module_name_4 = 'handybeam_core.propagator_mixins.lamb_propagator'
        module_name_5 = 'handybeam_core.propagator_mixins.rect_propagator'

        import handybeam_core.propagator_mixins
        import handybeam_core.propagator_mixins.clist_propagator
        import handybeam_core.propagator_mixins.hex_propagator
        import handybeam_core.propagator_mixins.lamb_propagator
        import handybeam_core.propagator_mixins.rect_propagator


        fail = False

        if  module_name_1 not in sys.modules or \
            module_name_2 not in sys.modules or \
            module_name_3 not in sys.modules or \
            module_name_4 not in sys.modules or \
            module_name_5 not in sys.modules:
                        
            fail = True

        self.assertEqual(fail,False)

    def test_instance_creation(self):

        import handybeam_core.propagator_mixins.clist_propagator
        import handybeam_core.propagator_mixins.hex_propagator
        import handybeam_core.propagator_mixins.lamb_propagator
        import handybeam_core.propagator_mixins.rect_propagator

        self.clist_propagator = handybeam_core.propagator_mixins.clist_propagator.ClistPropMixin()
        self.hex_propagator = handybeam_core.propagator_mixins.hex_propagator.HexPropMixin()
        self.lamb_propagator = handybeam_core.propagator_mixins.lamb_propagator.LambPropMixin()
        self.rect_propagator = handybeam_core.propagator_mixins.rect_propagator.RectPropMixin()

        fail = True

        if isinstance(self.clist_propagator,handybeam_core.propagator_mixins.clist_propagator.ClistPropMixin)     and \
           isinstance(self.hex_propagator, handybeam_core.propagator_mixins.hex_propagator.HexPropMixin)      and \
           isinstance(self.lamb_propagator, handybeam_core.propagator_mixins.lamb_propagator.LambPropMixin)   and \
           isinstance(self.rect_propagator, handybeam_core.propagator_mixins.rect_propagator.RectPropMixin) :            
            
            fail = False

        self.assertEqual(fail,False)


## Script 

if __name__ == '__main__':

    unittest.main()
