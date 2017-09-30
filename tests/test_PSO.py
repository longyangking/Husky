import sys
sys.path.append("..")

import Husky.PSO as PSO
import numpy as np
import unittest 

def func(x):
    return np.square(x[0]-2.6) + np.square(x[1]-1.5) + np.square(x[2]-3)

class TestPSO(unittest.TestCase):
    def setUp(self):
        self.tolerance = 0.05

    def testGeneralCase(self):
        pso = PSO.PSO(func,3)
        pso.start()
        (bestnvars,value) = pso.getsolution()
        self.assertTrue(np.sum(np.square(value-0.0))<self.tolerance)

if __name__ == '__main__':
    unittest.main() 