# Author: Yang Long <longyang_123@yeah.net>
#
# License:  LGPL-2.1

import numpy as np

class Individual:
    def __init__(self,chromes,targetsize):
        self.rank = None
        self.crowdingdistance = None
        self.dominatedindividuals = list()
        self.dominatecount = None
        self.chromes = chromes
        self.objectives = np.zeros(targetsize)

    def dominate(self,individual):
        '''
        To decide whether this individual dominate other individual
        '''
        num = np.sum(1*(self.objectives >= individual.objectives))
        if num == targetsize:
            return True
        return False

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
    
    def calcrowdingdistance(self):
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

    def crowding(self):
        pass

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
