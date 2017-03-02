# Author: Yang Long <longyang_123@yeah.net>
#
# License:  LGPL-2.1

import numpy as np
from Constraint import Constraints

class Candidates:
    def __init__(self,popsize,chromesize,fitnessfunc,\
                constraints=None,IntCon=None,LB=None,UB=None,\
                initpopulation=None,Elitecount=2,crossfraction=0.8,verbose=False):
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

        if LB is not None: 
            self.LB = LB
        else:
            self.UB = 2.0**64

        if UB is not None: 
            self.UB = UB
        else:
            self.UB = 2.0**-64

        
        self.verbose = verbose
        self.init()

    def init(self):
        '''
        Generate initial generation
        '''
        for i in range(self.popsize):
            self.populations[i] = self.LB + (self.UB - self.LB)*np.random.random(self.chromesize)
        self.integerrestrict()
        self.fitness = self.fit()
        if self.verbose:
            print 'Initiate Generations...'


    def crossover(self,a=0,breal=0.25,bint=0.25):
        '''
        Chrome Cross-Over
        '''
        (M,N) = np.shape(self.populations)
        newpopulations = np.zeros([M,N])
        newpopsize = 0

        while newpopsize<M:
            father = self.selection()
            mother = self.selection()
            while father == mother:
                mother = self.selection()

            #r = np.random.random(N)
            #u = np.random.random(N)

            #beta = a + breal*np.log(u)*(r>0.5) - breal*np.log(u)*(r<=0.5)
            #if self.IntCon is not None:
            #    beta[self.IntCon] = a + bint*np.log(u[self.IntCon])*(r[self.IntCon]>0.5) - bint*np.log(u[self.IntCon])*(r[self.IntCon]<=0.5)

            #x1 = self.populations[father]
            #x2 = self.populations[mother]
            #y1 = x1 + beta*np.abs(x1-x2)
            #y2 = x2 + beta*np.abs(x1-x2)

            #newpopulations[newpopsize,:] = y1
            #newpopulations[newpopsize+1,:] = y2 

            crosschromestart = np.random.randint(self.chromesize)
            crosschromeend = np.random.randint(crosschromestart+1,self.chromesize+1)

            crossfather = self.populations[father,crosschromestart:crosschromeend]
            crossmother = self.populations[mother,crosschromestart:crosschromeend]

            newcrossfather = np.zeros(crosschromeend-crosschromestart)
            newcrossmother = np.zeros(crosschromeend-crosschromestart)

            for i in range(len(crossfather)):
                v = np.sort([crossfather[i],crossmother[i]])
                newcrossfather[i] = v[0] + (v[1]-v[0])*np.random.random()
                newcrossmother[i] = v[0] + (v[1]-v[0])*np.random.random()

            newpopulations[newpopsize,:] = self.populations[father,:].copy()
            newpopulations[newpopsize+1,:] = self.populations[mother,:].copy()

            newpopulations[newpopsize,crosschromestart:crosschromeend] = newcrossfather
            newpopulations[newpopsize+1,crosschromestart:crosschromeend] = newcrossmother 

            newpopsize = newpopsize + 2

        return newpopulations


    def mutation(self,preal=0.25,pint=0.25):
        '''
        Mutation Operation
        '''
        M = self.popsize
        N = self.chromesize
        newpopulations = np.zeros([M,N])

        for i in range(M):
            chrome = self.populations[i].copy()
            #P = preal*np.ones(N)
            #if self.IntCon is not None:
            #    P[self.IntCon] = pint

            #s = np.random.random(N)**P
            #r = np.random.random(N)

            #t = (chrome-self.LB)/(self.UB-chrome)

            #newchromes[i] = chrome - s*(chrome-self.LB)*(r>t) + s*(self.UB-chrome)*(r<=t)
        
            #size = np.floor(np.random.random()*self.chromesize)
            pos = np.random.randint(self.chromesize)
            value = self.LB[pos] + (self.UB[pos]-self.LB[pos])*np.random.random()
            chrome[pos] = value

            newpopulations[i] = chrome

        return newpopulations

    def fit(self):
        '''
        Calculation of Fitness
        '''
        (M,N) = np.shape(self.populations)
        fitness = np.zeros(M)
        for i in range(M):
            fitness[i] = self.fitnessfunc(self.populations[i]) + self.constraints.fitness(self.populations[i])
        return fitness

    def selection(self):
        '''
        Make a selection from candidates based on tournament selection (Unachieved yet)
        '''
        prob = 1 - self.fitness/np.max(self.fitness)
        prob = -np.sort(-prob/np.sum(prob)) # Elite policy
        probcum = np.cumsum(prob)
        return np.sum(probcum<np.random.random())

    def integerrestrict(self):
        '''
        Integer Restriction
        '''
        (M,N) = np.shape(self.populations)
        if self.IntCon is not None:
            for i in range(M):
                intchrome = np.floor(self.populations[i,self.IntCon])
                intchrome = intchrome + 1*(np.random.random(len(intchrome))>0.5)

                posLB = np.where(intchrome<self.LB[self.IntCon])
                intchrome[posLB] = self.LB[self.IntCon][posLB]

                posUB = np.where(intchrome>self.UB[self.IntCon])
                intchrome[posUB] = self.UB[self.IntCon][posUB]

                self.populations[i,self.IntCon] = intchrome
    
    def update(self,tolerance=0.05,a=0,breal=0.25,bint=0.25,preal=0.25,pint=0.25):
        if len(np.unique(self.fitness)) <= np.floor(self.popsize*tolerance)+1:
            return True
        if self.verbose:
            print 'Start -> ',
        crossover = self.crossover(a=0,breal=0.25,bint=0.25)
        if self.verbose:
            print 'Cross -> ',
        mutation = self.mutation(preal=0.25,pint=0.25)
        if self.verbose:
            print 'Mutate -> ',
        self.populations = np.concatenate((self.populations,crossover,mutation))
        self.integerrestrict()
        self.fitness = self.fit()
        self.populations = self.populations[np.argsort(self.fitness)[:self.popsize]]
        self.fitness = self.fit()
        if self.verbose:
            print 'Finished!'
        return False


    def getbestcandidate(self):
        return self.populations[np.argmax(self.fitness)],np.max(self.fitness)

    def getallcandidates(self):
        return self.populations

    def getallfitness(self):
        return self.fitness