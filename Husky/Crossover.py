import numpy as np

def Crossover(chromes,fitness,LB,UB,IntCon,a=0,breal=0.5,bint=1):
    (M,N) = np.shape(chromes)
    newchromes = np.zeros([M,N])
    newpopsize = 0
    while newpopsize<M:
        father = Selection(chromes,fitness)
        mother = Selection(chromes,fitness)
        while father == mother:
            mother = Selection(chromes,fitness)

        r = np.random.random(N)
        u = np.random.random(N)
        beta = a + b*np.log(u)*(r>0.5) - b*np.log(u)*(r<=0.5)

        x1 = chromes[father,:]
        x2 = chromes[mother,:]
        y1 = x1 + beta*np.abs(x1-x2)
        y2 = x2 + beta*np.abs(x1-x2)

        newchromes[newpopsize,:] = IntegerStriction(y1,LB,UB,IntCon)
        newchromes[newpopsize+1,:] = IntegerStriction(y2,LB,UB,IntCon)

        newpopsize = newpopsize + 2

    return newchromes

