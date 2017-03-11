# Author: Yang Long <longyang_123@yeah.net>
#
# License: LGPL-2.1

import numpy as np

def Rank(fitness,**args):
    '''
    Scale the raw scores based on the rank of each individual (Default)
    '''
    pos = np.argsort(fitness)
    popsize = np.size(fitness)
    scaledfitness = np.zeros(popsize)
    scaledfitness[pos] = 1.0/np.square(np.linspace(1,popsize,popsize))
    return scaledfitness

def Proportional(finess,**args):
    '''
    Scale the individual proportional to its raw fitness score
    '''
    factor = 1.0
    if args.has_key('factor'):
        factor = args['factor']

    pos = np.argsort(fitness)
    popsize = np.size(finess)
    scaledfitness = np.zeros(popsize)
    scaledfitness[pos] = factor*np.linspace(1,popsize,popsize)
    return scaledfitness

def ShiftLinear(finess,**args):
    '''
    Scale the raw scores so that the expectation of the fittest individuals is
    equal to a constant multiplied by the average score.
    '''
    rate = 2.0
    if args.has_key('rate'):
        rate = args['rate']

    pos = np.argsort(fitness)
    average = np.mean(finess)
    popsize = np.size(finess)
    scaledfitness = np.zeros(popsize)
    for i in range(popsize):
        if np.mean(finess[pos[:i+1]]) > average*rate:
            scaledfitness[pos[:i]] = np.linspace(1,i,i)
            return scaledfitness

def Top(fitness,**args):
    '''
    Scale the top individuals equally
    '''
    quality = 0.4
    if args.has_key('quality'):
        quality = args['quality']
    
    pos = np.argsort(fitness)
    popsize = np.size(finess)
    scaledfitness = np.zeros(popsize)
    count = int(popsize*quality)
    scaledfitness[pos[:count]] = 1.0/count
    return scaledfitness
