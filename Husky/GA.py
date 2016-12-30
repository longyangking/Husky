# Author: Yang Long <longyang_123@yeah.net>
#
# License:  LGPL-2.1

import numpy as np
from Constraint import Constraints
from Candidate import Candidates

class GA:
    def __init__(self,fitnessfunc,nvars,LB=None,UB=None,IntCon=None,initpopulation=None,timelimit=None,maxgeneration=100,popsize=60):
        self.chromesize = nvars                 # Number of variants
        self.timelimit = timelimit              # Time Limit to run
        self.maxgeneration = maxgeneration      # Max Generation to evlove
        self.constraints = Constraints()        # Constraints
        self.popsize = popsize                  # Size of populations
        self.fitnessfunc = fitnessfunc          # Function to calculate fitness
        self.candidates = None                  # Candidates
        self.LB = LB                            # Lower Boundary
        self.UB = UB                            # Upper Boundary
        self.IntCon = IntCon                    # Integer Constraint
        self.initpopulation = initpopulation    # Initial Population
    
    def addconstraint(self,constraintfunc,penalty=100):
        self.constraints.add(constraintfunc,penalty)

    def setparameter(self,parameter,value):
        if parameter == 'timelimit':
            self.timelimit = value
            return True
        if parameter == 'maxgeneration':
            self.maxgeneration = value
            return True
        return False

    def start(self):
        self.candidates = Candidates(self.popsize,self.chromesize,self.fitnessfunc,constraints=self.constraints,IntCon=self.IntCon,LB=self.LB,UB=self.UB,initpopulation=self.initpopulation):
        for i in range(self.maxgeneration):
            self.update()  

    def update(self):
        # 1. Generate Initial Generation
        # 2. Calculate their fitness with penalty
        # 3. Crossover according to fitnesses
        # 4. Mutation according to fitnesses
        # 5. Return to Step 2
        self.candidates.crossover()
        self.candidates.mutation()

    def getcache(self):
        return self.candidates.getallcandidates(),self.candidates.getallfitness()

    def getsolution(self):
        return self.candidates.getbestcandidate()