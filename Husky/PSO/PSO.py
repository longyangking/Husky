# Author: Yang Long <longyang_123@yeah.net>
#
# License: LGPL-2.1

import numpy as np
from Constraint import Constraints
from Particle import Particle
import Creation

class PSO:
    def __init__(self,fitnessfunc,nvars,LB=None,UB=None,IntCon=None,initparticles=None,
        C1=0.2,C2=0.2,w=1.0,minfractionneighbors=0.25,\
        timelimit=None,stalliterlimit=50,stalltimelimit=None,TolFun=1.0*10**-6,\
        groupsize=1,exchangeforward=True,exchangefraction=0.2,exchangeinterval=20,\
        maxiter=300,particlesize=300,\
        parallelized=False,verbose=False,options=None):

        self.featuresize = nvars                # Number of variables
        self.timelimit = timelimit              # Time limit to optimize
        self.maxiter = maxiter                  # Maximum of generation
        self.constraints = Constraints()        # Nomral Constraints class
        self.particlesize = particlesize        # Size of particle swarm
        self.fitnessfunc = fitnessfunc          # Fitness function
        self.particles = None                   # Particles class

        self.LB = LB
        self.UB = UB
        self.IntCon = IntCon                    # Integer Constraint
        self.initparticles = initparticles      # Initial particles
        self.verbose = verbose                  # Verbose sign

        self.C1 = C1
        self.C2 = C2
        self.w = w
        self.minfractionneighbors = minfractionneighbors

        self.stalliterlimit = stalliterlimit
        self.stalltimelimit = stalltimelimit
        self.TolFun = TolFun

        self.groupsize = groupsize
        self.exchangeforward = exchangeforward
        self.exchangefraction = exchangefraction
        self.exchangeinterval = exchangeinterval

        self.parallelized = parallelized
        self.options = options
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
        self.particles = Particle(func=self.fitnessfunc,num=self.particlesize,\
                                dimension=self.featuresize,C1=self.C1,C2=self.C2,w=self.w,\
                                LB=self.LB,UB=self.UB,initpos=self.initparticles,verbose=self.verbose) 

        for i in range(self.maxiter):
            if self.verbose:
                print '{num}th update: '.format(num=i+1),
            if self.update():
                if self.verbose:
                    print 'Optimization terminated: Tolerance is less than specific value {num}'.format(num=self.tolerance)
                break
        if self. verbose:
            print 'Optimization terminated: Maximum Generaion'

    def update(self):
        return self.particles.update()

    def check(self):
        pass

    def exchange(self):
        
    def getcache(self):

    def getsolution(self):
        return self.particles.getbest()
