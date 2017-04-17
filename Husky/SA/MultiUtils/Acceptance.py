# Author: Yang Long <longyang_123@yeah.net>
#
# License: LGPL-2.1

import numpy as np

def AcceptanceSA(drank,ddistance,temperature,args):
    '''
    Basic Acceptance of Simulated Annealing
    '''
    statesize = np.size(drank)
    acceptance = np.zeros(statesize)

    acceptstate = np.where(drank < 0)
    acceptance[acceptstate] = 1
    #acceptstate = np.where((drank == 0)*(ddistance > 0))
    #acceptance[acceptstate] = 1

    considerstate = np.where(drank >= 0)
    prob = np.zeros(np.size(considerstate))

    if np.max(temperature) == 0:
        return acceptance

    delta = drank[considerstate]/np.max(temperature)
    inf = delta>100
    prob[inf==True] = 0
    prob[inf==False] = 1/(1+np.exp(delta[inf==False]))

    rand = np.random.random(np.size(considerstate))

    acceptpoint = np.where(prob > rand)
    acceptance[acceptpoint] = 1

    return acceptance