# Author: Yang Long <longyang_123@yeah.net>
# 
# License: LGPL-2.1

import numpy as np
from . import Pareto

class MultiParticle:
    def __init__(self,func,particlesize,featuresize,targetsize,C1,C2,w,LB,UB,IntCon,constraints,\
        initpos,initbestpos,initvelocity,initgroupbestpos,\
        creationfunction,minfractionneighbors,distancefunction,fitnessscalefunction,mutationfunction,\
        mutationrate,parallelized,verbose,options):

        self.func = func
        self.particlesize = particlesize
        self.featuresize = featuresize
        self.targetsize = targetsize

        self.C1 = C1
        self.C2 = C2
        self.w = w
    
        if LB is not None:
            self.LB = np.array(LB)
        else:
            self.LB = LB
        
        if UB is not None:
            self.UB = np.array(UB)
        else:
            self.UB = UB
        
        if IntCon is not None:
            self.IntCon = np.array(IntCon)
        else:
            self.IntCon = IntCon

        self.constraints = constraints
        
        self.pos = initpos
        self.velocity = initvelocity

        self.bestpos = initbestpos
        self.groupbestpos = initgroupbestpos

        self.verbose = verbose
        self.parallelized = parallelized
        self.options = options

        self.mutationrate = mutationrate
        self.minfractionneighbors = minfractionneighbors
        self.fitnessscalefunction = fitnessscalefunction
        self.creationfunction = creationfunction
        self.distancefunction = distancefunction
        self.mutationfunction = mutationfunction

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

        pos,velocity = self.creationfunction(self.particlesize,self.featuresize,\
                        LB=self.LB,UB=self.UB,IntCon=self.IntCon,\
                        args=self.options.Creation.args)

        if self.bestpos is None:
            self.bestpos = pos          # Can be improved
        else:
            self.bestpos = np.array(self.bestpos)

        if self.groupbestpos is None:
            self.groupbestpos = None  # Can be improved
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

        if self.IntCon is not None:
            intpos = np.floor(self.pos[:,self.IntCon])
            intpos = intpos + 1*(np.random.random(size=intpos.shape)>0.5)
            self.pos[:,self.IntCon] = intpos
        
        if self.LB is not None:
            for i in range(self.featuresize):
                posLB = np.where(self.pos[:,i]<self.LB[i])
                self.pos[posLB,i] = self.LB[i]
        
        if self.UB is not None:
            for i in range(self.featuresize):
                posUB = np.where(self.pos[:,i]>self.UB[i])
                self.pos[posUB,i] = self.UB[i]
       
        self.mutation()
        self.evaluate()

        if self.verbose:
            print('The number of particles in best group position: {best}'.format(best=len(self.groupbestpos)))

    def mutation(self):
        fitness = np.zeros((self.particlesize,self.targetsize))
        for i in range(self.particlesize):
            fitness[i] = np.array(self.func(self.pos[i])) + self.constraints.fitness(self.pos[i])
        
        scaledfitness = self.fitnessscalefunction(fitness,args=self.options.FitnessScale.args)
        rank,distance = Pareto.FastNonDominatedSorting(scaledfitness,args=self.options.Pareto.args)

        self.pos = self.mutationfunction(self.pos,rank,distance,self.LB,self.UB,self.mutationrate,self.IntCon,
                        args=self.options.Mutation.args)

    def evaluate(self):
        length = 2*self.particlesize
        fitness = np.zeros((length,self.targetsize))
        pos = np.zeros((length,self.featuresize))

        # Update Particle Best Positions
        for i in range(self.particlesize):
            pos[i] = self.pos[i]
            fitness[i] = np.array(self.func(self.pos[i])) + self.constraints.fitness(self.pos[i])
            pos[i+self.particlesize] = self.bestpos[i]
            fitness[i+self.particlesize] = np.array(self.func(self.bestpos[i])) + self.constraints.fitness(self.bestpos[i])
        
        scaledfitness = self.fitnessscalefunction(fitness,args=self.options.FitnessScale.args)
        rank,distance = Pareto.FastNonDominatedSorting(scaledfitness,args=self.options.Pareto.args)

        for i in range(self.particlesize):
            if (rank[i] < rank[i+self.particlesize]) or ((rank[i] == rank[i+self.particlesize]) and (distance[i] > distance[i+self.particlesize])):
                self.bestpos[i] = self.pos[i]
      
        # Update Group Best Positions
        if self.groupbestpos is not None:
            pos = np.concatenate((self.bestpos,self.groupbestpos))
        else:
            pos = self.bestpos
        fitness = np.zeros((len(pos),self.targetsize)) 
        for i in range(len(pos)):
            fitness[i] = np.array(self.func(pos[i])) + self.constraints.fitness(pos[i])

        scaledfitness = self.fitnessscalefunction(fitness,args=self.options.FitnessScale.args)
        rank,distance = Pareto.FastNonDominatedSorting(scaledfitness,args=self.options.Pareto.args)

        groupbestindex = np.where(rank==0)
        self.groupbestpos = pos[groupbestindex]

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
        objectives = np.zeros((len(self.groupbestpos),self.targetsize))
        for i in range(len(self.groupbestpos)):
            objectives[i] = np.array(self.func(self.groupbestpos[i]))
        return self.groupbestpos,objectives
