import numpy as np

def Uniform(particlesize,featuresize,LB,UB,IntCon,args):
    particles = np.random.random((particlesize,featuresize))
    if (LB is not None) and (UB is not None):
        for i in range(particlesize):
            particles[i] = LB + np.random.random(featuresize)*(UB - LB)

    if LB is not None:
        for i in range(particlesize):
            particles[i] = LB + np.random.random(featuresize)
    
    if UB is not None:
        for i in range(particlesize):
            particles[i] = UB - np.random.random(featuresize)
    
    if IntCon is not None:
        intpos = np.floor(particles[:,IntCon])
        intpos = intpos + 1*(np.random.random(size=intpos.shape)>0.5)
        particles[:,IntCon] = intpos

    velocity = np.random.random((particlesize,featuresize))       # TODO Modification is coming soon

    return particles,velocity
