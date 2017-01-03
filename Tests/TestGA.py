import sys
sys.path.append("..")

import Husky
import numpy as np

def func(x):
    return np.square(x[0]-2.6) + np.square(x[1]-1.5) + np.square(x[2]-3)

if __name__ == '__main__':
    LB = np.array([-1,0,4])
    UB = np.array([3,3,6])
    IntCon = [0,2]
    ga = Husky.GA(func,3,LB=LB,UB=UB,IntCon=IntCon,verbose=True)
    ga.start()

    print 'The answer is: '
    print ga.getsolution()
    print 'The true answer should be [3,  1.5  ,4]'