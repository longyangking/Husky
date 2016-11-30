import Candidates.Candidates as Candidates
import numpy as np

class GA(object):
    def __init__(self,popsize,chromsize,fitnessfun,probcross=0.8,probmutate=0.1,lencross=5,maxiteration=50,bestspliter=5):
        self.popsize = popsize
        self.chromsize = chromsize
        self.candidates = Candidates(popsize,chromsize,fitnessfun)
        self.fitnessfun = fitnessfun
        self.probcross = probcross
        self.probmutate = probmutate
        self.lencross = lencross
        self.maxiteration = maxiteration
        self.bestspliter = bestspliter

    def originalgeneration(self):
        self.candidates.randinit()
        self.candidates.fit()

    def newgeneration(self):
        '''
        Genetic Cross and Mutation
        '''
        self.candidates.eliminate(bestspliter)

    def update(self):
        '''
        Select best Candidates
        '''
        self.newgeneration() 
        self.candidates.mutate(self.probmutate)
        self.candidates.cross(self.probcross,self.lencross)

    def start(self):
        self.originalgeneration()
        for iter in range(self.maxiteration-1):
            self.newgeneration()
            self.update()
        self.newgeneration()

    def result(self,index):
        return self.candidates.getcandidate(index)

