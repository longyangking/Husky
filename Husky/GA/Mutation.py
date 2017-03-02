# Author: Yang Long <longyang_123@yeah.net>
#
# License: LGPL-2.1

import numpy as np

def Uniform(chromes,LB,UB,IntCon,preal=0.1,pint=0.2):
    (M,N) = np.shape(chromes)
    newchromes = np.zeros([M,N])
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

            posLB = np.where(intchrome<LB[IntCon])
            intchrome[posLB] = UB[IntCon][posLB]        # Mutate to be UB when lower than LB

            posUB = np.where(intchrome>UB[IntCon])
            intchrome[posUB] = LB[IntCon][posUB]        # Mutate to be LB when larger than UB
            
            chrome[IntCon] = intchrome

    return newchromes

def SinglePoint(chromes,LB,UB,IntCon,constraints):
    # TODO
    pass

def Gaussian(chromes,LB,UB,IntCon,constraints):
    # TODO
    pass


def AdaptiveFeasible(chromes,LB,UB,IntCon,constraints):
    # TODO
    pass