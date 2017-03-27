# Author: Yang Long <longyang_123@yeah.net>
#
# License: LGPL-2.1

import numpy as np
import time

from Constraint import Constraints
from Particle import Particle
from PSOoptions import PSOoptions
import MultiUtils

class MultiPSO:
    def __init__(self,func,nvars,targetsize,LB=None,UB=None,IntCon=None,\
        initpos=None,initbestpos=None,initvelocity=None,initgroupbestpos=None,\
        C1=0.2,C2=0.2,w=1.0,minfractionneighbors=None,\
        timelimit=None,stalliterlimit=50,stalltimelimit=None,TolFun=1.0*10**-6,\
        groupsize=1,exchangeforward=True,exchangefraction=0.2,exchangeinterval=20,\
        maxiter=None,particlesize=300,\
        algorithm='SMPSO',parallelized=False,verbose=False,options=None):
        '''
        Multi-objective Particle Swarm Optimization
            1. OMOPSO
            2. SMPSO
        '''

        self.targetsize = targetsize
        self.featuresize = nvars                # Number of variables
        self.timelimit = timelimit              # Time limit to optimize
        self.maxiter = maxiter                  # Maximum of generation
        self.constraints = Constraints()        # Nomral Constraints class
        self.particlesize = particlesize        # Size of particle swarm
        self.func = func          # Fitness function
        self.particles = list()                  # Particles class

        self.LB = LB
        self.UB = UB
        self.IntCon = IntCon                    # Integer Constraint
        self.initpos = initpos                  # Initial particles
        self.initbestpos = initbestpos
        self.initvelocity = initvelocity
        self.initgroupbestpos = initgroupbestpos

        self.verbose = verbose                  # Verbose sign

        self.C1 = C1
        self.C2 = C2
        self.w = w
        self.minfractionneighbors = minfractionneighbors

        self.groupsize = groupsize
        self.particlesstatus = np.zeros(groupsize)
        self.exchangeforward = exchangeforward
        self.exchangefraction = exchangefraction
        self.exchangeinterval = exchangeinterval

        self.parallelized = parallelized
        if options is not None:
            self.options = options
        else:
            self.options = PSOoptions()
        self.creationfunction = MultiUtils.Creation.Uniform
        self.distancefunction = MultiUtils.Pareto.FastNonDominatedSorting

        self.stalliterlimit = stalliterlimit
        self.stalltimelimit = stalltimelimit
        self.TolFun = TolFun
        self.stallobjectives = list()
        self.stallcount = np.zeros(groupsize)
        self.stallstarttime = np.zeros(groupsize)
        self.stalltime = np.zeros(groupsize)
    
    def addconstraint(self,constraintfunc,penalty=1000):
        self.constraints.add(constraintfunc,penalty)
    
    def setparameter(self,parameter,value): 
        if parameter == 'timelimit':
            self.timelimit = value
            return True
        if parameter == 'maxiter':
            self.maxiter = value
            return True
        return False

    def start(self):
        '''
        Main process of PSO
        '''
        starttime = time.time()
        # Initiate the particles group
        for i in range(self.groupsize):
            self.particles.append(Particle(func=self.func,particlesize=self.particlesize,\
                                featuresize=self.featuresize,C1=self.C1,C2=self.C2,w=self.w,\
                                LB=self.LB,UB=self.UB,IntCon=self.IntCon,constraints=self.constraints,\
                                initpos=self.initpos,initbestpos=self.initbestpos,\
                                initvelocity=self.initvelocity,initgroupbestpos=self.initgroupbestpos,\
                                creationfunction=self.creationfunction,distancefunction=self.distancefunction,\
                                minfractionneighbors=self.minfractionneighbors,\
                                parallelized=self.parallelized,verbose=self.verbose,options=self.options))
            self.stallobjectives.append(None)

        if self.maxiter is not None:
            for i in range(self.maxiter):
                if self.verbose:
                    print '{num}th update: '.format(num=i+1),
                self.update()

                [status,code] = self.check()
                if status:
                    if self.verbose:
                        print 'Optimization terminated: {reason}'.format(reason=code)
                    break

                if (i+1)%self.exchangeinterval == 0 and self.groupsize > 1:
                    self.exchange()
                    if self.verbose:
                        print '-----exchange-----'

                # Terminate by the time limit
                if self.timelimit is not None:
                    currenttime = time.time()
                    if currenttime-starttime > self.timelimit:
                        if self.verbose:
                            print 'Optimization terminated: Time Limit!'
                        break
                    
            if self.verbose and not status:
                print 'Optimization terminated: Maximum Generaion'
        else:
            iter = 0
            while 1:
                if self.verbose:
                    print '{num}th update: '.format(num=iter+1),
                self.update()

                [status,code] = self.check()
                if status:
                    if self.verbose:
                        print 'Optimization terminated: {reason}'.format(reason=code)
                    break

                if (iter+1)%self.exchangeinterval == 0 and self.groupsize > 1:
                    self.exchange()
                    if self.verbose:
                        print '-----exchange-----'

                # Terminate by the time limit
                if self.timelimit is not None:
                    currenttime = time.time()
                    if currenttime-starttime > self.timelimit:
                        if self.verbose:
                            print 'Optimization terminated: Time Limit!'
                        break
            
                iter += 1

    def update(self):
        '''
        Evolve every particle group
        '''
        for i in range(self.groupsize):
            if self.particlesstatus[i] == 0:             # Paricles[i] is on Active State
                self.particles[i].update()

    def check(self):
        '''
        Check tolerance of populations
        '''
        activecount = 0
        for i in range(self.groupsize):
            (solution,objective) = self.particles[i].getbest()
            
            if self.stallobjectives[i] is None:
                self.stallobjectives[i] = objective
                activecount += 1
                continue
            
            # Calculate Stall Generation
            averagechange = np.abs(objective-self.stallobjectives[i])
            if averagechange < self.TolFun:
                self.stallcount[i] += 1
                self.stalltime[i] = self.stalltime[i] + time.time() - self.stallstarttime[i]
                #if self.verbose:
                #    print ' -> Start stall: Generation {generation}th '.format(generation=self.stallgeneration)
            else:
                self.stallcount[i] = 0
                self.stallstarttime[i] = time.time()
                self.stalltime[i] = 0
                self.stallobjectives[i] = objective
            
            # Stall Generation Limit
            if self.stallcount[i] > self.stalliterlimit:
                self.particlesstatus[i] = 1                 # Stall Gen Limit

            # Stall Time Limit
            if self.stalltimelimit is not None:
                if self.stalltime[i] > self.stalltimelimit:
                    self.particlesstatus[i] = 2             # Stall Time Limit

            if self.particlesstatus[i] == 0:
                activecount += 1                            # Some group still alive

        if activecount >= 1:
            return False,None
        else:
            code = str()
            for i in range(self.groupsize):
                if self.particlesstatus[i] == 1:
                    code += '{num}th group -> {reason}\n'.format(num=i+1,reason='Stall Generation Limit')
                elif self.particlesstatus[i] == 2:
                    code += '{num}th group -> {reason}\n'.format(num=i+1,reason='Stall Time Limit')
            return True,code

    def exchange(self):
        '''
        Exchange particles
        '''
        exchangesize = int(self.particlesize*self.exchangefraction)
        if self.exchangesizeforward:
            for i in range(self.groupsize):
                (particles1,source1) = self.particles[i].exchangeout(exchangesize)
                if i+1<self.groupsize:
                    (particles2,source2) = self.particles[i+1].exchangeout(exchangesize)
                    self.particles[i].exchangein(source2,particles2)
                    self.particles[i+1].exchangein(source1,particles1)
                else:
                    (particles2,source2) = self.particles[0].exchangeout(exchangesize)
                    self.particles[i].exchangein(source2,particles2)
                    self.particles[0].exchangein(source1,particles1)
        else:
            for i in range(self.groupsize,-1,-1):
                (particles1,source1) = self.particles[i].exchangeout(exchangesize)
                if i-1>=0:
                    (particles2,source2) = self.particles[i-1].exchangeout(exchangesize)
                    self.particles[i].exchangein(source2,particles2)
                    self.particles[i-1].exchangein(source1,particles1)
                else:
                    (particles2,source2) = self.particles[self.groupsize].exchangeout(exchangesize)
                    self.particles[i].exchangein(source2,particles2)
                    self.particles[self.groupsize].exchangein(source1,particles1)

    def getcache(self):
        solutions = np.zeros((self.particlesize*self.groupsize,self.featuresize))
        objectives = np.zeros(self.particlesize*self.groupsize)
        for i in range(self.groupsize):
            (solution,objective) = self.particles[i].getallparticles()
            solutions[(i)*self.popsize:(i+1)*self.popsize,:] = solution
            objectives[(i)*self.popsize:(i+1)*self.popsize] = objective

        return solutions,objectives

    def getsolution(self):
        solutions = np.zeros((self.groupsize,self.featuresize))
        objectives = np.zeros(self.groupsize)
        for i in range(self.groupsize):
            (solutions[i],objectives[i]) = self.particles[i].getbest()
        bestpos = np.argmin(objectives)
        return solutions[bestpos],objectives[bestpos]
