import numpy as np
import random

class MultiState:
    def __init__(self,func,statesize,featuresize,targetsize,LB,UB,IntCon,constraints,
        initstates,inittemperature,maxfunevals,mutationrate,
        acceptancefunction,annealingfunction,temperaturefunction,fitnessscalefunction,distancefunction,mutationfunction,
        parallelized,verbose,options):

        self.func = func
        self.statesize = statesize
        self.featuresize = featuresize
        self.targetsize = targetsize

        self.LB = LB
        self.UB = UB
        self.IntCon = IntCon
        self.constraints = constraints

        if inittemperature is not None:
            self.inittemperature = inittemperature
            self.temperature = inittemperature
        else:
            self.inittemperature = self.statesize*np.ones(self.featuresize)       # max rank = 10
            self.temperature = self.statesize*np.ones(self.featuresize)

        self.k = np.ones(self.featuresize)
        self.maxfunevals = maxfunevals
        self.mutationrate = mutationrate

        if initstates is not None:
            self.states = initstates
        else:
            self.states = np.zeros((self.statesize,self.featuresize))

        self.objectives = np.zeros((self.statesize,self.targetsize))
        self.fitness = np.zeros((self.statesize,self.targetsize))

        self.bestobjectives = None
        self.bestfitness = None
        self.beststate = None

        self.acceptancefunction = acceptancefunction
        self.annealingfunction = annealingfunction
        self.temperaturefunction = temperaturefunction
        self.fitnessscalefunction = fitnessscalefunction
        self.distancefunction = distancefunction
        self.mutationfunction = mutationfunction

        self.parallelized = parallelized
        self.verbose = verbose
        self.options = options

        self.init()
        

    def init(self):
        for i in range(self.statesize):
            self.states[i] = self.LB + (self.UB-self.LB)*np.random.random(self.featuresize)
        # Integer Restriction
        if self.IntCon is not None:
            intstate = np.floor(self.states[:,self.IntCon])
            intstate = intstate + 1*(np.random.random(size=intstate.shape)>0.5)
            self.states[:,self.IntCon] = intstate

        (self.fitness,self.objectives) = self.evaluate(self.states)
        self.adjustfrontier()

    def evaluate(self,states):
        (statesize,featuresize) = states.shape
        fitness = np.zeros((statesize,self.targetsize))
        objectives = np.zeros((statesize,self.targetsize))

        for i in range(statesize):
            fitness[i] = np.array(self.func(states[i])) + self.constraints.fitness(states[i])*np.ones(self.targetsize)
            objectives[i] = np.array(self.func(states[i]))

        return fitness,objectives       

    def update(self):
        for i in range(self.maxfunevals):
            # Annealing
            states = self.annealingfunction(currenstates=self.states,LB=self.LB,UB=self.UB,IntCon=self.IntCon,
                temperature=self.temperature/self.statesize,args=self.options.Annealing.args)
            
            states = self.mutationfunction(states,LB=self.LB,UB=self.UB,mutationrate=self.mutationrate,IntCon=self.IntCon,args=self.options.Mutation.args)

            (fitness,objectives) = self.evaluate(states)

            # Whether to Accept
            paretofitness = np.concatenate((self.fitness,fitness))
            paretofitness = self.fitnessscalefunction(fitness=paretofitness,args=self.options.FitnessScale.args)
            rank,distance = self.distancefunction(paretofitness,args=self.options.Pareto.args)
            drank = rank[self.statesize:] - rank[:self.statesize]
            ddistance = distance[self.statesize:] - distance[:self.statesize]
            acceptance = self.acceptancefunction(drank=drank,ddistance=ddistance,temperature=self.temperature,args=self.options.Acceptance.args)

            pos = np.where(acceptance)

            self.states[pos] = states[pos]
            self.fitness[pos] = fitness[pos]
            self.objectives[pos] = objectives[pos]

            self.adjustfrontier()
        # Update Temperature
        self.temperature = self.temperaturefunction(temperature=self.temperature,k=self.k,args=self.options.Temperature.args)

        #print self.beststate, self.bestobjectives

        if self.verbose:
            print('Temperature {temperature} with number of pareto frontier:{num}'.format(temperature=self.temperature,num=np.size(self.bestfitness,axis=0)))
    
    def reanneal(self):
        # Calculate s
        #bounddiff = self.UB-self.LB
        #state = self.beststate

        #value0 = np.mean(self.bestfitness,axis=0)
        #value1 = self.func(np.mean(state+state/10000,axis=0)) + self.constraints.fitness(np.mean(state+state/10000,axis=0))
        #diff = value1-value0
        #s = np.max(np.abs(bounddiff*diff))
        #smax = np.max(s)

        # Update k
        self.temperature = np.ones(self.featuresize)
        #self.temperature[self.temperature==0] = 1
        #Tratio = self.inittemperature/self.temperature
        #Sratio = smax/s     
        #ratio = Tratio*Sratio

        #self.k[ratio==0] = 1000
        #self.k = np.abs(np.log(ratio))

        #self.k[np.isinf(self.k)] = 1.0
        #self.temperature = self.temperature*Sratio  # TODO check the logic
        self.k = 1

        if self.verbose:
            print("Reanneal parameters: {k}".format(k=self.k))

    def exchangeout(self,statesize):
        pos = np.array(random.sample(range(self.statesize),statesize))
        return self.states[pos],pos

    def exchangein(self,pos,states):
        self.states[pos] = states

    def adjustfrontier(self):
        if self.bestobjectives is None:
            rank,distance = self.distancefunction(self.fitness,args=self.options.Pareto.args)
            pos = np.where(rank==0)
            self.beststate = self.states[pos]
            self.bestfitness = self.fitness[pos]
            self.bestobjectives = self.objectives[pos]

        paretofitness = np.concatenate((self.bestfitness,self.fitness))
        paretostates = np.concatenate((self.beststate,self.states))
        paretoobjectives = np.concatenate((self.bestobjectives,self.objectives))
        rank,distance = self.distancefunction(paretofitness,args=self.options.Pareto.args)
        pos = np.where(rank==0)

        self.bestobjectives = paretoobjectives[pos]
        self.beststate = paretostates[pos]
        self.bestfitness = paretofitness[pos]

    def getfrontier(self):
        return self.beststate,self.bestobjectives

    def getallstates(self):
        return self.states,self.objectives
