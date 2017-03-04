# Author: Yang Long <longyang_123@yeah.net>
#
# License:  LGPL-2.1

import numpy as np
from Constraint import Constraints
from Candidate import Candidates
import Creation
import Selection
import FitnessScale
import Crossover 
import Mutation 

class GA:
    def __init__(self,func,nvars,LB=None,UB=None,IntCon=None,initpopulation=None,maxgeneration=None,popsize=300,\
        stallgenlimit=50,stalltimelimit=None,fitnesslimit=None,timelimit=None,TolCon=1.0*10**-6,TolFun=1.0*10**-6,\
        groupsize=1,migrateforward=True,migrationfraction=0.2,migrationinterval=20,\
        elitecount=2,crossoverfraction=0.8,mutationrate=0.1,\
        verbose=False,parallelized=False):

        self.func = func                        # Function to minimize
        self.chromesize = nvars                 # Number of variants
        self.LB = LB                            # Lower Boundary
        self.UB = UB                            # Upper Boundary
        self.IntCon = IntCon                    # Integer Constraint
        if IntCon is None:                      # Size of populations
            self.popsize = popsize              
        else:
            self.popsize = np.max([15*nvars,popsize])
        self.initpopulation = initpopulation    # Initial Populations
        self.maxgeneration = maxgeneration      # Max Generation to evlove 
        
        self.stallgenlimit = stallgenlimit
        self.stalltimelimit = stalltimelimit
        self.fitnesslimit = fitnesslimit
        self.timelimit = timelimit              # Time Limit to run (in unit of minutes)
        self.TolCon = TolCon
        self.TolFun = TolFun

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

        self.candidates = None                  # Candidates
        self.constraints = Constraints()        # Constraints

        # Default Settings
        self.createfunction = Creation.Uniform
        self.crossoverfunction = Crossover.TwoPoint
        self.mutationfunction = Mutation.Uniform
        self.fitnessscalingfunction = FitnessScale.Rank
        self.selectionfunction = Selection.Tournament
    
    def addconstraint(self,constraintfunc,penalty=1000):
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
        self.candidates = Candidates(popsize=self.popsize,chromesize=self.chromesize,func=self.func,\
                                    constraints=self.constraints,IntCon=self.IntCon,LB=self.LB,UB=self.UB,\
                                    initpopulation=self.initpopulation,Elitecount=self.elitecount,\
                                    crossoverfraction=self.crossoverfraction,mutationrate=self.mutationrate,\
                                    createfunction=self.createfunction,\
                                    crossoverfunction=self.crossoverfunction,\
                                    mutationfunction=self.mutationfunction,\
                                    selectionfunction=self.selectionfunction,\
                                    fitnessscalingfunction=self.fitnessscalingfunction,\
                                    verbose=self.verbose)
        
        if self.maxgeneration is not None:
            for i in range(self.maxgeneration):
                if self.verbose:
                    print '{num}th generation:'.format(num=i+1),
                self.update()
                
                [status,code] = self.check()
                if status:
                    if self.verbose:
                        print 'Optimization terminated: {reason}'.format(reason=code)
                    break
            if self.verbose:
                print 'Optimization terminated: Maximum Generation'
        else:
            generation = 1
            while 1:
                if self.verbose:
                    print '{num}th generation:'.format(num=generation),
                self.update()
                    
                [status,code] = self.check()
                if status:
                    if self.verbose:
                        print 'Optimization terminated: {reason}'.format(reason=code)
                    break

    def update(self):
        return self.candidates.update(tolerance=self.tolerance)

    def migration(self):
        # TODO
        pass

    def getcache(self):
        return self.candidates.getallcandidates(),self.candidates.getallfitness()

    def getsolution(self):
        return self.candidates.getbestcandidate()