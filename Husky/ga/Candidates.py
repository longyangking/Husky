import numpy as np
import random

class Candidates(object):
    def __init__(self,popsize,chromsize,fitnessfun):
        self.popsize = popsize
        self.chromsize = chromsize
        self.fitnessfun = fitnessfun
        self.fitness = np.zeros([popsize,1])
        self.chroms = np.zeros([popsize,chromsize])

    def randinit(self):
        self.chroms = np.random.randint(2,size=(self.popsize,self.chromsize))        

    def mutate(self,pmutate):
        temp = self.chroms.reshape(self.popsize*self.chromsize,1)
        self.chroms = np.array(map(lambda x:self.__mutateChrome(x,pmutate),temp)).reshape(self.popsize,self.chromsize)

    def __mutateChrome(self,x,pmutate):
        if random.random() < pmutate:
            return (x+1)%2
        return x

    def cross(self,pcross,lencross):
        for i in range(self.popsize):
            if random.random() < pcross:
                father = random.randinit(0,self.popsize-1)
                mother = random.randinit(0,self.popsize-1)
                while father == mother:
                    mother = random.randinit(0,self.popsize-1)
                crossChrome = random.randinit(0,self.chromsize-lencross-1)
                
                gene = self.chroms[father][crossChrome:crossChrome+lencross-1]
                self.chroms[father][crossChrome:crossChrome+lencross-1] = self.chroms[mother][crossChrome:crossChrome+lencross-1]
                self.chroms[mother][crossChrome:crossChrome+lencross-1] = gene

    
    def fit(self):
        for i in range(self.popsize):
            self.fitness[i] = self.fitnessfun(self.chroms[i])

    def eliminate(self,size):
        '''
        Leave size of best candidates and regenerate new generation in popsize-size
        '''
        self.fit()
        fitnessorder = sorted(self.fitness,reverse=True)
        bestchroms = np.zeros([size,chromsize])
        for i in range(size):
            bestchroms[i] = self.chroms[fitness.index(fitnessorder[i])]
        self.randinit() #All left will be regenerated randomly
        for i in range(size):
            self.chroms[i] = bestchroms[i]

    def getcandidate(self,index):
        return self.chroms[index]

