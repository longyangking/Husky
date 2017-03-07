# Author: Yang Long <longyang_123@yeah.net>
#
# License: LGPL-2.1

import numpy as np
import Creation

class PSO:
    def __init__(self,fitnessfunc,nvars,LB=None,UB=None,IntCon=None,initparticles=None,\
        timelimit=None,\
        maxiter=300,particlesize=100,\
        parallelized=False,verbose=False):
        self.featuresize = nvars                # Number of variables
        self.timelimit = timelimit              # Time limit to optimize
        self.maxgeneration = maxgeneration      # Maximum of generation
        self.constraints = Constraints()        # Nomral Constraints class
        self.particlesize = particlesize        # Size of particle swarm
        self.fitnessfunc = fitnessfunc          # Fitness function
        self.particles = None                   # Particles class
        self.LB = LB                            # Lower Boundary
        self.UB = UB                            # Upper Boundary
        self.IntCon = IntCon                    # Integer Constraint
        self.initparticles = initparticles      # Initial particles
        self.verbose = verbose                  # Verbose sign
        self.tolerance = tolerance              # Optimization Tolerance

        self.creationfunction = Creation.Uniform
    
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
        #Init PSO and start to calculate, coming soon
        #
        #
        self.particles = Paricle() # Coming, can not work now
        for i in range(self.maxgeneration):
            if self.verbose:
                print '{num}th update:'.format(num=i+1)
            if self.update():
                if self.verbose:
                    print 'Optimization terminated: Tolerance is less than specific value {num}'.format(num=self.tolerance)
                break
        if self. verbose:
            print 'Optimization terminated: Maximum Generaion'

    def update(self):
        return self.particles.update(tolerance=self.tolerance)

    def getsolution(self):
        return self.particles.getresult()
