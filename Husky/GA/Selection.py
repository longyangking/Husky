import numpy as np

def Tournament(fitness,tournamentsize=3):
    bestindividual = fitness[np.random.randint(N,size=tournamentsize)]
    return np.argmin(bestindividual)

def StochasticUniform(fitness):
    # TODO
    pass

def Remainder(fitness):
    # TODO
    pass

def Roulette(fitness):
    # TODO
    pass

