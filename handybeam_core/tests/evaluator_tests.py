## Imports

import os
import sys
import inspect
import unittest

# Include path to handybeam_core directory

sys.path.append('../.')

## Class

class EvaluatorTests(unittest.TestCase):

    def setUp(self):

        self.evaluator = None

    def tearDown(self):

        del self.evaluator
    
    def test_import(self):

        module_name = 'handybeam_core.evaluators'

        import handybeam_core.evaluators

        fail = False

        if module_name not in sys.modules:
            
            fail = True

        self.assertEqual(fail,False)

    def test_instance_creation(self):

        import handybeam_core.evaluators

        evaluator_2d = handybeam_core.evaluators.Evaluator2D()
        evaluator_3d = handybeam_core.evaluators.Evaluator3D()

        if isinstance(evaluator_2d, handybeam_core.evaluators.Evaluator2D) and \
           isinstance(evaluator_3d, handybeam_core.evaluators.Evaluator3D):
           
            fail = False

        self.assertEqual(fail,False)

    def test_2d_metrics(self):

        import handybeam_core.evaluators
        import numpy as np
        from handybeam_core.test_code.beam_metrics_2d import TestSamplingField
    
        fail = True

        # Initialise the world 

        world = handybeam_core.world.World()

        # Initialise evaluator object.
                                
        evaluator_2d = handybeam_core.evaluators.Evaluator2D()

        test_sampler = TestSamplingField(world)

        test_sampler.calculate_metrics()

        # Add sampling field.

        evaluator_2d.add_sampling_field(test_sampler)
    
        evaluator_results = evaluator_2d.find_area_metrics()

        if np.sum(evaluator_results - test_sampler.vector_2d_metrics) < 1e-15:
            
            fail = False
        
        self.assertEqual(fail,False)

    def test_3d_metrics(self):

        import handybeam_core.evaluators
        import numpy as np
        from handybeam_core.test_code.beam_metrics_3d import TestSamplingField
    
        fail = True

        # Initialise the world 

        world = handybeam_core.world.World()

        # Initialise evaluator object.
                                
        evaluator_3d = handybeam_core.evaluators.Evaluator3D()

        test_sampler = TestSamplingField(world)

        test_sampler.calculate_metrics()

        # Add sampling field.

        evaluator_3d.add_sampling_field(test_sampler)
    
        evaluator_results = evaluator_3d.find_volume_metrics()

        if np.sum(evaluator_results - test_sampler.vector_3d_metrics) < 1e-15:
            
            fail = False
        
        self.assertEqual(fail,False)




## Script 

if __name__ == '__main__':

    unittest.main()
