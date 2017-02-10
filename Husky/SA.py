# Author: Yang Long <longyang_123@yeah.net>
#
# License: LGPL-2.1

import numpy as np

class SA:
    def __init__(self,fitnessfunc,nvars,LB=None,UB=None,IntCon=None,initstates=None,timelimit=None,maxgeneration=300,statesize=100,tolerance=0.05,verbose=False):
        self.featuresize = nvars
        self.timelimit = timelimit
        self.maxgeneration = maxgeneration
        self.constraints = Constraints()
        self.statesize = statesize
        self.fitnessfunc = fitnessfunc
        self.states = None
        self.LB = LB
        self.UB = UB
        self.IntCon = IntCon
        self.initstates = initstates
        self.verbose = verbose
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
        # Coming soon
        self.states = State()
        for i in range(self.maxgeneration):
            if self.verbose:
                print '{num}th cooling:'.format(num=i+1)
            if self.update():
                if self.verbose:
                    print 'Optimization terminated: Tolerance is less than specific value {num}'.format(num=self.tolerance)
                break
        if self.verbose:
            print 'Optimization terminated: Maximum Generation'

    def update(self):
        return self.states.cooling(tolerance=self.tolerance)
    
    def getsolution(self):
        return self.state.getresult()
