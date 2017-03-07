import sys
sys.path.append("..\..")

import numpy as np
import Husky.GA.Selection as Selection
import unittest 


class TestGAmutation(unittest.TestCase):
    def setUp(self):
        pass

    def testTwoPoint(self):
        fitness = np.array([1,2,3])
        parents = Selection.Tournament(fitness,nParents=4,tournamentsize=3)
        print parents
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main() 