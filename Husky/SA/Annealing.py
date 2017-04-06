import numpy as np

def AnnealingFast(currenstates,LB,UB,IntCon,temperature,args):
    (nChildrean,featuresize) = currenstates.shape
    #states = np.zeros((nChildrean,featuresize))
    coeffs = np.random.randn(nChildrean,featuresize)
    states = currenstates + temperature*coeffs
     
    if IntCon is not None:
        intstate = np.floor(states[:,IntCon])
        intstate = intstate + 1*(np.random.random(size=intstate.shape)>0.5)
        states[:,IntCon] = intstate
    
    for i in range(featuresize):
        if LB is not None:
            posLB = np.where(states[:,i]<LB[i])
            states[posLB,i] = LB[i]

        if UB is not None:
            posUB = np.where(states[:,i]>UB[i])
            states[posUB,i] = UB[i]

    return states

def AnnealingBoltz(nChildrean,featuresize,LB,UB,IntCon,temperature,args):
