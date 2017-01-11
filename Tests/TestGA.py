import sys
sys.path.append("..")

import Husky
import numpy as np

def func(x):
    return np.square(x[0]-2.6) + np.square(x[1]-1.5) + np.square(x[2]-3)

def func2(x):
    return np.power(x[0]-2.6,3) + np.square(x[1]-1.5) + np.square(x[2]-3.5)

if __name__ == '__main__':
    LB = np.array([-1,0,4])
    UB = np.array([3,3,6])
    IntCon = [0,2]
    ga = Husky.GA(func,3,LB=LB,UB=UB,IntCon=IntCon,verbose=False)
    ga.start()

    print 'The answer is: '
    print ga.getsolution()
    print 'The true answer should be [3,  1.5  ,4]'

    LB = np.array([0,0,3])
    UB = np.array([3,3,6])
    ga = Husky.GA(func2,3,LB=LB,UB=UB,verbose=True)
    ga.start()

    print 'The answer is: '
    print ga.getsolution()
    print 'The true answer should be [2.6,  1.5  , 3.5]'

    LB = np.array([-1,0,4])
    UB = np.array([3,3,6])
    ga = Husky.GA(func,3,LB=LB,UB=UB,verbose=False)
    ga.start()

    print 'The answer is: '
    print ga.getsolution()
    print 'The true answer should be [2.6,  1.5  , 4]'