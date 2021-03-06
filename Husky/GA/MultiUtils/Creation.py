# Author: Yang Long <longyang_123@yeah.net>
#
# License: LGPL-2.1

import numpy as np

def Uniform(popsize,chromesize,LB,UB,IntCon,args):
    '''
    Create Random Initial Population for GA
    '''
    populations = np.zeros((popsize,chromesize))

    for i in range(popsize):
        chrome = LB + (UB - LB)*np.random.random(chromesize)
        # Satisfy the Integer constraints
        if IntCon is not None:
            intchrome = np.floor(chrome[IntCon])
            intchrome = intchrome + 1*(np.random.random(size=np.size(intchrome))>0.5)

            posLB = np.where(intchrome<LB[IntCon])
            intchrome[posLB] = LB[IntCon][posLB]

            posUB = np.where(intchrome>UB[IntCon])
            intchrome[posUB] = UB[IntCon][posUB]
            
            chrome[IntCon] = intchrome
        populations[i] = chrome
    
    return populations

def Feasible(popsize,chromesize,LB,UB,IntCon,args):
    # TODO
    pass

def NonlinearFeasible(popsize,chromesize,LB,UB,IntCon,args):
    # TODO
    pass

