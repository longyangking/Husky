# Author: Yang Long <longyang_123@yeah.net>
#
# License: LGPL-2.1

import numpy as np
from numpy import linalg as LA

def AnnealingFast(currenstates,LB,UB,IntCon,temperature,args):
    '''
    Fast Annealing (Default)
    '''
    (nChildrean,featuresize) = currenstates.shape
    #states = np.zeros((nChildrean,featuresize))
    coeffs = np.random.randn(nChildrean,featuresize)
    coeffs = coeffs/LA.norm(coeffs)
    states = currenstates + temperature*coeffs
     
    if IntCon is not None:
        intstate = np.floor(states[:,IntCon])
        intstate = intstate + 1*(np.random.random(size=intstate.shape)>0.5)
        states[:,IntCon] = intstate
    
    for i in range(featuresize):
        if LB is not None:
            posLB = np.where(states[:,i]<LB[i])
            states[posLB,i] = LB[i]

        if UB is not None:
            posUB = np.where(states[:,i]>UB[i])
            states[posUB,i] = UB[i]

    return states

def AnnealingBoltz(currenstates,LB,UB,IntCon,temperature,args):
    '''
    Boltzmann Annealing
    '''
    (nChildrean,featuresize) = currenstates.shape
    coeffs = np.random.randn(nChildrean,featuresize)
    coeffs = coeffs/LA.norm(coeffs)
    states = currenstates + np.sqrt(temperature)*coeffs
     
    if IntCon is not None:
        intstate = np.floor(states[:,IntCon])
        intstate = intstate + 1*(np.random.random(size=intstate.shape)>0.5)
        states[:,IntCon] = intstate
    
    for i in range(featuresize):
        if LB is not None:
            posLB = np.where(states[:,i]<LB[i])
            states[posLB,i] = LB[i]

        if UB is not None:
            posUB = np.where(states[:,i]>UB[i])
            states[posUB,i] = UB[i]

    return states