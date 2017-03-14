# Author: Yang Long <longyang_123@yeah.net>
#
# License:  LGPL-2.1

import numpy as np

class Candidates:
    def __init__(self,popsize,chromesize,func,constraints,IntCon,LB,UB,\
                initpopulation,Elitecount,crossoverfraction,mutationrate,\
                createfunction,crossoverfunction,mutationfunction,selectionfunction,fitnessscalingfunction,\
                verbose,options):
        self.verbose = verbose
        self.options = options
        self.popsize = popsize
        self.chromesize = chromesize
        self.func = func
        self.constraints = constraints
        self.IntCon = IntCon
        if LB is not None: 
            self.LB = LB
        else:
            self.LB = -10.0*np.ones(chromesize)              # Initial LB would make a huge influence about the optimization

        if UB is not None: 
            self.UB = UB
        else:
            self.UB = 10.0*np.ones(chromesize)

        if initpopulation is None:
            self.populations = createfunction(popsize=popsize,chromesize=chromesize,\
                            LB=self.LB,UB=self.UB,IntCon=IntCon,args=self.options.Creation.args)
            if self.verbose:
                print('Initial Populations have been generated...')
        else:
            self.populations = initpopulation
        self.Elitecount = Elitecount
        self.crossoverfraction = crossoverfraction
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
        self.scaledfitness = self.fitnessscalingfunction(rawfitness,args=self.options.FitnessScale.args)

    def crossover(self):
        '''
        Crossover Operation
        ''' 
        nParents = int(1.0*(self.popsize - self.Elitecount)*self.crossoverfraction)
        parentindexs = self.selectionfunction(fitness=self.scaledfitness,nParents=nParents,args=self.options.Selection.args)
        childs = self.crossoverfunction(parents=self.populations[parentindexs],fitness=self.scaledfitness,\
                LB=self.LB,UB=self.UB,IntCon=self.IntCon,args=self.options.Crossover.args)
        return childs

    def mutation(self):
        '''
        Mutation Operation
        '''
        nParents = self.popsize - self.Elitecount - int(1.0*(self.popsize - self.Elitecount)*self.crossoverfraction)
        parentindexs = self.selectionfunction(fitness=self.scaledfitness,nParents=nParents,args=self.options.Selection.args)
        childs = self.mutationfunction(chromes=self.populations[parentindexs],\
                    LB=self.LB,UB=self.UB,IntCon=self.IntCon,mutationrate=self.mutationrate,args=self.options.Mutation.args)
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
        '''
        Populations Evolution
        '''
        if self.verbose:
            print 'Start: ',
        elitechilds = self.elite()

        if self.verbose:
            print 'Elite({num}) -> '.format(num=np.size(elitechilds)),
        crossoverchilds = self.crossover()

        if self.verbose:
            print 'Cross({num}) -> '.format(num=np.size(crossoverchilds)),
        mutationchilds = self.mutation()

        if self.verbose:
            print 'Mutate({num}) -> '.format(num=np.size(mutationchilds)),
            
        self.populations = np.concatenate((elitechilds,crossoverchilds,mutationchilds))
        #self.populations = self.populations[np.argsort(self.fitness)[:self.popsize]]
        # Whether allow the competetion between parents and childs
        self.fit()
        if self.verbose:
            print 'Finished! Diversity:',self.getdiversity()

    def migrateout(self,popsize):
        '''
        Select members to migrate out from this populations
        '''
        selected = np.random.randint(self.popsize,size=popsize)
        return self.populations[selected],selected

    def migratein(self,position,populations):
        '''
        Migrate some external members from other populations
        '''
        self.populations[position] = populations
        return True

    def getbestcandidate(self):
        bestcandidate = np.argmax(self.scaledfitness)
        return self.populations[bestcandidate],self.fitness[bestcandidate]

    def getallcandidates(self):
        return self.populations

    def getallfitness(self):
        return self.fitness

    def getdiversity(self):
        delta = np.std(self.populations,axis=0)
        average = np.abs(np.mean(self.populations,axis=0))
        diversity =  np.sum(delta/average)/np.size(delta)
        return diversity

class MultiCandidates:
    def __init__(self,popsize,chromesize,func,targetsize,constraints,IntCon,LB,UB,\
                initpopulation,Elitecount,crossoverfraction,mutationrate,\
                createfunction,crossoverfunction,mutationfunction,selectionfunction,fitnessscalingfunction,\
                verbose,options):
        self.verbose = verbose
        self.options = options
        self.popsize = popsize
        self.chromesize = chromesize
        self.targetsize = targetsize
        self.func = func
        self.constraints = constraints
        self.IntCon = IntCon
        if LB is not None: 
            self.LB = LB
        else:
            self.LB = -10.0*np.ones(chromesize)              # Initial LB would make a huge influence about the optimization

        if UB is not None: 
            self.UB = UB
        else:
            self.UB = 10.0*np.ones(chromesize)

        if initpopulation is None:
            self.populations = createfunction(popsize=popsize,chromesize=chromesize,\
                            LB=self.LB,UB=self.UB,IntCon=IntCon,args=self.options.Creation.args)
            if self.verbose:
                print('Initial Populations have been generated...')
        else:
            self.populations = initpopulation
        self.Elitecount = Elitecount
        self.crossoverfraction = crossoverfraction
        self.mutationrate = mutationrate

        self.createfunction = createfunction
        self.crossoverfunction = crossoverfunction
        self.mutationfunction = mutationfunction
        self.selectionfunction = selectionfunction
        self.fitnessscalingfunction = fitnessscalingfunction
    
        self.fitness = np.zeros((popsize,targetsize))
        self.scaledfitness = np.zeros((popsize,targetsize))
        self.fit()

    def sort(self):
        front = 1
        F = list()
        individualn = np.zeros(self.popsize)
        individualp = list()
        for i in range(self.popsize):
            dominateset = list()
            for j in range(self.popsize):
                dom_less = 0
                dom_equal = 0
                dom_more = 0
                for k in range(self.targetsize):
                    if self.fitness
    
        # TODO Scaled Fitness will be based on Non-dominated sort


    def fit(self):
        '''
        Calculation of Fitness
        '''
        rawfitness = np.zeros((self.targetsize,self.popsize))
        for i in range(self.popsize):
            rawfitness[i] = self.func(self.populations[i]) \
                + self.constraints.fitness(self.populations[i])*np.ones(self.targetsize)
            self.fitness[i] = self.func(self.populations[i])
    
        # Sacle the raw fitness into scaled fitness
        for i in range(self.targetsize):
            self.scaledfitness[:,i] = self.fitnessscalingfunction(rawfitness[:,i].flatten(),args=self.options.FitnessScale.args)

    def crossover(self):
        '''
        Crossover Operation
        ''' 
        nParents = int(1.0*(self.popsize - self.Elitecount)*self.crossoverfraction)
        parentindexs = self.selectionfunction(fitness=self.scaledfitness,nParents=nParents,args=self.options.Selection.args)
        childs = self.crossoverfunction(parents=self.populations[parentindexs],fitness=self.scaledfitness,\
                LB=self.LB,UB=self.UB,IntCon=self.IntCon,args=self.options.Crossover.args)
        return childs

    def mutation(self):
        '''
        Mutation Operation
        '''
        nParents = self.popsize - self.Elitecount - int(1.0*(self.popsize - self.Elitecount)*self.crossoverfraction)
        parentindexs = self.selectionfunction(fitness=self.scaledfitness,nParents=nParents,args=self.options.Selection.args)
        childs = self.mutationfunction(chromes=self.populations[parentindexs],\
                    LB=self.LB,UB=self.UB,IntCon=self.IntCon,mutationrate=self.mutationrate,args=self.options.Mutation.args)
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
        '''
        Populations Evolution
        '''
        if self.verbose:
            print 'Start: ',
        elitechilds = self.elite()

        if self.verbose:
            print 'Elite({num}) -> '.format(num=np.size(elitechilds)),
        crossoverchilds = self.crossover()

        if self.verbose:
            print 'Cross({num}) -> '.format(num=np.size(crossoverchilds)),
        mutationchilds = self.mutation()

        if self.verbose:
            print 'Mutate({num}) -> '.format(num=np.size(mutationchilds)),
            
        self.populations = np.concatenate((elitechilds,crossoverchilds,mutationchilds))
        #self.populations = self.populations[np.argsort(self.fitness)[:self.popsize]]
        # Whether allow the competetion between parents and childs
        self.fit()
        if self.verbose:
            print 'Finished! Diversity:',self.getdiversity()

    def migrateout(self,popsize):
        '''
        Select members to migrate out from this populations
        '''
        selected = np.random.randint(self.popsize,size=popsize)
        return self.populations[selected],selected

    def migratein(self,position,populations):
        '''
        Migrate some external members from other populations
        '''
        self.populations[position] = populations
        return True

    def getbestcandidate(self):
        bestcandidate = np.argmax(self.scaledfitness)
        return self.populations[bestcandidate],self.fitness[bestcandidate]

    def getallcandidates(self):
        return self.populations

    def getallfitness(self):
        return self.fitness

    def getdiversity(self):
        delta = np.std(self.populations,axis=0)
        average = np.abs(np.mean(self.populations,axis=0))
        diversity =  np.sum(delta/average)/np.size(delta)
        return diversity
