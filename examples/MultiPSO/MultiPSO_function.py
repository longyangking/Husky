# Author: Yang Long <longyang_123@yeah.net>
#
# License: LGPL-2.1


import sys
sys.path.append("../..")

import Husky.PSO as PSO
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
    print '1th Function Optimizing ...'
    LB = [-10]
    UB = [10]
    multipso = PSO.MultiPSO(func=fun1,nvars=1,targetsize=2,LB=LB,UB=UB,maxiter=30,particlesize=100)
    multipso.start()
    solutions,objectives = multipso.getsolution()

    plt.figure()
    plt.scatter(objectives[:,0],objectives[:,1])
    plt.xlabel(r'$F_1$')
    plt.ylabel(r'$F_2$')
    plt.title('Pareto Front')

    print '2th Function Optimizing ...'
    LB = [-10]
    UB = [10]
    multipso = PSO.MultiPSO(func=fun2,nvars=1,targetsize=2,LB=LB,UB=UB,particlesize=80,verbose=True)
    multipso.start()
    solutions,objectives = multipso.getsolution()

    plt.figure()
    plt.scatter(objectives[:,0],objectives[:,1])
    plt.xlabel(r'$F_1$')
    plt.ylabel(r'$F_2$')
    plt.title('Pareto Front')

    plt.show()