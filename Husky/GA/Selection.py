# Author: Yang Long <longyang_123@yeah.net>
#
# License: LGPL-2.1

import numpy as np

# Selection function will select parents for next generation based on fitness data

def Tournament(fitness,nParents=1,tournamentsize=3):
    '''
    Choose best individual based on the Tournament (Default)
    '''
    selected = np.zeros(nParents,dtype=int)
    N = np.size(fitness)
    for i in range(nParents):
        pos = np.random.randint(N,size=tournamentsize)
        bestindividual = fitness[pos]
        selected[i] = pos[np.argmax(bestindividual)]
    return selected

def StochasticUniform(fitness,nParents=1):
    '''
    Choose parents based on the combination of stochastic start and uniform process
    '''
    selected = np.zeros(nParents,dtype=int)
    popsize = np.size(fitness)
    wheel = np.cumsum(fitness)/np.sum(fitness)/nParents
    # Step through the wheel in even steps
    stepsize = 1.0/nParents
    # Start at a random position
    position = np.random.random()*stepsize
    start = 0
    for i in range(nParents):
        for j in range(start,popsize):
            if (position < wheel[j]):
                selected[i] = j
                start = j
                break
        position += stepsize
    return selected

def Remainder(fitness,nParents=1):
    '''
    Select parents based on the integer and fractional parts
    '''
    selected = np.zeros(nParents,dtype=int)
    popsize = np.size(fitness)
    value = fitness[:] # Deep Copy
    next = 0
    for i in range(popsize):
        while value[i] >= 1:
            if  next >= nParents:
                selected[next] = i
                next += 1
                value[i] -= 1
            else:
                return selected

    # Return if number of parents has been satisfied
    if next >= nParents:
        return selected

    intervals = np.cumsum(value)
    intervals = intervals/intervals[-1]

    # Pick rest of parents by chance
    for i in range(next,nParents):
        pick = np.random.random()
        for j in range(popsize):
            if pick <= intervals(i):
                selected[i] = j

                value[i] = 0
                intervals = np.cumsum(value)
                if intervals[-1] != 0:
                    intervals = intervals/intervals[-1]
                break
    
    return selected

def Roulette(fitness,nParents=1):
    '''
    Select parents by simulating a Roulette Wheel
    '''
    selected = np.zeros(nParents,dtype=int)
    popsize = np.size(fitness)
    wheel = np.cumsum(fitness)/np.sum(fitness)
    
    for i in range(nParents):
        pick = np.random.random()
        for j in range(popsize):
            if (pick < wheel[j]):
                selected[i] = j
                break

    return selected

