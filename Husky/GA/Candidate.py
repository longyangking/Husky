# Author: Yang Long <longyang_123@yeah.net>
#
# License:  LGPL-2.1

import numpy as np

class Candidates:
    def __init__(self,popsize,chromesize,func,constraints,IntCon,LB,UB,\
                initpopulation,Elitecount,crossfraction,mutationrate,\
                createfunction,crossoverfunction,mutationfunction,selectionfunction,fitnessscalingfunction,\
                verbose):
        self.verbose = verbose

        self.popsize = popsize
        self.chromesize = chromesize
        self.func = func
        self.constraints = constraints
        self.IntCon = IntCon
        if LB is not None: 
            self.LB = LB
        else:
            self.LB = -2.0**32*np.ones(chromesize)

        if UB is not None: 
            self.UB = UB
        else:
            self.UB = 2.0**32*np.ones(chromesize)

        if initpopulation is None:
            self.populations = createfunction(popsize=popsize,chromesize=chromesize,LB=self.LB,UB=self.UB,IntCon=IntCon)
            if self.verbose:
                print('Initial Populations have been generated...')
        else:
            self.populations = initpopulation
        self.Elitecount = Elitecount
        self.crossfraction = crossfraction
        self.mutationrate = mutationrate

        self.createfunction = createfunction
        self.crossoverfunction = crossoverfunction
        self.mutationfunction = mutationfunction
        self.selectionfunction = selectionfunction
        self.fitnessscalingfunction = fitnessscalingfunction

        self.fitness = np.zeros(popsize)
        self.scaledfitness = np.zeros(popsize)
        self.fit()

    def fit(self):
        '''
        Calculation of Fitness
        '''
        rawfitness = np.zeros(self.popsize)
        for i in range(self.popsize):
            rawfitness[i] = self.func(self.populations[i]) \
                + self.constraints.fitness(self.populations[i])
            self.fitness[i] = self.func(self.populations[i])
        # Sacle the raw fitness into scaled fitness
        self.scaledfitness = self.fitnessscalingfunction(rawfitness)

    def crossover(self):
        '''
        Crossover Operation
        ''' 
        nParents = np.floor(1.0*(self.popsize - self.Elitecount)*self.crossfraction)
        parentindexs = self.selectionfunction(fitness=self.scaledfitness,nParents=nParents)
        childs = self.crossoverfunction(parents=self.populations[parentindexs],fitness=self.scaledfitness,\
                LB=self.LB,UB=self.UB,IntCon=self.IntCon)
        return childs

    def mutation(self):
        '''
        Mutation Operation
        '''
        nParents = self.popsize - self.Elitecount - np.floor(1.0*(self.popsize - self.Elitecount)*self.crossfraction)
        parentindexs = self.selectionfunction(fitness=self.scaledfitness,nParents=nParents)
        childs = self.mutationfunction(chromes=self.populations[parentindexs],\
                    LB=self.LB,UB=self.UB,IntCon=self.IntCon,mutationrate=self.mutationrate)
        return childs
    
    def elite(self):
        '''
        Elite Operation
        '''
        if self.Elitecount > 0:
            pos = np.argsort(self.scaledfitness)
            return self.populations[pos[:self.Elitecount]]
        return np.array([])

    def update(self):
        if self.verbose:
            print 'Start: Elite -> ',
        elitechilds = self.elite()

        if self.verbose:
            print 'Cross -> ',
        crossoverchilds = self.crossover()

        if self.verbose:
            print 'Mutate -> ',
        mutationchilds = self.mutation()

        self.populations = np.concatenate((elitechilds,crossoverchilds,mutationchilds))
        #self.populations = self.populations[np.argsort(self.fitness)[:self.popsize]]
        # Whether allow the competetion between parents and childs
        self.fit()
        if self.verbose:
            print 'Finished!'

    def check(self,stallgenlimit,stalltimelimit,fitnesslimit,TolCon,TolFun):

        return False,None

    def getbestcandidate(self):
        bestcandidate = np.argmax(self.scaledfitness)
        return self.populationsbestcandidate],self.fitness[bestcandidate]

    def getallcandidates(self):
        return self.populations

    def getallfitness(self):
        return self.fitness