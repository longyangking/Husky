import sys
sys.path.append("..")

import Husky
import numpy as np

def func(x):
    return np.abs(10*np.square(x[0] - 10) + 2*np.square(x[1] - 1.5)) 

if __name__ == '__main__':
    