# Author: Yang Long <longyang_123@yeah.net>
#
# License: LGPL-2.1

import numpy as np

def Laplacian(parents,rank,distance,LB,UB,IntCon,args):
    '''
    Laplacian Crossover Operator (Two parents, Two childs: Son & Girl)
    '''
    a = 0
    breal = 0.5
    bint = 0.75
    if args.has_key('a'):
        a = args['a']
    if args.has_key('breal'):
        breal = args['breal']
    if args.has_key('bint'):
        bint = args['bint']

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

def Scattered(parents,rank,distance,LB,UB,IntCon,args):
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

def SinglePoint(parents,rank,distance,LB,UB,IntCon,args):
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
        son = np.concatenate((father[:pos], mother[pos:]))
        girl = np.concatenate((mother[:pos], father[pos:]))

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

def TwoPoint(parents,rank,distance,LB,UB,IntCon,args):
    '''
    Crossover based on two random points (Default)
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

        son = np.concatenate((mother[:start], father[start:end], mother[end:]))
        girl = np.concatenate((father[:start], mother[start:end], father[end:]))

        childs[index] = son
        if index+1 < M:                 # Odd number of parents
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

def Intermediate(parents,rank,distance,LB,UB,IntCon,args):
    '''
    Crossover based on the intermediate evolution
    '''
    ratio = 1.0
    if args.has_key('ratio'):
        ratio = args['ratio']

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

def Heuristic(parents,rank,distance,LB,UB,IntCon,args):
    '''
    Evolve with the direction to better parent
    '''
    R = 1.2
    if args.has_key('R'):
        R = args['R']

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

def LogisticChaoticSequence(parents,rank,distance,LB,UB,IntCon,args):
    # TODO This part will be done after the completement of module Optimize
    return TwoPoint(parents,rank,distance,LB,UB,IntCon)

def Arithmetic(parents,rank,distance,LB,UB,IntCon,args):
    # TODO This part will be done after the completement of module Optimize
    return TwoPoint(parents,rank,distance,LB,UB,IntCon)
