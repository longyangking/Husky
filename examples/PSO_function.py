# Author: Yang Long <longyang_123@yeah.net>
#
# License: LGPL-2.1
#
# Genetic Algorithm Demo with generalized constraints
# Note: You can find the original problem setting from this reference:
#
#       [1]Deep K, Singh K P, Kansal M L, et al. 
#       A real coded genetic algorithm for solving integer and mixed integer optimization problems[J]. 
#       Applied Mathematics & Computation, 2009, 212(2):505-518.
#

import sys
sys.path.append("..")

import Husky.PSO as PSO
import numpy as np

def constraintfun1(x):
    penalty = abs(1.25-x[0]**2-x[1]**2)*(1.25-x[0]**2-x[1]**2>0)
    penalty += abs(x[0]+x[1]-1.6)*(x[0]+x[1]-1.6<0)
    return penalty

def fun1(x):
    return 2*x[0]+x[1]

def constraintfun2(x):
    if np.abs(x[0])<0.000001:
        return np.inf
    penalty = np.abs(-x[0]-np.log(x[0]/2)+x[1])*(-x[0]-np.log(x[0]/2)+x[1]>0)
    return penalty

def fun2(x):
    if np.abs(x[0])<0.000001:
        return np.inf
    return -x[1]+2*x[0]-np.log(x[0]/2)

def constraintfun3(x):
    penalty = np.abs((x[0]-5)**2 + (x[1]-5)**2-100)*((x[0]-5)**2 + (x[1]-5)**2-100<0)
    penalty += np.abs(-(x[0]-6)**2-(x[1]-5)**2+82.81)*(-(x[0]-6)**2-(x[1]-5)**2+82.81<0)
    return penalty

def fun3(x):
    return (x[0]-10)**3 + (x[1]-20)**3

def constraintfun4(x):
    penalty = np.abs(2*x[0]**2 + x[1]**2 - 15)*(2*x[0]**2 + x[1]**2 - 15>0)
    penalty += np.abs(-x[0]+2*x[1]+x[2]-3.0)*(-x[0]+2*x[1]+x[2]-3.0>0)
    return penalty

def fun4(x):
    return x[0]**2 + x[0]*x[1] + 2*x[1]**2 - 6*x[0] - 2*x[1] - 12*x[2]

def constraintfun5(x):
    penalty = np.abs(x[0] + 2*x[1] + x[2] + x[3] - 4.0)*(x[0] + 2*x[1] + x[2] + x[3] - 4.0>=0)
    return penalty

def fun5(x):
    return (x[0] + 2*x[1] + 3*x[2] - x[3])*(2*x[0] + 5*x[1] + 3*x[2] - 6*x[3])

def constraintfun6(x):
    penalty = np.abs(0.9*(1-np.exp(-0.5*x[0]))-2*x[2])*(0.9*(1-np.exp(-0.5*x[0]))-2*x[2]>0)
    penalty += np.abs(0.8*(1-np.exp(-0.4*x[1]))-2*(1-x[2]))*(0.8*(1-np.exp(-0.4*x[1]))-2*(1-x[2])>0)
    penalty += np.abs(x[0]-10.0*x[2])*(x[0]-10.0*x[2]>0)
    penalty += np.abs(x[1]-10.0*(1-x[2]))*(x[1]-10.0*(1-x[2])>0)
    return penalty

def fun6(x):
    if 0.8*(1-np.exp(-0.4*x[0])) < 0.00001:
        return np.inf
    return 7.5*x[2] + 5.5*(1-x[2]) + 7*x[0] + 6*x[1] + 50*(x[2]/(2*x[2]-1))/(0.9*(1-np.exp(-0.5*x[0]))) \
        + 50*(1-x[2]/(2*x[2]-1))/(0.8*(1-np.exp(-0.4*x[0])))

if __name__=='__main__':
    print('-'*50)

    LB = [0,0]
    UB = [1.6,1]
    IntCon = [1]
    pso = PSO.PSO(fun1,2,LB=LB,UB=UB,IntCon=IntCon)
    pso.addconstraint(constraintfun1)
    pso.start()
    print('The global optimal is (0.5,1) with value 2')
    print('Fun 1 answer: ',pso.getsolution())
    print('-'*50)

    
    LB = [0.5,0]
    UB = [1.5,1]
    IntCon = [1]
    pso = PSO.PSO(fun2,2,C1=0.5,C2=0.5,LB=LB,UB=UB,IntCon=IntCon)
    pso.addconstraint(constraintfun2)
    pso.start()
    print('The global optimal is (1.35,1) with value 2.1')
    print('Fun 2 answer: ',pso.getsolution())
    print('-'*50)

    LB = [13,0]
    UB = [100,100]
    pso = PSO.PSO(fun3,2,C1=0.5,C2=0.5,LB=LB,UB=UB)
    pso.addconstraint(constraintfun3)
    pso.start()
    print('The global optimal is (14,0.8) with value -6961')
    print('Fun 3 answer: ',pso.getsolution())
    print('-'*50)

    LB = [0,0,0]
    UB = [10,10,10]
    IntCon = [0,1,2]
    pso = PSO.PSO(fun4,3,LB=LB,UB=UB,IntCon=IntCon)
    pso.addconstraint(constraintfun4)
    pso.start()
    print('The global optimal is (2,0,5) with value -68')
    print('Fun 4 answer: ',pso.getsolution())
    print('-'*50)

    LB = [0,0,0,0]
    UB = [1,1,1,1]
    IntCon = [0,1,2,3]
    pso = PSO.PSO(fun5,4,LB=LB,UB=UB,IntCon=IntCon)
    pso.addconstraint(constraintfun5,20)
    pso.start()
    print('The global optimal is (0,0,1,1) with value -6')
    print('Fun 5 answer: ',pso.getsolution())
    print('-'*50)

    LB = [0,0,0]
    UB = [10,10,1]
    IntCon = [2]
    pso = PSO.PSO(fun6,3,LB=LB,UB=UB,IntCon=IntCon)
    pso.addconstraint(constraintfun6)
    pso.start()
    print('The global optimal is (3.5,0,1) with value 99.2')
    print('Fun 6 answer: ',pso.getsolution())