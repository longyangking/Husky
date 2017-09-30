# Author: Yang Long <longyang_123@yeah.net>
#
# License: LGPL-2.1

import numpy as np

def Rank(fitness,args):
    '''
    Scale the raw scores based on the rank of each individual (Default)
    '''
    popsize = np.size(fitness,axis=0)
    targetsize = np.size(fitness,axis=1)
    scaledfitness = np.zeros((popsize,targetsize))
    pos = np.argsort(fitness,axis=0)

    for i in range(targetsize):
        scaledfitness[pos[:,i],i] = 1.0/np.square(np.linspace(1,popsize,popsize))
    return scaledfitness

def Proportional(finess,args):
    '''
    Scale the individual proportional to its raw fitness score
    '''
    factor = 1.0
    if 'factor' in args:
        factor = args['factor']

    popsize = np.size(fitness,axis=0)
    targetsize = np.szie(fitness,axis=1)
    scaledfitness = np.zeros((popsize,targetsize))
    pos = np.argsort(fitness,axis=0)

    for i in range(targetsize):
        scaledfitness[pos[:,i],i] = factor*np.square(np.linspace(popsize,1,popsize))
    return scaledfitness

def ShiftLinear(finess,args):
    '''
    Scale the raw scores so that the expectation of the fittest individuals is
    equal to a constant multiplied by the average score.
    '''
    rate = 2.0
    if args.has_key('rate'):
        rate = args['rate']

    popsize = np.size(fitness,axis=0)
    targetsize = np.szie(fitness,axis=1)
    scaledfitness = np.zeros((popsize,targetsize))
    pos = np.argsort(fitness,axis=0)
    average = np.mean(finess,axis=0)

    for j in range(targetsize):
        for i in range(popsize):
            if np.mean(finess[pos[:i+1,j],j]) > average[j]*rate:
                scaledfitness[pos[:i,j],j] = np.linspace(1,i,i)
                break
    return scaledfitness

def Top(fitness,args):
    '''
    Scale the top individuals equally
    '''
    quality = 0.4
    if args.has_key('quality'):
        quality = args['quality']
    
    popsize = np.size(fitness,axis=0)
    targetsize = np.szie(fitness,axis=1)
    scaledfitness = np.zeros((popsize,targetsize))
    pos = np.argsort(fitness,axis=0)

    count = int(popsize*quality)
    for i in range(targetsize):
        scaledfitness[pos[:count,i],i] = 1.0/count
    return scaledfitness
