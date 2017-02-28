import numpy as np

def Mutation(chromes,LB,UB,IntCon,preal=0.5,pint=1):
    (M,N) = np.shape(chromes)
    newchromes = np.zeros([M,N])

    for i in range(M):
        chrome = chromes[i,:]
        P = preal*np.ones(N)
        P[IntCon] = pint
        s = np.random.random(N)**p
        r = np.random.random(N)
        t = (chrome-LB)/(UB-chrome)
        newchrome = chrome - s*(chrome-LB)*(r>t) + s*(UB-chrome)*(r-t)
        newchromes[i,:] = IntegerStriction(newchrome,LB,UB,IntCon)

    return newchromes

def SinglePoint():
    # TODO
    pass

def Gaussian():
    # TODO
    pass

def Uniform():
    # TODO
    pass

def AdaptiveFeasible():
    # TODO
    pass