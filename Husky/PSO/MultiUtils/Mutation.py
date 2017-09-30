# Author: Yang Long <longyang_123@yeah.net>
#
# License: LGPL-2.1

import numpy as np

def Uniform(chromes,rank,distance,LB,UB,mutationrate,IntCon,args):
    '''
    Uniform random mutation (Default)
    '''
    preal = 0.1
    pint = 0.2
    if 'preal' in args:
        preal = args['preal']
    if 'pint' in args:
        pint = args['pint']

    (M,N) = np.shape(chromes)
    newchromes = np.zeros([M,N])
    if mutationrate is not None:
        preal = mutationrate
        pint = 2.0*preal
    # Satisfy the Integer constraints
    for i in range(M):
        chrome = chromes[i]
        
        P = preal*np.ones(N)
        P[IntCon] = pint
        s = np.random.random(size=N)
        pos = np.where(s>P)
        chrome[pos] = LB[pos] + np.random.random(np.size(pos))*(UB[pos] - LB[pos])

        if IntCon is not None:
            intchrome = np.floor(chrome[IntCon])
            intchrome = intchrome + 1*(np.random.random(size=np.size(intchrome))>0.5)
            chrome[IntCon] = intchrome

        posLB = np.where(chrome<LB)
        chrome[posLB] = LB[posLB]        # Mutate to be UB when lower than LB

        posUB = np.where(chrome>UB)
        chrome[posUB] = UB[posUB]        # Mutate to be LB when larger than UB

        newchromes[i] = chrome

    return newchromes

def Gaussian(chromes,rank,distance,LB,UB,mutationrate,IntCon,args):
    '''
    Mutate based on the standard deviation
    '''
    shrink = 1.0
    scale = 1.0
    if 'shrink' in args:
        shrink = args['shrink']
    if 'scale' in args:
        scale = args['scale']
    
    (M,N) = np.shape(chromes)
    newchromes = np.zeros([M,N])

    scale = scale - shrink*scale*np.std(chromes,axis=0)

    for i in range(M):
        newchrome = chromes[i] + scale*np.random.randint(M,size=N)
        # Integer constraints
        if IntCon is not None:
            intchrome = np.floor(newchrome[IntCon])
            intchrome = intchrome + 1*(np.random.random(size=np.size(intchrome))>0.5)
            newchrome[IntCon] = intchrome
            
        posLB = np.where(newchrome<LB)
        newchrome[posLB] = UB[posLB]

        posUB = np.where(newchrome>UB)
        newchrome[posUB] = LB[posUB]

        newchromes[i] = newchrome
    
    return newchromes

def LogisticChaoticSequence(chromes,rank,distance,LB,UB,mutationrate,IntCon,args):
    # TODO This part will be done after the completement of module Optimize
    return Uniform(chromes,rank,distance,LB,UB,IntCon)

def AdaptiveFeasible(chromes,rank,distance,LB,UB,mutationrate,IntCon,args):
    '''
    Randomly mutate that are adaptive with respect to the constraints (filter the individuals in advance)
    '''
    # TODO This part will be done after the completement of module Optimize
    return Uniform(chromes,rank,distance,LB,UB,IntCon)
