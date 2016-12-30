# Author: Yang Long <longyang_123@yeah.net>
#
# License:  LGPL-2.1

import numpy as np
from Constraint import Constraints

class Candidates:
    def __init__(self,popsize,chromesize,fitnessfunc,constraints=None,IntCon=None,LB=None,UB=None,initpopulation=None):
        self.popsize = popsize
        self.chromesize = chromesize
        self.fitnessfunc = fitnessfunc
        self.constraints = constraints
        self.IntCon = IntCon
        if initpopulation is None:
            self.populations = np.zeros([popsize,chromesize])
        else:
            self.populations = initpopulation
        self.fitness = np.zeros(popsize)
        self.LB = LB
        self.UB = UB
        self.init()

    def init(self):
        '''
        Generate initial generation
        '''
        self.populations = self.LB + (self.UB - self.LB)*np.random.random(self.chromesize)
        self.integerrestrict()
        self.fitness()


    def crossover(self,a=0,breal=0.25,bint=0.25):
        '''
        Chrome Cross-Over
        '''
        self.fitness()
        (M,N) = np.shape(self.populations)
        newpopulations = np.zeros([M,N])
        newpopsize = 0

        while newpopsize<M:
            father = self.selection()
            mother = self.selection()
            while father == mother:
                mother = self.selection()

            r = np.random.random(N)
            u = np.random.random(N)

            beta = a + breal*np.log(u)*(r>0.5) - breal*np.log(u)*(r<=0.5)
            if self.IntCon is not None:
                beta[self.IntCon] = a + bint*np.log(u[self.IntCon])*(r[self.IntCon]>0.5) - bint*np.log(u[self.IntCon])*(r[self.IntCon]<=0.5)

            x1 = self.populations[father]
            x2 = self.populations[mother]
            y1 = x1 + beta*np.abs(x1-x2)
            y2 = x2 + beta*np.abs(x1-x2)

            newchromes[newpopsize,:] = y1
            newchromes[newpopsize+1,:] = y2 

            newpopsize = newpopsize + 2

        self.populations = newpopulations
        self.integerrestrict()
        self.fitness()

    def mutation(self,preal=0.25,pint=0.25):
        '''
        Mutation Operation
        '''
        M = self.popsize
        N = self.chromesize
        newchromes = np.zeros([M,N])

        for i in range(M):
            chrome = self.populations[i]
            P = preal*np.ones(N)
            if self.IntCon is not None:
                P[self.IntCon] = pint

            s = np.random.random(N)**P
            r = np.random.random(N)

            t = (chrome-LB)/(UB-chrome)

            newchromes[i] = chrome - s*(chrome-LB)*(r>t) + s*(UB-chrome)*(r<=t)

        self.populations = newchromes
        self.integerrestrict()
        self.fitness()

    def fitness(self):
        '''
        Calculation of Fitness
        '''
        for i in range(self.popsize):
            self.fitness[i] = self.fitnessfunc(self.populations[i]) + self.constraints.fitness(self.populations[i])
        

    def selection(self):
        '''
        Make a selection from candidates based on tournament selection (Unachieved yet)
        '''
        prob = 1 - self.fitness/np.max(self.fitness)
        prob = prob/np.sum(prob)
        probcum = np.cumsum(prob)
        return np.sum(probcum<np.random.random())

    def integerrestrict(self):
        '''
        Integer Restriction
        '''
        if self.IntCon is not None:
            for i in range(self.popsize):
                intchrome = np.floor(self.populations[i,self.IntCon])
                intchrome = intchrome + 1*(np.random.random(len(intchrome))>0.5)

                posLB = np.where(intchrome<self.LB[self.IntCon])
                intchrome[posLB] = self.LB[self.IntCon][posLB]

                posUB = np.where(intchrome>self.UB[self.IntCon])
                intchrome[posUB] = self.UB[self.IntCon][posUB]

                self.populations[i,self.IntCon] = intchrom

    def getbestcandidate(self):
        return self.populations[np.argmax(self.fitness)],np.max(self.fitness)

    def getallcandidates(self):
        return self.populations

    def getallfitness(self):
        return self.fitness