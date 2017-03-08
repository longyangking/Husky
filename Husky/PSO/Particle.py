# Author: Yang Long <longyang_123@yeah.net>
# 
# License: LGPL-2.1

import numpy as np

class Particle:
    def __init__(self,func,num,dimension,C1,C2,w,LB,UB,IntCon=None,\
        Vmin=None,Vmax=None,initpos=None,initbestpos=None,initvelocity=None,\
        initgroupbestpos=None,creationfunction=None,\
        verbose=False):

        self.func = func
        self.num = num
        self.dimension = dimension

        self.C1 = C1
        self.C2 = C2   
        self.w = w
    
        self.LB = LB
        self.UB = UB
        self.Vmin = Vmin
        self.Vmax = Vmax
        
        if initpos is not None:
            self.pos = initpos
        else:
            self.pos = np.zeros((num,dimension))
        
        if initbestpos is not None:
            self.bestpos = initbestpos
        else:
            self.bestpos = np.zeros((num,dimension))
        
        if initvelocity is not None:
            self.velocity = initvelocity
        else:
            self.velocity = np.zeros((num,dimension))

        if initgroupbestpos is not None:
            self.groupbestpos = initgroupbestpos
        else:
            self.groupbestpos = np.zeros(dimension)

        self.verbose = verbose
        self.initparticles()

    def initparticles(self):
        self.velocity = np.random.random((self.num,self.dimension))
        self.pos = np.random.random((self.num,self.dimension))
        self.evaluate()

    def update(self):
        # Naive update
        R1 = np.random.random((self.num,self.dimension))
        R2 = np.random.random((self.num,self.dimension))
        V = self.w*self.velocity + self.C1*R1*(self.bestpos-self.pos) + self.C2*R2*(self.groupbestpos-self.pos)
        self.velocity = V
        self.pos = self.pos + V
        
        if self.LB is not None:
            posLB = np.where(self.pos<LB)
            self.pos[posLB] = LB[posLB]
        
        if self.UB is not None:
            posUB = np.where(self.pos>UB)
            self.pos[posUB] = UB[posUB]

        self.evaluate()

    def evaluate(self):
        for i in range(self.num):
            if self.func(self.pos[i]) < self.func(self.bestpos[i]):
                self.bestpos[i] = self.pos[i]
            if self.func(self.bestpos[i]) < self.func(self.groupbestpos):
                self.groupbestpos = self.bestpos[i]
        if self.verbose:
            print 'Best Particle: {best}'.format(best=self.groupbestpos)

    def check(self):
        return True

    def getbest(self):
        return self.groupbestpos,self.func(self.groupbestpos)
