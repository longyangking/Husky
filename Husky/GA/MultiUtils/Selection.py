# Author: Yang Long <longyang_123@yeah.net>
#
# License: LGPL-2.1

import numpy as np
from . import Pareto
# Selection function will select parents for next generation based on fitness data

def Tournament(rank,distance,nParents,args):
    '''
    Choose best individual based on the Tournament (Default)
    '''
    tournamentsize = 3
    if 'tournamentsize' in args:
        tournamentsize = args['tournamentsize']

    selected = np.zeros(nParents,dtype=int)
    popsize = np.size(rank)

    for i in range(nParents):
        pos = np.random.randint(popsize,size=tournamentsize)
        sortedpos = Pareto.crowdingoperator(rank[pos],distance[pos])
        selected[i] = pos[sortedpos[0]]
    return selected

def StochasticUniform(rank,distance,nParents,args):
    '''
    Choose parents based on the combination of stochastic start and uniform process
    '''
    return Tournament(rank,distance,nParents,args)

#    selected = np.zeros(nParents,dtype=int)
#    popsize = np.size(rank)
#    wheel = np.cumsum(rank)/np.sum(rank)/nParents
#    # Step through the wheel in even steps
#    stepsize = 1.0/nParents
#    # Start at a random position
#    position = np.random.random()*stepsize
#    start = 0
#    for i in range(nParents):
#        for j in range(start,popsize):
#            if (position < wheel[j]):
#                selected[i] = j
#                start = j
#                break
#        position += stepsize
#    return selected

def Remainder(rank,distance,nParents,args):
    '''
    Select parents based on the integer and fractional parts
    '''
    return Tournament(rank,distance,nParents,args)

#    selected = np.zeros(nParents,dtype=int)
#    popsize = np.size(fitness)
#    value = fitness[:] # Deep Copy
#    next = 0
#    for i in range(popsize):
#        while value[i] >= 1:
#            if  next >= nParents:
#                selected[next] = i
#                next += 1
#                value[i] -= 1
#            else:
#                return selected
#
#    # Return if number of parents has been satisfied
#    if next >= nParents:
#        return selected
#
#    intervals = np.cumsum(value)
#    intervals = intervals/intervals[-1]
#
#    # Pick rest of parents by chance
#    for i in range(next,nParents):
#        pick = np.random.random()
#        for j in range(popsize):
#            if pick <= intervals(i):
#                selected[i] = j
#
#                value[i] = 0
#                intervals = np.cumsum(value)
#                if intervals[-1] != 0:
#                    intervals = intervals/intervals[-1]
#                break
#    
#    return selected

def Roulette(rank,distance,nParents,args):
    '''
    Select parents by simulating a Roulette Wheel
    '''
    return Tournament(rank,distance,nParents,args)

#    selected = np.zeros(nParents,dtype=int)
#    popsize = np.size(fitness)
#    wheel = np.cumsum(fitness)/np.sum(fitness)
#    
#    for i in range(nParents):
#        pick = np.random.random()
#        for j in range(popsize):
#            if (pick < wheel[j]):
#                selected[i] = j
#                break
#
#    return selected

