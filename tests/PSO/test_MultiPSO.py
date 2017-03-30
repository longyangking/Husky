import sys
sys.path.append("..\..")

import Husky.PSO as PSO
import numpy as np
import unittest 

def func(x):
    f1 = np.square(x[0]-2)
    f2 = np.square(x[0])
    return f1,f2

class TestPSO(unittest.TestCase):
    def setUp(self):
        self.tolerance = 0.05

    def testGeneralCase(self):
        multipso = PSO.MultiPSO(func,1,2,verbose=True,maxiter=5)
        multipso.start()
        (bestnvars,value) = multipso.getsolution()
        print bestnvars

if __name__ == '__main__':
    unittest.main() 