import numpy as np

def Uniform(particlesize,featuresize,LB,UB,Vmin,Vmax,IntCon,sargs):
    particles = np.zeros((particlesize,featuresize))
    if (LB is not None) and (UB is not None):
        for i in range(particlesize):
            particles[i] = LB + np.random.random(featuresize)*(UB - LB)
        return particles

    if LB is not None:
        for i in range(particlesize):
            particles[i] = LB + np.random.random(featuresize)
        return particles
    
    if UB is not None:
        for i in range(particlesize):
            particles[i] = UB - np.random.random(featuresize)
        return particles
    
    particles = np.random.random((particlesize,featuresize))
    velocity = np.random.random((particlesize,featuresize))       # TODO Modification is coming soon

    return particles,velocity
