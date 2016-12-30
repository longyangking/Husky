# Author: Yang Long <longyang_123@yeah.net>
#
# License:  LGPL-2.1

import numpy as np
from Constraint import Constraints
from Candidate import Candidates

class GA:
    def __init__(self,fitnessfunc,nvars,LB=None,UB=None,IntCon=None,initpopulation=None,timelimit=None,maxgeneration=100,popsize=60):
        self.chromesize = nvars
        self.timelimit = timelimit
        self.maxgeneration = maxgeneration
        self.constraints = Constraints()
        self.popsize = popsize
        self.fitnessfunc = fitnessfunc
        self.candidates = None
        self.LB = LB
        self.UB = UB
        self.IntCon = IntCon
        self.initpopulation = initpopulation
    
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