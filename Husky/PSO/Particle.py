# Author: Yang Long <longyang_123@yeah.net>
# 
# License: LGPL-2.1

import numpy as np

class Particle:
    def __init__(self,func,num,dimension,C1,C2,w,LB,UB,IntCon,constraints,\
        Vmin,Vmax,initpos,initbestpos,initvelocity,initgroupbestpos,\
        creationfunction,\
        parallelized,verbose,options):

        self.func = func
        self.num = num
        self.dimension = dimension

        self.C1 = C1
        self.C2 = C2
        self.w = w
    
        self.LB = LB
        self.UB = UB
        self.IntCon = IntCon
        self.constraints = constraints

        self.Vmin = Vmin
        self.Vmax = Vmax
        
        self.pos = initpos
        self.bestpos = initbestpos
        self.velocity = initvelocity
        self.groupbestpos = initgroupbestpos

        self.verbose = verbose
        self.parallelized = parallelized
        self.options = options

        self.creationfunction = creationfunction

        self.initparticles()

    def initparticles(self):
        if self.velocity is None:
            self.velocity = np.random.random((self.num,self.dimension))
        if self.pos is None:
            self.pos = np.random.random((self.num,self.dimension))
        if self.bestpos is None:
            self.bestpos = np.random.random((self.num,self.dimension))
        if self.groupbestpos is None:
            self.groupbestpos = np.zeros(dimension)

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
        groupbest = self.func(self.groupbestpos) + self.constraints.fitness(self.groupbestpos)

        for i in range(self.num):
            value = self.func(self.pos[i]) + self.constraints.fitness(self.pos[i])
            bestvalue = self.func(self.bestpos[i]) + self.constraints.fitness(self.bestpos[i])

            if value < bestvalue:
                self.bestpos[i] = self.pos[i]
                bestvalue = self.func(self.bestpos[i]) + self.constraints.fitness(self.bestpos[i])

            if bestvalue < groupbestpos:
                self.groupbestpos = self.bestpos[i]
                groupbest = self.func(self.groupbestpos) + self.constraints.fitness(self.groupbestpos)
                
        if self.verbose:
            print 'Best Particle: {best}'.format(best=self.groupbestpos)

    def exchangeout(self,size):
        position = np.array(random.sample(range(self.num),size))
        return self.pos[position],position

    def exchangein(self,position,particles):
        self.pos[position] = particles
        return True

    def getbest(self):
        return self.groupbestpos,self.func(self.groupbestpos)
