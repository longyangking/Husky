import numpy as np
import random

class State:
    def __init__(self,func,statesize,featuresize,LB,UB,IntCon,constraints,
        initstates,inittemperature,maxfunevals,
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
            self.inittemperature = inittemperature
            self.temperature = inittemperature
        else:
            self.inittemperature = (UB-LB)/2
            self.temperature = (UB-LB)/2

        self.k = np.ones(self.featuresize)
        self.maxfunevals = maxfunevals

        if initstates is not None:
            self.states = initstates
        else:
            self.states = np.zeros((self.statesize,self.featuresize))

        self.objectives = np.zeros(self.statesize)
        self.fitness = np.zeros(self.statesize)

        self.bestobjective = None
        self.bestfitness = None
        self.beststate = None

        self.acceptancefunction = acceptancefunction
        self.annealingfunction = annealingfunction
        self.temperaturefunction = temperaturefunction
        self.fitnessscalefunction = fitnessscalefunction

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
        self.adjustbeststate()

    def evaluate(self,states):
        (statesize,featuresize) = states.shape
        fitness = np.zeros(statesize)
        objectives = np.zeros(statesize)

        for i in range(statesize):
            fitness[i] = self.func(states[i]) + self.constraints.fitness(states[i])
            objectives[i] = self.func(states[i])

        return fitness,objectives

    def update(self):
        for i in range(self.maxfunevals):
            # Annealing
            states = self.annealingfunction(currenstates=self.states,LB=self.LB,UB=self.UB,IntCon=self.IntCon,
                temperature=self.temperature,args=self.options.Annealing.args)
            (fitness,objectives) = self.evaluate(states)

            # Whether to Accept
            delfitness = self.fitnessscalefunction(fitness=fitness-self.fitness,args=self.options.FitnessScale.args)
            acceptance = self.acceptancefunction(delE=delfitness,temperature=self.temperature,args=self.options.Acceptance.args)

            pos = np.where(acceptance)

            self.states[pos] = states[pos]
            self.fitness[pos] = fitness[pos]
            self.objectives[pos] = objectives[pos]

            self.adjustbeststate()
        # Update Temperature
        self.temperature = self.temperaturefunction(temperature=self.temperature,k=self.k,args=self.options.Temperature.args)

        if self.verbose:
            (beststate,bestobjective) = self.getbest()
            print 'Temperature {temperature} with objective {objective}'.format(temperature=self.temperature,objective=self.bestobjective)
    
    def reanneal(self):
        # Calculate s
        bounddiff = self.UB-self.LB
        bestpos = np.argmin(self.objectives)
        state = self.states[bestpos]

        value0 = self.fitness[bestpos]
        value1 = self.func(state+state/10000) + self.constraints.fitness(state+state/10000)
        diff = value1-value0
        s = np.abs(bounddiff*diff)
        smax = np.max(s)

        # Update k
        self.temperature[self.temperature==0] = 10000
        Tratio = self.inittemperature/self.temperature
        Sratio = smax/s     

        
        ratio = Tratio*Sratio
        #self.k[ratio==0] = 1000
        self.k = np.abs(np.log(ratio))

        self.k[np.isinf(self.k)] = 1.0
        self.temperature = self.temperature*Sratio  # TODO check the logic

        if self.verbose:
            print "Reanneal parameters: {k}".format(k=self.k)

    def exchangeout(self,statesize):
        pos = np.array(random.sample(range(self.statesize),statesize))
        return self.states[pos],pos

    def exchangein(self,pos,states):
        self.states[pos] = states

    def adjustbeststate(self):
        bestpos = np.argmin(self.fitness)
        beststate = self.states[bestpos]
        bestobjective = self.objectives[bestpos]
        bestfitness = self.fitness[bestpos]

        if bestfitness < self.bestfitness:
            self.bestobjective = bestobjective
            self.beststate = beststate
            self.bestfitness = bestfitness

    def getbest(self):
        bestpos = np.argmin(self.fitness)
        beststate = self.states[bestpos]
        bestobjective = self.objectives[bestpos]
        bestfitness = self.fitness[bestpos]

        if (self.beststate is None) or (bestfitness < self.bestfitness):
            return beststate,bestobjective
        else:
            return self.beststate,self.bestobjective

    def getallstates(self):
        return self.states,self.objectives
