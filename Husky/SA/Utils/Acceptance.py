# Author: Yang Long <longyang_123@yeah.net>
#
# License: LGPL-2.1

import numpy as np

def AcceptanceSA(delE,temperature,args):
    '''
    Basic Acceptance of Simulated Annealing
    '''
    statesize = np.size(delE)
    acceptance = np.zeros(statesize)

    acceptstate = np.where(delE < 0)
    acceptance[acceptstate] = 1

    considerstate = np.where(delE >= 0)
    prob = 1/(1 + np.exp(delE[considerstate]/np.max(temperature)))
    rand = np.random.random(np.size(considerstate))

    acceptpoint = np.where(prob > rand)
    acceptance[acceptpoint] = 1

    return acceptance