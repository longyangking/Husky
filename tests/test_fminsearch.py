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

if __name__=='__main__':
    x0 = np.array([1])
    [x,value] = Optimize.fminsearch(fun,x0)
    print([x,value])
