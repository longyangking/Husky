# Author: Yang Long <longyang_123@yeah.net>
#
# License: LGPL-2.1
#
# Genetic Algorithm Demo with generalized constraints
# Note: You can find the original problem setting from this reference:
#
#       [1]Deb K, Pratap A, Agarwal S, et al. 
#       A fast and elitist multiobjective genetic algorithm: NSGA-II[J]. 
#       IEEE transactions on evolutionary computation, 2002, 6(2): 182-197.
#

import sys
sys.path.append("../..")

import Husky.GA as GA
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
    multiga = GA.MultiGA(func=fun1,nvars=1,targetsize=2,LB=LB,UB=UB,maxgeneration=50,verbose=True)
    multiga.start()
    solutions,objectives = multiga.getsolution()

    plt.figure()
    plt.scatter(objectives[:,0],objectives[:,1])
    plt.xlabel(r'$F_1$')
    plt.ylabel(r'$F_2$')
    plt.title('Pareto Front')

    print('2th Function Optimizing ...')
    LB = [-10]
    UB = [10]
    multiga = GA.MultiGA(func=fun2,nvars=1,targetsize=2,LB=LB,UB=UB,maxgeneration=50)
    multiga.start()
    solutions,objectives = multiga.getsolution()

    plt.figure()
    plt.scatter(objectives[:,0],objectives[:,1])
    plt.xlabel(r'$F_1$')
    plt.ylabel(r'$F_2$')
    plt.title('Pareto Front')

    plt.show()
    