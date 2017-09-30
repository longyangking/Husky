# Author: Yang Long <longyang_123@yeah.net>
#
# License: LGPL-2.1
#
# Test cases for fminsearch

import sys
sys.path.append("..")

import Husky.Optimize as Optimize
import numpy as np


def fun(x):
    return np.square(x-3) + np.square(x-2)

def fun2(x):
    return np.square(x-5) + 2*np.sin(2*np.pi*x)

if __name__=='__main__':
    x0 = np.array([1])
    [x,value] = Optimize.fminsearch(fun,x0,numofpoints=100)
    # x: 2.5 value: 0.5
    print([x,value])

    [x,value] = Optimize.fminsearch(fun2,x0)
    # x: 1.834  value: 8.2957
    print([x,value])