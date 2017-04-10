# Author: Yang Long <longyang_123@yeah.net>
#
# License: LGPL-2.1

import numpy as np

def Same(fitness,args):
    return fitness

def Rank(fitness,args):
    popsize = np.size(fitness,axis=0)
    targetsize = np.size(fitness,axis=1)
    scaledfitness = np.zeros((popsize,targetsize))
    pos = np.argsort(fitness,axis=0)

    for i in range(targetsize):
        scaledfitness[pos[:,i],i] = 1.0/np.square(np.linspace(1,popsize,popsize))
    return scaledfitness

