import numpy as np
import random

class Individual:
    def __init__(self,chromes,targetsize,LB,UB,IntCon):
        self.rank = None
        self.crowdingdistance = None
        self.dominatedindividuals = list()
        self.dominatecount = None
        self.chromes = chromes
        self.objectives = np.zeros(targetsize)
        self.LB = LB
        self.UB = UB
        self.IntCon = IntCon

    def dominate(self,individual):
        '''
        To decide whether this individual dominate other individual
        '''
        num = np.sum(1*(self.objectives >= individual.objectives))
        if num == targetsize:
            return True
        return False

    def compare(self,A,B):
        if (A.rank < B.rand) or ((A.rank == B.rank) and (A.crowdingdistance > B.crowdingdistance)):
            return 1
        else:
            return -1

    def restrict(self):
        if self.IntCon is not None:
            intchromes = np.floor(self.chromes[self.IntCon])
            intchromes = intchromes + 1*(np.random.random(size=np.size(intchromes))>0.5)
            self.chromes[self.IntCon] = intchromes

        posLB = np.where(self.chromes<LB)
        self.chromes[posLB] = LB[posLB]

        posUB = np.where(self.chromes>UB)
        self.chromes[posUB] = UB[posUB]


class Crossover:
    def __init__(self):
        # TODO some system parameters setting

        pass

    def TwoPoints(parents):
        childs = list()
        

class Mutation:
    def __init__(self):
        # TODO some system parameters setting
        pass

class Pareto:
    def __init__(self):
        # TODO some system parameters setting
        self.DistanceType = 'phenotype'
    
    def Sort(self):
        '''
        Fast non-dominated sorting

        Reference:
            Deb K, Pratap A, Agarwal S, et al. 
            A fast and elitist multiobjective genetic algorithm: NSGA-II[J]. 
            IEEE transactions on evolutionary computation, 2002, 6(2): 182-197.

        '''
        self.fronts = list()
        self.fronts.append([])  # First Front is Blank

        # Get first front firstly
        for i in range(self.popsize):
            self.individuals[i].dominatedindividuals = list()
            self.individuals[i].dominatecount = 0

            for j in range(self.popsize):
                if self.individuals[i].dominate(self.individuals[j]):
                    self.individuals[i].dominatedindividuals.add(i)
                elif self.individuals[j].dominate(self.individuals[i]):
                    self.individuals[i].dominatecount += 1
            if self.individuals[i].dominatecount == 0:
                self.fronts[0].append(i)
                self.individuals[i].rank = 0

        # Get subsequent front
        index = 0
        while len(self.fronts[index]) > 0:
            nextfront = list()
            for i in range(self.fronts[index]):
                for j in self.individuals[i].dominatedindividuals:
                    self.individuals[j].dominatecount -= 1
                    if self.individuals[j].dominatecount == 0:
                        self.individuals[j].rank = index + 1
                        nextfront.append(j)
            index += 1
            self.fronts.append(nextfront)

    def CrowdingDistant(self):
        if len(self.fronts) > 0:
            for index in range(len(self.fronts)):
                front = self.fronts[index]
                frontnum = len(front)
                if frontnum > 0:
                    for m in front:
                        self.individuals[m].crowdingdistance = 0

                    # TODO need check
                    for k in range(self.targetsize):
                        objectives = [self.individuals[i].objectives[k] for i in front]
                        sortindex = np.argsort(objectives)
                        maxobjective = objectives[sortindex[frontnum-1]]
                        minobjective = objectives[sortindex[0]]
                        posmax = front[sortindex[frontnum-1]]
                        posmin = front[sortindex[0]]
                        
                        self.individuals[posmax].crowdingdistance = maxobjective
                        self.individuals[posmin].crowdingdistance = minobjective
                        
                        # TODO Check!
                        for i in range(1,len(sortindex)-1):
                            pos = front[sortindex[i]]
                            left = front[sortindex[i-1]]
                            right = front[sortindex[i+1]]
                            self.individuals[pos].crowdingdistance = \
                                (self.individuals[right].crowdingdistance-self.individuals[left].crowdingdistance)/(maxobjective-minobjective)

    def Frontier(self):
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

class Selection:
    def __init__(self):
        # TODO some system parameters setting
        self.tournamentsize = 3

    def Tournament(self,individuals,nParents):
        childs = list()
        for i in range(nParents):
            parents = random.sample(individuals,self.tournamentsize)
            best = parents[0]
            for parent in parents:
                if (best is None) or (best.compare(parent,best)):
                    best = parent
            childs.append(best)
        return childs

class CreateChildrens:
    def __init__(self):
        # TODO some system parameters setting
        pass