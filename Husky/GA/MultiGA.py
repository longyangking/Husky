# Author: Yang Long <longyang_123@yeah.net>
#
# License:  LGPL-2.1

import numpy as np
import time

from Constraint import Constraints
from MultiCandidate import MultiCandidates
import MultiUtils

class MultiGA:
    '''
    NSGA-II
    '''
    def __init__(self,func,targetsize,nvars,LB=None,UB=None,IntCon=None,initpopulation=None,maxgeneration=None,popsize=300,\
        stallgenlimit=100,stalltimelimit=None,objectiveslimit=None,timelimit=None,TolCon=1.0*10**-6,TolFun=1.0*10**-6,diversitylimit=0.05,\
        groupsize=1,migrateforward=True,migrationfraction=0.2,migrationinterval=20,\
        paretofraction=0.01,crossoverfraction=0.8,mutationrate=0.1,\
        verbose=False,parallelized=False,options=None):

        self.func = func                      # Function to minimize
        self.chromesize = nvars                 # Number of variants
        self.targetsize = targetsize

        # Lower Boundary
        if LB is not None:
            self.LB = np.array(LB)
        else:
            self.LB = LB   
        # Upper Boundary
        if UB is not None:
            self.UB = np.array(UB)
        else:
            self.UB = UB       
        # Integer Constraint
        if IntCon is not None:
            self.IntCon = np.array(IntCon)
        else:
            self.IntCon = IntCon 

        if IntCon is None:                      # Size of populations
            self.popsize = popsize              
        else:
            self.popsize = np.max([15*nvars,popsize])
        self.initpopulation = initpopulation    # Initial Populations
        self.maxgeneration = maxgeneration      # Max Generation to evlove 
        
        self.stallgenlimit = stallgenlimit
        self.stalltimelimit = stalltimelimit
        if objectiveslimit is not None:
            self.objectiveslimit = np.array(objectiveslimit)
        else:
            self.objectiveslimit = objectiveslimit

        self.timelimit = timelimit              # Time Limit to run (in unit of seconds)
        self.TolCon = TolCon
        self.TolFun = TolFun
        self.diversitylimit = diversitylimit

        self.groupsize = groupsize
        self.migrateforward = migrateforward
        self.migrationfraction = migrationfraction
        self.migrationinterval = migrationinterval

        
        self.paretofraction = paretofraction
        self.crossoverfraction = crossoverfraction
        self.mutationrate = mutationrate

        self.verbose = verbose                  # Print Computational Info
        self.parallelized = parallelized
        if options is not None:
            self.options = options
        else:
            self.options = MultiUtils.MultiGAoptions.MultiGAoptions()

        self.candidates = list()                # Candidates
        self.candidatestatus = np.zeros(groupsize)
        self.constraints = Constraints()        # Constraints

        # Default Settings
        self.createfunction = MultiUtils.Creation.Uniform
        self.crossoverfunction = MultiUtils.Crossover.TwoPoint
        self.mutationfunction = MultiUtils.Mutation.Uniform
        self.fitnessscalingfunction = MultiUtils.FitnessScale.Rank
        self.selectionfunction = MultiUtils.Selection.Tournament
        self.distancefunction = MultiUtils.Pareto.FastNonDominatedSorting

        # Stall Limit
        self.stallobjectives = list()
        self.stallgeneration = np.zeros(groupsize)
        self.stallstarttime = np.zeros(groupsize)
        self.stalltime = np.zeros(groupsize)
    
    def addconstraint(self,constraintfunc,penalty=10):
        self.constraints.add(constraintfunc,penalty)

    def setparameter(self,parameter,value):
        if parameter == 'createfunction':
            if value == 'Uniform':
                self.createfunction = Creation.Uniform
            else:
                return False
            return True
        if parameter == 'crossoverfunction':
            if value == 'Laplacian':
                self.crossoverfunction = Crossover.Laplacian
            elif value == 'Scattered':
                self.crossoverfunction = Crossover.Scattered
            elif value == 'SinglePoint':
                self.crossoverfunction = Crossover.SinglePoint
            elif value == 'TwoPoint':
                self.crossoverfunction = Crossover.TwoPoint
            elif value == 'Intermediate':
                self.crossoverfunction = Crossover.Intermediate
            elif value == 'Heuristic':
                self.crossoverfunction = Crossover.Heuristic
            else:
                return False
            return True
        if parameter == 'fitnessscalingfunction':
            if value == 'Rank':
                self.fitnessscalingfunction = FitnessScale.Rank
            elif value == 'Proportional':
                self.fitnessscalingfunction = FitnessScale.Proportional
            elif value == 'ShiftLiner':
                self.fitnessscalingfunction = FitnessScale.ShiftLiner
            elif value == 'Top':
                self.fitnessscalingfunction = FitnessScale.Top
            else:
                return False
            return True
        if parameter == 'mutationfunction':
            if value == 'Uniform':
                self.mutationfunction = Mutation.Uniform
            elif value == 'Gaussian':
                self.mutationfunction = Mutation.Gaussian
            else:
                return False
            return True
        if parameter == 'selectionfunction':
            if value == 'Tournament':
                self.selectionfunction = Selection.Tournament
            elif value == 'StochasticUniform':
                self.selectionfunction = Selection.StochasticUniform
            elif value == 'Remainder':
                self.selectionfunction = Selection.Reminder
            elif value == 'Roulette':
                self.selectionfunction = Selection.Roulette
            else:
                return False
            return True
        return False

    def start(self):
        '''
        Main function to start GA
        '''
        starttime = time.time()
        for i in range(self.groupsize):
            self.candidates.append(MultiCandidates(popsize=self.popsize,chromesize=self.chromesize,func=self.func,targetsize=self.targetsize,\
                                        constraints=self.constraints,IntCon=self.IntCon,LB=self.LB,UB=self.UB,\
                                        initpopulation=self.initpopulation,paretofraction=self.paretofraction,\
                                        crossoverfraction=self.crossoverfraction,mutationrate=self.mutationrate,\
                                        createfunction=self.createfunction,\
                                        crossoverfunction=self.crossoverfunction,\
                                        mutationfunction=self.mutationfunction,\
                                        selectionfunction=self.selectionfunction,\
                                        fitnessscalingfunction=self.fitnessscalingfunction,\
                                        distancefunction=self.distancefunction,\
                                        verbose=self.verbose,options=self.options))
            self.candidatestatus[i] = 0
            self.stallobjectives.append(None)
        
        if self.maxgeneration is not None:
            for i in range(self.maxgeneration):
                if self.verbose:
                    print '{num}th generation:'.format(num=i+1)
                self.update()
                
                [status,code] = self.check()
                # Terminate by the tolerance
                if status:
                    if self.verbose:
                        print 'Optimization terminated: \n{reason}'.format(reason=code)
                    break

                if (i+1)%self.migrationinterval == 0:
                    self.migrate()
                    if self.verbose:
                        print '----Migration----'

                # Terminate by the time limit
                if self.timelimit is not None:
                    currenttime = time.time()
                    if currenttime-starttime > self.timelimit:
                        if self.verbose:
                            print 'Optimization terminated: Time Limit!'
                        break
            if self.verbose:
                print 'Optimization terminated: Maximum Generation'
        else:
            generation = 1
            while 1:
                if self.verbose:
                    print '{num}th generation:'.format(num=generation)
                self.update()
                    
                [status,code] = self.check()
                # Terminate by the tolerance
                if status:
                    if self.verbose:
                        print 'Optimization terminated: \n{reason}'.format(reason=code)
                    break

                if generation%self.migrationinterval == 0:
                    self.migrate()
                    if self.verbose:
                        print '----Migration----'

                # Terminate by the time limit
                if self.timelimit is not None:
                    currenttime = time.time()
                    if currenttime-starttime > self.timelimit:
                        if self.verbose:
                            print 'Optimization terminated: Time Limit!'
                        break
                
                generation += 1

    def check(self):
        '''
        Check tolerance of populations
        '''
        activecount = 0
        for i in range(self.groupsize):
            objectives = self.candidates[i].getallobjectives()
            
            # Objectives Limit
            if self.objectiveslimit is not None:
                if np.sum(np.min(objectives,axis=0) < self.objectiveslimit) == sself.targetsize:
                    self.candidatestatus[i] = 1             # Objectives Limit
            
            if self.stallobjectives[i] is None:
                self.stallobjectives[i] = objectives
                activecount += 1
                continue
            
            # Calculate Stall Generation
            averagechange = np.sum(np.mean(objectives,axis=0)-np.mean(self.stallobjectives[i],axis=0))
            base = np.sum(np.min(self.stallobjectives[i],axis=0))
            if (averagechange/base < self.TolFun) and (len(objectives) > 1):
                self.stallgeneration[i] += 1
                self.stalltime[i] = self.stalltime[i] + time.time() - self.stallstarttime[i]
                #if self.verbose:
                #    print ' -> Start stall: Generation {generation}th '.format(generation=self.stallgeneration)
            else:
                self.stallgeneration[i] = 0
                self.stallstarttime[i] = time.time()
                self.stalltime[i] = 0
                self.stallobjectives[i] = objectives
            
            # Stall Generation Limit
            if self.stallgeneration[i] > self.stallgenlimit:
                self.candidatestatus[i] = 2                 # Stall Gen Limit
                
            #if self.candidates[i].getdiversity() < self.diversitylimit:
            #    self.candidatestatus[i] = 3                 # Diversity Limit

            # Stall Time Limit
            if self.stalltimelimit is not None:
                if self.stalltime[i] > self.stalltimelimit:
                    self.candidatestatus[i] = 4             # Stall Time Limit

            if self.candidatestatus[i] == 0:
                activecount += 1                            # Some group still alive

        if activecount >= 1:
            return False,None
        else:
            code = str()
            for i in range(self.groupsize):
                if self.candidatestatus[i] == 1:
                    code += '{num}th group -> {reason}\n'.format(num=i+1,reason='Objectives Limit')
                elif self.candidatestatus[i] == 2:
                    code += '{num}th group -> {reason}\n'.format(num=i+1,reason='Stall Generation Limit')
                elif self.candidatestatus[i] == 3:
                    code += '{num}th group -> {reason}\n'.format(num=i+1,reason='Diversity Limit')
                elif self.candidatestatus[i] == 4:
                    code += '{num}th group -> {reason}\n'.format(num=i+1,reason='Stall Time Limit')
            return True,code
        
    def update(self):
        '''
        Evolve every generation
        '''
        for i in range(self.groupsize):
            if self.candidatestatus[i] == 0:             # Candidate[i] is on Active State
                self.candidates[i].update()

    def migrate(self):
        '''
        Migrate subpopulations
        '''
        popsize = int(self.popsize*self.migrationfraction)
        if self.migrateforward:
            for i in range(self.groupsize):
                (population1,source1) = self.candidates[i].migrateout(popsize)
                if i+1<self.groupsize:
                    (population2,source2) = self.candidates[i+1].migrateout(popsize)
                    self.candidates[i].migratein(source2,population2)
                    self.candidates[i+1].migratein(source1,population1)
                else:
                    (population2,source2) = self.candidates[0].migrateout(popsize)
                    self.candidates[i].migratein(source2,population2)
                    self.candidates[0].migratein(source1,population1)
        else:
            for i in range(self.groupsize,-1,-1):
                (population1,source1) = self.candidates[i].migrateout(popsize)
                if i-1>=0:
                    (population2,source2) = self.candidates[i-1].migrateout(popsize)
                    self.candidates[i].migratein(source2,population2)
                    self.candidates[i-1].migratein(source1,population1)
                else:
                    (population2,source2) = self.candidates[self.groupsize].migrateout(popsize)
                    self.candidates[i].migratein(source2,population2)
                    self.candidates[self.groupsize].migratein(source1,population1)

    def getcache(self):
        solutions = np.zeros((self.popsize*self.groupsize,self.chromesize))
        objectives = np.zeros(self.popsize*self.groupsize,self.targetsize)
        for i in range(self.groupsize):
            solutions[(i)*self.popsize:(i+1)*self.popsize,:] = self.candidates[i].getallcandidates()
            objectives[(i)*self.popsize:(i+1)*self.popsize,:] = self.candidates[i].getallobjectives()
        return solutions,objectives

    def getsolution(self):
        solutions = list()
        objectives = list()
        for i in range(self.groupsize):
            (solution,objective) = self.candidates[i].getfrontier()
            popsize = np.size(solution,axis=0)
            for j in range(popsize):
                solutions.append(solution[j])
                objectives.append(objective[j])

        return np.array(solutions),np.array(objectives)
