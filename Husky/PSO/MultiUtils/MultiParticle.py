# Author: Yang Long <longyang_123@yeah.net>
# 
# License: LGPL-2.1

import numpy as np
import Pareto

class MultiParticle:
    def __init__(self,func,particlesize,featuresize,targetsize,C1,C2,w,LB,UB,IntCon,constraints,\
        initpos,initbestpos,initvelocity,initgroupbestpos,\
        creationfunction,minfractionneighbors,distancefunction,mutationfunction,\
        algorithm,parallelized,verbose,options):

        self.func = func
        self.particlesize = particlesize
        self.featuresize = featuresize
        self.targetsize = targetsize

        self.C1 = C1
        self.C2 = C2
        self.w = w
    
        self.LB = LB
        self.UB = UB
        self.IntCon = IntCon
        self.constraints = constraints
        
        self.pos = initpos
        self.velocity = initvelocity

        self.bestpos = initbestpos
        self.groupbestpos = initgroupbestpos

        self.algorithm = algorithm
        self.verbose = verbose
        self.parallelized = parallelized
        self.options = options

        self.minfractionneighbors = minfractionneighbors
        self.mutationfunction = mutationfunction
        self.creationfunction = creationfunction
        self.distancefunction = distancefunction

        self.initparticles()

    def initparticles(self):
        pos,velocity = self.creationfunction(self.particlesize,self.featuresize,\
                        LB=self.LB,UB=self.UB,IntCon=self.IntCon,\
                        args=self.options.Creation.args)

        if self.velocity is None:
            self.velocity = velocity
        else:
            self.velocity = np.array(self.velocity)

        if self.pos is None:
            self.pos = pos
        else:
            self.pos = np.array(self.pos)

        if self.bestpos is None:
            self.bestpos = pos          # Can be improved
        else:
            self.bestpos = np.array(self.bestpos)

        if self.groupbestpos is None:
            self.groupbestpos = np.array([])  # Can be improved
        else:
            self.groupbestpos = np.array(self.groupbestpos)

        self.evaluate()

    def update(self):
        # Naive update
        R1 = np.random.random((self.particlesize,self.featuresize))
        R2 = np.random.random((self.particlesize,self.featuresize))

        # Algorithm Setting here
        groupbestpos = self.groupbestpos[np.random.randint(len(self.groupbestpos),size=self.particlesize)]
        V = self.w*self.velocity + self.C1*R1*(self.bestpos-self.pos) + self.C2*R2*(groupbestpos-self.pos)

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
        length = 2*self.particlesize + len(self.groupbestpos)
        fitness = np.zeros((length,self.targetsize))
        pos = np.zeros((length,self.featuresize))

        # TODO Can be optimized here!
        for i in range(self.particlesize):
            pos[i] = self.pos[i]
            fitness[i] = np.array(self.func(self.pos[i])) + self.constraints.fitness(self.pos[i])
            pos[i+self.particlesize] = self.bestpos[i]
            fitness[i+self.particlesize] = np.array(self.func(self.bestpos[i])) + self.constraints.fitness(self.bestpos[i])
        
        if len(self.groupbestpos) > 0:
            for i in range(len(self.groupbestpos)):
                pos[i+2*self.particlesize] = self.groupbestpos[i]
                fitness[i+2*self.particlesize] = np.array(self.func(self.groupbestpos[i])) + self.constraints.fitness(self.groupbestpos[i])

        rank,distance = Pareto.FastNonDominatedSorting(fitness,args=self.options.Pareto.args)

        groupbestindex = np.where(rank==0)
        self.groupbestpos[groupbestindex] = pos[groupbestindex]

        for i in range(self.particlesize):
            if (rank[i] < rank[i+self.particlesize]) or ((rank[i] == rank[i+self.particlesize]) and (distance[i] > distance[i+self.particlesize])):
                self.bestpos[i] = self.pos[i]
                
        if self.verbose:
            print 'The number of particles in best group position: {best}'.format(best=len(self.groupbestpos))

    def exchangeout(self,size):
        position = np.array(random.sample(range(self.particlesize),size))
        return self.pos[position],position

    def exchangein(self,position,particles):
        self.pos[position] = particles
        return True
    
    def getallparticles(self):
        objectives = np.zeros(self.particlesize)
        for i in range(self.particlesize):
            objectives[i] = np.array(self.func(self.pos[i]))
        return self.pos,objectives

    def getbest(self):
        objectives = np.zeros(len(self.groupbestpos),self.targetsize)
        for i in range(len(self.groupbestpos)):
            objectives[i] = np.array(self.func(self.groupbestpos[i]))
        return self.groupbestpos,objectives
