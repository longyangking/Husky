import numpy as np

from collections import deque

class Constraints(object):
    def __init__(self):
        self.table = deque()

    def add(self,constraintfunc,penalty=100):
        self.table.append((constraintfunc,penalty))

    def numberofconstraints(self):
        return len(self.table)
    
    def get(self,index):
        N = len(self.table)
        if (index >=0) and (index < N):
            return self.table[index]
        if index >= N:
            return self.table[(index%N)+1]
        if index < 0:
            return self.table[index%N]

    def fitness(self,feature):
        N = len(self.table)
        totalpenalty = 0
        for i in range(N):
            (func,penalty) = self.table[i]
            totalpenalty += penalty*np.square(np.abs(func(feature)))
        return totalpenalty