# Author: Yang Long <longyang_123@yeah.net>
#
# License: LGPL-2.1

import numpy as np

def Laplacian(parents,fitness,LB,UB,IntCon=None,a=0,breal=0.5,bint=0.75):
    '''
    Laplacian Crossover Operator (Two parents, Two childs: Son & Girl)
    '''
    (M,N) = np.shape(parents)
    childs = np.zeros([M,N])
    index = 0
    while index < M:
        fatherindex = np.random.randint(M)
        motherindex = np.random.randint(M)
        while fatherindex == motherindex:
            motherindex = np.random.randint(M)

        r = np.random.random(N)
        u = np.random.random(N)
        beta = a + breal*np.log(u)*(r>0.5) - breal*np.log(u)*(r<=0.5)
        if IntCon is not None:
            beta[IntCon] = a + bint*np.log(u[IntCon])*(r[IntCon]>0.5) - bint*np.log(u[IntCon])*(r[IntCon]<=0.5)

        father = parents[fatherindex]
        mother = parents[motherindex]
        son = father + beta*np.abs(father - mother)
        girl = mother + beta*np.abs(father - mother)

        childs[index] = son
        childs[index+1] = girl

        index = index + 2
    
    # Constraint childs with LB, UB and IntCon
    for i in range(M):
        child = childs[i]
       
        if IntCon is not None:
            intchild = np.floor(child[IntCon])
            intchild = intchild + 1*(np.random.random(size=np.size(intchild))>0.5)
            child[IntCon] = intchild

        posLB = np.where(child<LB)
        child[posLB] = LB[posLB]        

        posUB = np.where(child>UB)
        child[posUB] = UB[posUB]        
            
        childs[i] = child

    return childs

def Scattered(parents,fitness,LB,UB,IntCon=None):
    '''
    Crossover based on the random binary control vector
    '''
    (M,N) = np.shape(parents)
    childs = np.zeros([M,N])
    index = 0
    while index < M:
        fatherindex = np.random.randint(M)
        motherindex = np.random.randint(M)
        while fatherindex == motherindex:
            motherindex = np.random.randint(M)
        
        p = np.random.randint(2,size=N)

        father = parents[fatherindex]
        mother = parents[motherindex]
        son = father*(p==1) + mother*(p==0)
        girl = father*(p==0) + mother*(p==1)

        childs[index] = son
        childs[index+1] = girl

        index = index + 2
    
    # Constraint childs with LB, UB and IntCon
    for i in range(M):
        child = childs[i]
       
        if IntCon is not None:
            intchild = np.floor(child[IntCon])
            intchild = intchild + 1*(np.random.random(size=np.size(intchild))>0.5)
            child[IntCon] = intchild

        posLB = np.where(child<LB)
        child[posLB] = LB[posLB]        

        posUB = np.where(child>UB)
        child[posUB] = UB[posUB]        
            
        childs[i] = child

    return childs

def SinglePoint(parents,fitness,LB,UB,IntCon=None):
    '''
    Crossover based on a random point
    '''
    (M,N) = np.shape(parents)
    childs = np.zeros([M,N])
    index = 0
    while index < M:
        fatherindex = np.random.randint(M)
        motherindex = np.random.randint(M)
        while fatherindex == motherindex:
            motherindex = np.random.randint(M)
        
        pos = np.random.randint(1,N)

        father = parents[fatherindex]
        mother = parents[motherindex]
        son = father[:pos] + mother[pos:]
        girl = mother[:pos] + father[pos:]

        childs[index] = son
        childs[index+1] = girl

        index = index + 2
    
    # Constraint childs with LB, UB and IntCon
    for i in range(M):
        child = childs[i]
       
        if IntCon is not None:
            intchild = np.floor(child[IntCon])
            intchild = intchild + 1*(np.random.random(size=np.size(intchild))>0.5)
            child[IntCon] = intchild

        posLB = np.where(child<LB)
        child[posLB] = LB[posLB]        

        posUB = np.where(child>UB)
        child[posUB] = UB[posUB]        
            
        childs[i] = child

    return childs

def TwoPoint(parents,fitness,LB,UB,IntCon=None):
    '''
    Crossover based on two random points
    '''
    (M,N) = np.shape(parents)
    childs = np.zeros([M,N])
    index = 0
    while index < M:
        fatherindex = np.random.randint(M)
        motherindex = np.random.randint(M)
        while fatherindex == motherindex:
            motherindex = np.random.randint(M)
        
        start = np.random.randint(N-1)
        end = np.random.randint(start,N)

        father = parents[fatherindex]
        mother = parents[motherindex]
        son = father[start:end] + mother[:start] + mother[end:]
        girl = mother[start:end] + father[:start] + father[end:]

        childs[index] = son
        childs[index+1] = girl

        index = index + 2
    
    # Constraint childs with LB, UB and IntCon
    for i in range(M):
        child = childs[i]
       
        if IntCon is not None:
            intchild = np.floor(child[IntCon])
            intchild = intchild + 1*(np.random.random(size=np.size(intchild))>0.5)
            child[IntCon] = intchild

        posLB = np.where(child<LB)
        child[posLB] = LB[posLB]        

        posUB = np.where(child>UB)
        child[posUB] = UB[posUB]        
            
        childs[i] = child

    return childs

def Intermediate(parents,fitness,LB,UB,IntCon=None,ratio=1.0):
    '''
    Crossover based on the intermediate evolution
    '''
    (M,N) = np.shape(parents)
    childs = np.zeros([M,N])
    index = 0
    while index < M:
        fatherindex = np.random.randint(M)
        motherindex = np.random.randint(M)
        while fatherindex == motherindex:
            motherindex = np.random.randint(M)
        
        father = parents[fatherindex]
        mother = parents[motherindex]
        son = father + ratio*np.random.random(size=N)*(mother - father)
        girl = mother + ratio*np.random.random(size=N)*(father - mother)

        childs[index] = son
        childs[index+1] = girl

        index = index + 2
    
    # Constraint childs with LB, UB and IntCon
    for i in range(M):
        child = childs[i]
       
        if IntCon is not None:
            intchild = np.floor(child[IntCon])
            intchild = intchild + 1*(np.random.random(size=np.size(intchild))>0.5)
            child[IntCon] = intchild

        posLB = np.where(child<LB)
        child[posLB] = LB[posLB]        

        posUB = np.where(child>UB)
        child[posUB] = UB[posUB]        
            
        childs[i] = child

    return childs

def Heuristic(parents,fitness,LB,UB,IntCon=None,R=1.2):
    '''
    Evolve with the direction to better parent
    '''
    (M,N) = np.shape(parents)
    childs = np.zeros([M,N])
    index = 0
    while index < M:
        fatherindex = np.random.randint(M)
        motherindex = np.random.randint(M)
        while fatherindex == motherindex:
            motherindex = np.random.randint(M)

        father = parents[fatherindex]
        fatherfitness = fitness[fatherfitness]
        mother = parents[motherindex]
        motherfitness = fitness[motherfitness]
 
        son = father + (fatherfitness>motherfitness)*R*(father - mother) + (fatherfitness<=motherfitness)*R*(mother - father)
        girl = mother + (fatherfitness>motherfitness)*R*(father - mother) + (fatherfitness<=motherfitness)*R*(mother - father)

        childs[index] = son
        childs[index+1] = girl

        index = index + 2
    
    # Constraint childs with LB, UB and IntCon
    for i in range(M):
        child = childs[i]
       
        if IntCon is not None:
            intchild = np.floor(child[IntCon])
            intchild = intchild + 1*(np.random.random(size=np.size(intchild))>0.5)
            child[IntCon] = intchild

        posLB = np.where(child<LB)
        child[posLB] = LB[posLB]        

        posUB = np.where(child>UB)
        child[posUB] = UB[posUB]        
            
        childs[i] = child

    return childs

def Arithmetic(parents,fitness,LB,UB,constraints,IntCon=None):
    # TODO This part will be done after the completement of module Optimize
    return TwoPoint(parents,fitness,LB,UB,IntCon)