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