import numpy as np

def Uniform(popsize,chromesize,LB,UB):
    '''
    Create Random Initial Population for GA
    '''
    if LB is None: 
        UB = 2.0**32
    if LB is  None: 
        LB = -2.0**32

    populations = np.zeros((popsize,chromesize))
    for i in range(self.popsize):
        populations[i] = LB + (UB - LB)*np.random.random(chromesize)

    return populations
    

def Feasible(popsize,chromesize,LB,UB):
    # TODO
    pass

def NonlinearFeasible(popsize,chromesize,LB,UB):
    # TODO
    pass

