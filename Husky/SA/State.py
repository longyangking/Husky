import numpy as np
import random

class State:
    def __init__(self,func,statesize,featuresize,LB,UB,IntCon,constraints,
        initstates,inittemperature,
        acceptancefunction,annealingfunction,temperaturefunction,fitnessscalefunction,
        parallelized,verbose,options):

        self.func = func
        self.statesize = statesize
        self.featuresize = featuresize

        self.LB = LB
        self.UB = UB
        self.IntCon = IntCon
        self.constraints = constraints

        if inittemperature is not None:
            self.temperature = inittemperature
        else:
            self.temperature = (UB-LB)/2

        self.k = np.ones(self.featuresize)

        if initstates is not None:
            self.states = initstates
        else:
            self.states = np.zeros((self.statesize,self.featuresize))

        self.objectives = np.zeros(self.statesize)
        self.fitness = np.zeros(self.statesize)

        self.acceptancefunction = acceptancefunction
        self.annealingfunction = annealingfunction
        self.temperaturefunction = temperaturefunction
        self.fitnessscalefunction = fitnessscalefunction

        self.parallelized = parallelized
        self.verbose = verbose
        self.options = options

        self.init()
        self.evaluate()
        
    def init(self):
        for i in range(self.statesize):
            self.states[i] = self.LB + (self.UB-self.LB)*np.random.random(self.featuresize)
        # Integer Restriction
        if IntCon is not None:
            intstate = np.floor(states[:,IntCon])
            intstate = intstate + 1*(np.random.random(size=intstate.shape)>0.5)
            states[:,IntCon] = intstate

    def evaluate(self):
        for i in range(self.statesize):
            self.fitness[i] = self.func(self.states[i])
                + self.constraints.fitness(self.states[i])
            self.objectives[i] = self.func(self.states[i])

    def update(self):
        self.states = self.annealingfunction(currenstates=self.states,
            LB=self.LB,UB=self.UB,IntCon=self.IntCon,
            temperature=self.temperature,
            options=self.options.Annealing.args)
    
    def reanneal(self):
        

    def exchangeout(self,statesize):
        pos = np.array(random.sample(range(self.statesize),statesize))
        return self.states[pos],pos

    def exchangein(self,pos,states):
        self.states[pos] = states

    def getbest(self):
        bestpos = np.argmin(self.objectives)
        return self.states[bestpos],self.objectives[bestpos]

    def getallstates(self):
        return self.states,self.objectives
