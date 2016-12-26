import numpy as np
from Constraint import Constraints

class Candidates:
    def __init__(self,popsize,chromesize,constraints,IntCon=None):
        self.popsize = popsize
        self.chromesize = chromesize
        self.IntCon = IntCon
        self.constraints = constraints

    def init(self):
        