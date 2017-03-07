# Author: Yang Long <longyang_123@yeah.net>
#
# License: LGPL-2.1
#
# Test cases for GA

import sys
sys.path.append("..\..")

import Husky.GA as GA
import numpy as np
import unittest 

def func(x):
    return np.square(x[0]-2.6) + np.square(x[1]-1.5) + np.square(x[2]-3)

def func2(x):
    return np.power(x[0]-2.6,3) + np.square(x[1]-1.5) + np.square(x[2]-3.5)

class TestGA(unittest.TestCase):
    def setUp(self):
        self.tolerance = 0.1

    def testGeneralGA(self):
        """
        General Cases
        """
        LB = np.array([-1,0,4])
        UB = np.array([3,3,6])
        IntCon = [0,2]
        ga = GA.GA(func,3,LB=LB,UB=UB,IntCon=IntCon,verbose=False)
        ga.start()
        (bestcandidate,value) = ga.getsolution()
        #self.assertTrue(np.sum(np.square(bestcandidate-[3,  1.5  ,4]))/np.sum(np.abs([3,  1.5  ,4]))<self.tolerance)
        self.assertTrue(np.sum(np.square(value-1.16))<self.tolerance)

        LB = np.array([0,0,3])
        UB = np.array([3,3,6])
        ga = GA.GA(func2,3,LB=LB,UB=UB,verbose=False)
        ga.start()
        (bestcandidate,value) = ga.getsolution()
        #self.assertTrue(np.sum(np.square(bestcandidate-[0,  1.5  , 3.5]))/np.sum(np.abs([0,  1.5  , 3.5]))<self.tolerance)
        self.assertTrue(np.sum(np.square(value-(-17.57)))<self.tolerance)

        LB = np.array([-1,0,4])
        UB = np.array([3,3,6])
        ga = GA.GA(func,3,LB=LB,UB=UB,verbose=False)
        ga.start()
        (bestcandidate,value) = ga.getsolution()
        #self.assertTrue(np.sum(np.square(bestcandidate-[2.6,  1.5  , 3]))/np.sum(np.abs([2.6,  1.5  , 3]))<self.tolerance)
        self.assertTrue(np.sum(np.square(value-1.003))<self.tolerance)

    def testDefaultGA(self):
        """
        Default Cases
        """
        LB = np.array([-8,-3,-3])
        UB = np.array([3,3,6])
        ga = GA.GA(func,3,LB=LB,UB=UB,verbose=False)
        ga.start()
        (bestcandidate,value) = ga.getsolution()
        #print bestcandidate
        #self.assertTrue(np.sum(np.square(bestcandidate-[2.6,  1.5  ,3]))/3<self.tolerance)
        self.assertTrue(np.abs(value-0.0)<self.tolerance)

        ga = GA.GA(func,3,verbose=False)
        ga.start()
        (bestcandidate,value) = ga.getsolution()
        #print value
        #self.assertTrue(np.sum(np.square(bestcandidate-[2.6,  1.5  ,3]))/3<self.tolerance)
        self.assertTrue(np.abs(value-0.0)<self.tolerance)

    def testMigration(self):
        LB = np.array([0,0,3])
        UB = np.array([3,3,6])
        ga = GA.GA(func2,3,LB=LB,UB=UB,verbose=False,groupsize=2)
        ga.start()
        (bestcandidate,value) = ga.getsolution()
        #self.assertTrue(np.sum(np.square(bestcandidate-[0,  1.5  , 3.5]))/np.sum(np.abs([0,  1.5  , 3.5]))<self.tolerance)
        self.assertTrue(np.sum(np.square(value-(-17.57)))<self.tolerance)

    def testLinearConstraint(self):
        '''
        Test Linear Constraint
        '''
        pass

    def testNonlinearConstraint(self):
        '''
        Test Non-linear Constraint
        '''
        pass
    
if __name__ == '__main__':
    unittest.main() 