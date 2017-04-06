import numpy as np

class State:
    def __init__(self,func,statesize,featuresize,LB,UB,IntCon,
        inittemperature,temperature,initstates,
        acceptancefunction,annealingfunction,temperaturefunction,
        parallelized,verbose,options):

        self.func = func
        self.statesize = statesize
        self.featuresize = featuresize
        self.T = initT
        if initstates is not None:
            self.states = initstates
        else:
            self.states = None

        self.Es = np.zeros(self.statesize)
        self.K = K

        if dT is not None:
            self.dT = dT
        else:
            self.dT = 1.0*initT/300
        
    def init(self):
        if self.states is None:
            self.states = np.random.random((self.statesize,self.featuresize))
            for i in range(self.statesize):
                self.Es[i] = self.func(self.states[i])
    
    def newstates(self):
        states = np.random.random((self.statesize,self.featuresize))
        Es = np.zeros(self.statesize)
        for i in range(self.statesize):
            Es[i] = self.func(states[i])
        return states,Es

    def cooling(self,tolerance):
        # Naive cooling, coming soon
        newstates,newEs = self.newstates()
        for i in range(self.statesize):
            dE = newEs[i] - self.Es[i]
            if dE < 0:
                self.states[i] = newstates[i]
                self.Es[i] = newEs[i]
            elif exp(-dE/(self.K*self.T)) > np.random.random():
                self.states[i] = newstates[i]
                self.Es[i] = newEs[i]
        
        self.T = self.T - self.dT
    
    def getresult(self):
        bestpos = np.argmin(self.Es)
        return self.states[bestpos],self.Es[bestpos]
            
