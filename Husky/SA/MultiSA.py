# Author: Yang Long <longyang_123@yeah.net>
#
# License: LGPL-2.1

import numpy as np
from Constraint import Constraints
from MultiState import MultiState
import time
import MultiUtils

class MultiSA:
    def __init__(self,func,targetsize,nvars,LB=None,UB=None,IntCon=None,
        initstates=None,statesize=300,reannealinterval=100,inittemperature=None,
        timelimit=None,maxiter=None,TolFun=1.0*10**-6,mutationrate=0.2,
        objectivelimit=None,stalliterlimit=None,stalltimelimit=None,maxfunevals=None,
        groupsize=1,exchangeforward=True,exchangefraction=0.2,exchangeinterval=20,
        selfoptimization=False,parallelized=False,verbose=False,options=None):

        self.func = func
        self.featuresize = nvars
        self.targetsize = targetsize
        if LB is None:
            self.LB = LB
        else:
            self.LB = np.array(LB)
        if UB is None:
            self.UB = UB
        else:
            self.UB = np.array(UB)
        if IntCon is None:
            self.IntCon = IntCon
        else:
            self.IntCon = np.array(IntCon)

        self.initstates = initstates
        self.statesize = statesize
        self.reannealinterval = reannealinterval
        self.inittemperature = inittemperature

        self.timelimit = timelimit
        self.maxiter = maxiter

        if maxfunevals is not None:
            self.maxfunevals = maxfunevals
        else:
            self.maxfunevals = 3000*np.size(nvars)/self.statesize

        self.TolFun = TolFun
        self.objectivelimit = objectivelimit
        self.mutationrate = mutationrate

        if stalliterlimit is not None:
            self.stalliterlimit = stalliterlimit
        else:
            self.stalliterlimit = 150*np.size(nvars)

        self.stalltimelimit = stalltimelimit
        
        self.groupsize = groupsize
        self.exchangeforward = exchangeforward
        self.exchangefraction = exchangefraction
        self.exchangeinterval = exchangeinterval

        self.selfoptimization = selfoptimization
        self.verbose = verbose
        self.parallelized = parallelized

        if options is not None:
            self.options = options
        else:
            self.options = MultiUtils.MultiSAoptions()

        self.stallobjectives = list()
        self.stallcount = np.zeros(groupsize)
        self.stallstarttime = np.zeros(groupsize)
        self.stalltime = np.zeros(groupsize)
        self.statesstatus = np.zeros(groupsize)

        self.constraints = Constraints()
        self.states = list()
        self.acceptancefunction = MultiUtils.Acceptance.AcceptanceSA
        self.annealingfunction = MultiUtils.Annealing.AnnealingFast
        self.temperaturefunction = MultiUtils.Temperature.TemperatureExp
        self.fitnessscalefunction = MultiUtils.FitnessScale.Rank
        self.distancefunction = MultiUtils.Pareto.FastNonDominatedSorting
        self.mutationfunction = MultiUtils.Mutation.Uniform

    def addconstraint(self,constraintfunc,penalty=1000):
        self.constraints.add(constraintfunc,penalty)
    
    def setparameter(self,parameter,value):
        if parameter == 'timelimit':
            self.timelimit = value
            return True
        return False

    def start(self):
        '''
        Main process of SA
        '''
        starttime = time.time()
        # Initiate the States group
        for i in range(self.groupsize):
            self.states.append(MultiState(func=self.func,statesize=self.statesize,featuresize=self.featuresize,targetsize=self.targetsize,
                                LB=self.LB,UB=self.UB,IntCon=self.IntCon,constraints=self.constraints,mutationrate=self.mutationrate,
                                initstates=self.initstates,inittemperature=self.inittemperature,maxfunevals=self.maxfunevals,
                                acceptancefunction=self.acceptancefunction,
                                annealingfunction=self.annealingfunction,
                                temperaturefunction=self.temperaturefunction,
                                fitnessscalefunction=self.fitnessscalefunction,
                                distancefunction=self.distancefunction,
                                mutationfunction=self.mutationfunction,
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

                if (i+1)%self.reannealinterval == 0:
                    self.reanneal()
                    if self.verbose:
                        print '-----reanneal-----'
                    
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

                if (iter+1)%self.reannealinterval == 0:
                    self.reanneal()
                    if self.verbose:
                        print '-----reanneal-----'
            
                iter += 1

    def update(self):
        '''
        Evolve every particle group
        '''
        for i in range(self.groupsize):
            if self.statesstatus[i] == 0:             # Paricles[i] is on Active State
                self.states[i].update()

    def check(self):
        '''
        Check tolerance of populations
        '''
        activecount = 0
        for i in range(self.groupsize):
            (solution,objectives) = self.states[i].getfrontier()
            
            if self.stallobjectives[i] is None:
                self.stallobjectives[i] = objectives
                activecount += 1
                continue
            
            # Calculate Stall Generation
            averagechange = np.abs(np.mean(objectives,axis=0)-np.mean(self.stallobjectives[i],axis=0))/np.abs(np.mean(self.stallobjectives[i],axis=0))
            maxchange = np.abs(np.max(objectives,axis=0)-np.max(self.stallobjectives[i],axis=0))/np.abs(np.max(self.stallobjectives[i],axis=0))
            minchange = np.abs(np.min(objectives,axis=0)-np.min(self.stallobjectives[i],axis=0))/np.abs(np.min(self.stallobjectives[i],axis=0))
            change = np.sum(averagechange + maxchange + minchange)/3/self.targetsize
            if change < self.TolFun:
                self.stallcount[i] += 1
                self.stalltime[i] = self.stalltime[i] + time.time() - self.stallstarttime[i]
                #if self.verbose:
                #    print ' -> Start stall: Generation {generation}th '.format(generation=self.stallgeneration)
            else:
                self.stallcount[i] = 0
                self.stallstarttime[i] = time.time()
                self.stalltime[i] = 0
                self.stallobjectives[i] = objectives
            
            # Stall Generation Limit
            if self.stallcount[i] > self.stalliterlimit:
                self.statesstatus[i] = 1                 # Stall Gen Limit

            # Stall Time Limit
            if self.stalltimelimit is not None:
                if self.stalltime[i] > self.stalltimelimit:
                    self.statesstatus[i] = 2             # Stall Time Limit

            if self.statesstatus[i] == 0:
                activecount += 1                            # Some group still alive

        if activecount >= 1:
            return False,None
        else:
            code = str()
            for i in range(self.groupsize):
                if self.statesstatus[i] == 1:
                    code += '{num}th group -> {reason}\n'.format(num=i+1,reason='Stall Generation Limit')
                elif self.statesstatus[i] == 2:
                    code += '{num}th group -> {reason}\n'.format(num=i+1,reason='Stall Time Limit')
            return True,code

    def reanneal(self):
        '''
        Re-Annealing
        '''
        for i in range(self.groupsize):
            if self.statesstatus[i] == 0:             # Paricles[i] is on Active State
                self.states[i].reanneal()

    def exchange(self):
        '''
        Exchange states
        '''
        exchangesize = int(self.statesize*self.exchangefraction)
        if self.exchangesizeforward:
            for i in range(self.groupsize):
                (states1,source1) = self.states[i].exchangeout(exchangesize)
                if i+1<self.groupsize:
                    (states2,source2) = self.states[i+1].exchangeout(exchangesize)
                    self.states[i].exchangein(source2,states2)
                    self.states[i+1].exchangein(source1,states1)
                else:
                    (states2,source2) = self.states[0].exchangeout(exchangesize)
                    self.states[i].exchangein(source2,states2)
                    self.states[0].exchangein(source1,states1)
        else:
            for i in range(self.groupsize,-1,-1):
                (states1,source1) = self.states[i].exchangeout(exchangesize)
                if i-1>=0:
                    (states2,source2) = self.states[i-1].exchangeout(exchangesize)
                    self.states[i].exchangein(source2,states2)
                    self.states[i-1].exchangein(source1,states1)
                else:
                    (states2,source2) = self.states[self.groupsize].exchangeout(exchangesize)
                    self.states[i].exchangein(source2,states2)
                    self.states[self.groupsize].exchangein(source1,states1)

    def getcache(self):
        solutions = np.zeros((self.statesize*self.groupsize,self.featuresize))
        objectives = np.zeros((self.statesize*self.groupsize,self.targetsize))
        for i in range(self.groupsize):
            (solution,objective) = self.states[i].getallstates()
            solutions[(i)*self.statesize:(i+1)*self.statesize,:] = solution
            objectives[(i)*self.statesize:(i+1)*self.statesize] = objective

        return solutions,objectives

    def getsolution(self):
        solutions = list()
        objectives = list()
        fitness = list()

        for i in range(self.groupsize):
            (solution,objective) = self.states[i].getfrontier()
            for j in range(len(solution)):
                solutions.append(solution[j])
                objectives.append(objective[j])
                fitness.append(objective[j] + self.constraints.fitness(solution[j]))

        solutions = np.array(solutions)
        objectives = np.array(objectives)
        fitness = np.array(fitness)

        rank,distance = self.distancefunction(fitness,args=self.options.Pareto.args)
        front = np.where(rank==0)

        return solutions[front],objectives[front]