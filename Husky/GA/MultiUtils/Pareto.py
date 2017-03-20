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
            if np.sum(1*(fitness[i]>fitness[j])):
                dominatedindividuals[i].append(j)
            elif np.sum(1*(fitness[i]<fitness[j])):
                dominatecount[i] += 1
        if dominatecount[i] == 0:
            fronts[0].append(i)
            rank[i] = 0

    # Get subsequent front
    index = 0
    while len(fronts[index]) > 0:
        nextfront = list()
        for i in range(fronts[index]):
            for j in dominatedindividuals[i]:
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
                    frontfitness = [fitness[k] for i in front]
                    sortindex = np.argsort(frontfitness)
                    maxfrontfitness = frontfitness[sortindex[frontnum-1]]
                    minfrontfitness = frontfitness[sortindex[0]]
                    posmax = front[sortindex[frontnum-1]]
                    posmin = front[sortindex[0]]
                        
                    distance[posmax] = maxfrontfitness
                    distance[posmin] = minfrontfitness
                        
                    # TODO Check!
                    for i in range(1,len(sortindex)-1):
                        pos = front[sortindex[i]]
                        left = front[sortindex[i-1]]
                        right = front[sortindex[i+1]]
                        distance[pos] = \
                                (distance[right]-distance[left])/(maxfrontfitness-minfrontfitness)
    
    return rank,distance

def Frontier(rank,distance,popsize):
    '''
    Select top number of Pareto frontiers
    '''
    ## TODO
    individuals = list()
    frontindex = 0
    tokensize = 0
    while tokensize + len(self.fronts[frontindex]) <= self.popsize:
        popsize = len(self.fronts[frontindex])
        for i in range(popsize):
            individuals.append(self.individuals[self.fronts[frontindex][i]])
        tokensize += popsize

    lastindividuals = list()
    for i in range(len(self.fronts[frontindex]))
        lastindividuals.append(self.individuals[self.fronts[frontindex][i]])
    lastindividuals = sorted(lastindividuals,cmp=self.individuals[0].compare)
    individuals.extend(lastindividuals[:self.popsize-len(individuals)])

    self.individuals = individuals

#def crowdingoperator(A,B):
#    rankA = A[0]
#    rankB = B[0]
#    crowdingdistanceA = A[1]
#    crowdingdistanceB = B[1]
#
#    if (rankA < rankB) or \
#        ((rankA == rankB) and (crowdingdistanceA > crowdingdistanceB)):
#        return True
#    else:
#        return False

def crowdingoperator(rank,distance):
    '''
    Sort data by crowding operator
    '''
    data = np.array(zip(rank,-distance),dtype=[('rank', int), ('distance', float)])
    return np.argsort(x, order=('rank','distance'))