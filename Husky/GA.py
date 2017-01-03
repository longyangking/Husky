# Author: Yang Long <longyang_123@yeah.net>
#
# License:  LGPL-2.1

import numpy as np
from Constraint import Constraints
from Candidate import Candidates

class GA:
    def __init__(self,fitnessfunc,nvars,LB=None,UB=None,IntCon=None,initpopulation=None,timelimit=None,maxgeneration=300,popsize=60,tolerance=0.05,verbose=False):
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
        self.initpopulation = initpopulation    # Initial Populations
        self.verbose = verbose                  # Print Computational Info
        self.tolerance = tolerance
    
    def addconstraint(self,constraintfunc,penalty=1000):
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
        self.candidates = Candidates(self.popsize,self.chromesize,self.fitnessfunc,constraints=self.constraints,IntCon=self.IntCon,LB=self.LB,UB=self.UB,initpopulation=self.initpopulation,verbose=self.verbose)
        for i in range(self.maxgeneration):
            if self.verbose:
                print '{num}th generation:'.format(num=i+1),
            if self.update():
                if self.verbose:
                    print 'Optimization terminated: Tolerance is less than specific value {num}'.format(num=self.tolerance)
                break
        if self.verbose:
            print 'Optimization terminated: Maximum Generation'

    def update(self):
        return self.candidates.update(tolerance=self.tolerance)

    def getcache(self):
        return self.candidates.getallcandidates(),self.candidates.getallfitness()

    def getsolution(self):
        return self.candidates.getbestcandidate()