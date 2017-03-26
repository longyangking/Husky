# Author: Yang Long <longyang_123@yeah.net>
# 
# License: LGPL-2.1

import numpy as np

class Particle:
    def __init__(self,func,particlesize,featuresize,C1,C2,w,LB,UB,IntCon,constraints,\
        initpos,initbestpos,initvelocity,initgroupbestpos,\
        creationfunction,minfractionneighbors,\
        parallelized,verbose,options):

        self.func = func
        self.particlesize = particlesize
        self.featuresize = featuresize

        self.C1 = C1
        self.C2 = C2
        self.w = w
    
        self.LB = LB
        self.UB = UB
        self.IntCon = IntCon
        self.constraints = constraints
        
        self.pos = initpos
        self.bestpos = initbestpos
        self.velocity = initvelocity
        self.groupbestpos = initgroupbestpos

        self.verbose = verbose
        self.parallelized = parallelized
        self.options = options

        self.minfractionneighbors = minfractionneighbors
        self.creationfunction = creationfunction

        self.initparticles()

    def initparticles(self):
        pos,velocity = self.creationfunction(self.particlesize,self.featuresize,\
                        LB=self.LB,UB=self.UB,IntCon=self.IntCon,\
                        args=self.options.Creation.args)

        if self.velocity is None:
            self.velocity = velocity
        if self.pos is None:
            self.pos = pos
        if self.bestpos is None:
            self.bestpos = pos          # Can be improved
        if self.groupbestpos is None:
            self.groupbestpos = np.zeros(self.featuresize)  # Can be improved

        self.evaluate()

    def update(self):
        # Naive update
        R1 = np.random.random((self.particlesize,self.featuresize))
        R2 = np.random.random((self.particlesize,self.featuresize))
        V = self.w*self.velocity + self.C1*R1*(self.bestpos-self.pos) + self.C2*R2*(self.groupbestpos-self.pos)
        self.velocity = V
        self.pos = self.pos + V
        
        if self.LB is not None:
            posLB = np.where(self.pos<LB)
            self.pos[posLB] = LB[posLB]
        
        if self.UB is not None:
            posUB = np.where(self.pos>UB)
            self.pos[posUB] = UB[posUB]

        if self.IntCon is not None:
            intpos = np.floor(self.pos[:,self.IntCon])
            intpos = intpos + 1*(np.random.random(size=intpos.shape)>0.5)
            self.pos[:,self.IntCon] = intpos

        self.evaluate()

    def evaluate(self):
        groupbest = self.func(self.groupbestpos) + self.constraints.fitness(self.groupbestpos)

        for i in range(self.particlesize):
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
        position = np.array(random.sample(range(self.particlesize),size))
        return self.pos[position],position

    def exchangein(self,position,particles):
        self.pos[position] = particles
        return True
    
    def getallparticles(self):
        objectives = np.zeros(self.particlesize)
        for i in range(self.particlesize):
            objectives[i] = self.func(self.pos[i])
        return pos,objectives

    def getbest(self):
        return self.groupbestpos,self.func(self.groupbestpos)
