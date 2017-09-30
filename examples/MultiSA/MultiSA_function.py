# Author: Yang Long <longyang_123@yeah.net>
#
# License: LGPL-2.1


import sys
sys.path.append("../..")

import Husky.SA as SA
import numpy as np
import matplotlib.pyplot as plt

def fun1(x):
    f1 = x[0]**2
    f2 = (x[0]-2)**2
    return f1,f2

def fun2(x):    
    f1 = 1 - np.exp(-np.sum(np.square(x[0] - 1.0/np.sqrt(3))))
    f2 = 1 - np.exp(-np.sum(np.square(x[0] + 1.0/np.sqrt(3))))
    return f1,f2

if __name__=='__main__':
    print('1th Function Optimizing ...')
    LB = [-10]
    UB = [10]
    multisa = SA.MultiSA(func=fun1,nvars=1,targetsize=2,LB=LB,UB=UB,
                maxiter=10,statesize=50,maxfunevals=10,verbose=True)
    multisa.start()
    solutions,objectives = multisa.getsolution()

    plt.figure()
    plt.scatter(objectives[:,0],objectives[:,1])
    plt.xlabel(r'$F_1$')
    plt.ylabel(r'$F_2$')
    plt.title('Pareto Front')
    plt.show()

if 0:

    print('2th Function Optimizing ...')
    LB = [-10]
    UB = [10]
    multisa = SA.MultiSA(func=fun2,nvars=1,targetsize=2,LB=LB,UB=UB,statesize=100,verbose=True)
    multisa.start()
    solutions,objectives = multisa.getsolution()

    plt.figure()
    plt.scatter(objectives[:,0],objectives[:,1])
    plt.xlabel(r'$F_1$')
    plt.ylabel(r'$F_2$')
    plt.title('Pareto Front')

    