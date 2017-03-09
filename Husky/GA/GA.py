# Author: Yang Long <longyang_123@yeah.net>
#
# License:  LGPL-2.1

import numpy as np
import time

from Constraint import Constraints
from Candidate import Candidates
import Creation
import Selection
import FitnessScale
import Crossover 
import Mutation

class GA:
    def __init__(self,func,nvars,LB=None,UB=None,IntCon=None,initpopulation=None,maxgeneration=None,popsize=300,\
        stallgenlimit=100,stalltimelimit=None,fitnesslimit=None,timelimit=None,TolCon=1.0*10**-6,TolFun=1.0*10**-6,diversitylimit=0.05,\
        groupsize=1,migrateforward=True,migrationfraction=0.2,migrationinterval=20,\
        elitecount=2,crossoverfraction=0.8,mutationrate=0.1,\
        verbose=False,parallelized=False):

        self.func = func                        # Function to minimize
        self.chromesize = nvars                 # Number of variants

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
        self.fitnesslimit = fitnesslimit
        self.timelimit = timelimit              # Time Limit to run (in unit of seconds)
        self.TolCon = TolCon
        self.TolFun = TolFun
        self.diversitylimit = diversitylimit

        self.groupsize = groupsize
        self.migrateforward = migrateforward
        self.migrationfraction = migrationfraction
        self.migrationinterval = migrationinterval

        if IntCon is None:                      # Elite Count
            self.elitecount = elitecount
        else:
            self.elitecount = np.min([np.max([nvars,2]),5])
        self.crossoverfraction = crossoverfraction
        self.mutationrate = mutationrate

        self.verbose = verbose                  # Print Computational Info
        self.parallelized = parallelized

        self.candidates = list()                # Candidates
        self.candidatestatus = np.zeros(groupsize)
        self.constraints = Constraints()        # Constraints

        # Default Settings
        self.createfunction = Creation.Uniform
        self.crossoverfunction = Crossover.TwoPoint
        self.mutationfunction = Mutation.Uniform
        self.fitnessscalingfunction = FitnessScale.Rank
        self.selectionfunction = Selection.Tournament

        # Stall Limit
        self.stallfitness = list()
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
            self.candidates.append(Candidates(popsize=self.popsize,chromesize=self.chromesize,func=self.func,\
                                        constraints=self.constraints,IntCon=self.IntCon,LB=self.LB,UB=self.UB,\
                                        initpopulation=self.initpopulation,Elitecount=self.elitecount,\
                                        crossoverfraction=self.crossoverfraction,mutationrate=self.mutationrate,\
                                        createfunction=self.createfunction,\
                                        crossoverfunction=self.crossoverfunction,\
                                        mutationfunction=self.mutationfunction,\
                                        selectionfunction=self.selectionfunction,\
                                        fitnessscalingfunction=self.fitnessscalingfunction,\
                                        verbose=self.verbose))
            self.candidatestatus[i] = 0
            self.stallfitness.append(None)
        
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
            fitness = self.candidates[i].getallfitness()
            
            # Fitness Limit
            if self.fitnesslimit is not None:
                if np.min(fitness) < self.fitnesslimit:
                    self.candidatestatus[i] = 1             # Fitness Limit
            
            if self.stallfitness[i] is None:
                self.stallfitness[i] = fitness
                activecount += 1
                continue
            
            # Calculate Stall Generation
            averagechange = np.abs(np.min(fitness)-np.min(self.stallfitness[i]))
            if averagechange < self.TolFun:
                self.stallgeneration[i] += 1
                self.stalltime[i] = self.stalltime[i] + time.time() - self.stallstarttime[i]
                #if self.verbose:
                #    print ' -> Start stall: Generation {generation}th '.format(generation=self.stallgeneration)
            else:
                self.stallgeneration[i] = 0
                self.stallstarttime[i] = time.time()
                self.stalltime[i] = 0
                self.stallfitness[i] = fitness
            
            # Stall Generation Limit
            if self.stallgeneration[i] > self.stallgenlimit:
                self.candidatestatus[i] = 2                 # Stall Gen Limit
                
            if self.candidates[i].getdiversity() < self.diversitylimit:
                self.candidatestatus[i] = 3                 # Diversity Limit

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
                    code += '{num}th group -> {reason}\n'.format(num=i+1,reason='Fitness Limit')
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
        fitness = np.zeros(self.popsize*self.groupsize)
        for i in range(self.groupsize):
            solutions[(i)*self.popsize:(i+1)*self.popsize,:] = self.candidates[i].getallcandidates()
            fitness[(i)*self.popsize:(i+1)*self.popsize] = self.candidates[i].getallfitness()
        return solutions,fitness

    def getsolution(self):
        solutions = np.zeros((self.groupsize,self.chromesize))
        fitness = np.zeros(self.groupsize)
        for i in range(self.groupsize):
            (solutions[i],fitness[i]) = self.candidates[i].getbestcandidate()
        bestpos = np.argmin(fitness)
        return solutions[bestpos],fitness[bestpos]