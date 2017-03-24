# Author: Yang Long <longyang_123@yeah.net>
#
# License:  LGPL-2.1

import numpy as np
import MultiUtils

class MultiCandidates:
    def __init__(self,popsize,chromesize,func,targetsize,constraints,IntCon,LB,UB,\
                initpopulation,paretofraction,crossoverfraction,mutationrate,\
                createfunction,crossoverfunction,mutationfunction,selectionfunction,fitnessscalingfunction,distancefunction,\
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

        self.crossoverfraction = crossoverfraction
        self.mutationrate = mutationrate
        self.paretofraction = paretofraction

        self.createfunction = createfunction
        self.crossoverfunction = crossoverfunction
        self.mutationfunction = mutationfunction
        self.selectionfunction = selectionfunction
        self.fitnessscalingfunction = fitnessscalingfunction
        self.distancefunction = distancefunction
    
        self.fitness = np.zeros((popsize,targetsize))   # Fitness = Objective + Constraint
        self.objectives = np.zeros((popsize,targetsize))
        self.rank = np.zeros(popsize)
        self.distance = np.zeros(popsize)               
        self.fit()      

    def fit(self):
        '''
        Calculation of Fitness
        '''
        (popsize,chromesize) = self.populations.shape
        rawfitness = np.zeros((popsize,self.targetsize))
        objectives = np.zeros((popsize,self.targetsize))
        for i in range(popsize):
            rawfitness[i] = np.array(self.func(self.populations[i])) \
                + self.constraints.fitness(self.populations[i])*np.ones(self.targetsize)
            objectives[i] = self.func(self.populations[i])
        
        self.objectives = objectives
        self.fitness = self.fitnessscalingfunction(rawfitness,args=self.options.FitnessScale.args)      # Scale the fitness

        self.rank,self.distance = self.distancefunction(self.fitness,args=self.options.Pareto.args)

    def crossover(self):
        '''
        Crossover Operation
        ''' 
        nParents = int(1.0*(1.0 - self.paretofraction)*self.popsize*self.crossoverfraction)
        parentindexs = self.selectionfunction(rank=self.rank,distance=self.distance,nParents=nParents,args=self.options.Selection.args)
        childs = self.crossoverfunction(parents=self.populations[parentindexs],rank=self.rank,distance=self.distance,\
                LB=self.LB,UB=self.UB,IntCon=self.IntCon,args=self.options.Crossover.args)
        return childs

    def mutation(self):
        '''
        Mutation Operation
        '''
        nParents = self.popsize - int(self.popsize*self.paretofraction) - int(1.0*(1.0 - self.paretofraction)*self.popsize*self.crossoverfraction)
        parentindexs = self.selectionfunction(rank=self.rank,distance=self.distance,nParents=nParents,args=self.options.Selection.args)
        childs = self.mutationfunction(chromes=self.populations[parentindexs],rank=self.rank,distance=self.distance,\
                    LB=self.LB,UB=self.UB,IntCon=self.IntCon,mutationrate=self.mutationrate,args=self.options.Mutation.args)
        return childs
    
    def elite(self):
        '''
        Elite Operation
        '''
        if self.paretofraction > 0:
            pos = np.argsort(self.rank)
            popsize = int(self.popsize*self.paretofraction)     # Only some of individuals can be maintained in the frontier
            #if popsize <= sum(1*(self.rank==0)):
            #    popsize = sum(1*(self.rank==0))     
            return self.populations[pos[:popsize]]
        return np.array([])

    def update(self):
        '''
        Populations Evolution
        '''
        if self.verbose:
            print 'Start: ',
        elitechilds = self.elite()

        if self.verbose:
            print 'Pareto({num}) -> '.format(num=np.size(elitechilds,axis=0)),
        crossoverchilds = self.crossover()

        if self.verbose:
            print 'Cross({num}) -> '.format(num=np.size(crossoverchilds,axis=0)),
        mutationchilds = self.mutation()

        if self.verbose:
            print 'Mutate({num}) -> '.format(num=np.size(mutationchilds,axis=0)),
            
        self.populations = np.concatenate((self.populations,elitechilds,crossoverchilds,mutationchilds))
        self.fit()

        nextgenerations = MultiUtils.Pareto.frontier(self.rank,self.distance,self.popsize)
        self.populations = self.populations[nextgenerations]
        self.rank = self.rank[nextgenerations]
        self.distance = self.distance[nextgenerations]
        self.objectives = self.objectives[nextgenerations]
        
        if self.verbose:
            print 'Finished!'

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

    def getfrontier(self):
        self.fit()
        frontier = np.where(self.rank==0)
        return self.populations[frontier],self.objectives[frontier]

    def getallcandidates(self):
        return self.populations

    def getallobjectives(self):
        return self.objectives

    def getdiversity(self):
        # TODO Adjust the rate of mutation based on the diversity in real time
        return 0