# Author: Yang Long <longyang_123@yeah.net>
#
# License: LGPL-2.1

import numpy as np

def FastNonDominatedSorting(fitness,args):
    '''
    Fast non-dominated sorting

    Reference:
        Deb K, Pratap A, Agarwal S, et al. 
        A fast and elitist multiobjective genetic algorithm: NSGA-II[J]. 
        IEEE transactions on evolutionary computation, 2002, 6(2): 182-197.

    '''
    popsize = np.size(fitness,axis=0)
    targetsize = np.size(fitness,axis=1)
    #rank = popsize*np.ones(popsize)
    rank = np.zeros(popsize)
    distance = np.zeros(popsize)

    fronts = list()
    fronts.append([])  # First Front is Blank

    dominatedindividuals = list()
    dominatecount = np.zeros(popsize)
    

    # Get first front firstly
    for i in range(popsize):
        dominatedindividuals.append([])

        for j in range(popsize):
            if (np.sum(1*(fitness[i]>fitness[j]))==targetsize) and (np.sum(1*(fitness[i]==fitness[j]))<targetsize):
                dominatedindividuals[i].append(j)
            elif (np.sum(1*(fitness[i]<fitness[j]))==targetsize) and (np.sum(1*(fitness[i]==fitness[j]))<targetsize):
                dominatecount[i] += 1
        if dominatecount[i] == 0:
            fronts[0].append(i)
            rank[i] = 0

    # Get subsequent front
    index = 0
    while len(fronts[index]) > 0:
        nextfront = list()
        for frontindex in fronts[index]:
            for j in dominatedindividuals[frontindex]:
                dominatecount[j] -= 1
                if dominatecount[j] == 0:
                    rank[j] = index + 1
                    nextfront.append(j)
        index += 1
        fronts.append(nextfront)

    # Calculate CrowdingDistance
    if len(fronts) > 0:
        for index in range(len(fronts)):
            front = fronts[index]
            frontnum = len(front)
            if frontnum > 0:
                for k in range(targetsize):
                    frontfitness = [fitness[i,k] for i in front]
                    sortindex = np.argsort(frontfitness)
                    maxfrontfitness = frontfitness[sortindex[frontnum-1]]
                    minfrontfitness = frontfitness[sortindex[0]]
                    posmax = front[sortindex[frontnum-1]]
                    posmin = front[sortindex[0]]
                        
                    #distance[posmax] = maxfrontfitness
                    #distance[posmin] = minfrontfitness
                    Inf = 10.0*maxfrontfitness

                    distance[posmax] = Inf
                    distance[posmin] = Inf
                    
                    for i in range(1,len(sortindex)-1):
                        pos = front[sortindex[i]]
                        left = front[sortindex[i-1]]
                        right = front[sortindex[i+1]]
                        if maxfrontfitness == minfrontfitness:
                            distance[pos] = Inf
                        else:
                            distance[pos] = distance[right]-distance[left]#/(maxfrontfitness-minfrontfitness)
    
    return rank,distance

def frontier(rank,distance,nChildren):
    '''
    Select top number of Pareto frontiers
    '''
    frontier = crowdingoperator(rank,distance)
    return frontier[:nChildren]

def crowdingoperator(rank,distance):
    '''
    Sort data by crowding operator
    '''
    #data = np.array(zip(rank,-distance),dtype=[('rank', int), ('distance', float)])
    #return np.argsort(data, order=('rank','distance'))
    extra = distance/(np.max(distance)+1)
    newrank = rank - extra
    return np.argsort(newrank)