# Author: Yang Long <longyang_123@yeah.net>
#
# License: LGPL-2.1

class SAoptions:
    def __init__(self):
        self.Acceptance = Acceptance()
        self.Annealing = Annealing()
        self.Temperature = Temperature()
        self.FitnessScale = FitnessScale()

class Acceptance():
    def __init__(self):
        self.args = dict()

class Annealing():
    def __init__(self):
        self.args = dict()

class Temperature():
    def __init__(self):
        self.args = dict()

class FitnessScale():
    def __init__(self):
        self.args = dict()
        self.args['factor'] = 1.0
        self.args['rate'] = 2.0
        self.args['quality'] = 0.4