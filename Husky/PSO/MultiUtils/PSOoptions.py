# Author: Yang Long <longyang_123@yeah.net>
#
# License: LGPL-2.1

class PSOoptions:
    def __init__(self):
        self.Creation = Creation()
        self.Pareto = Pareto()
        self.FitnessScale = FitnessScale()
        self.Mutation = Mutation()

class Creation:
    def __init__(self):
        self.args = dict()

class Pareto:
    def __init__(self):
        self.args = dict()

class FitnessScale:
    def __init__(self):
        self.args = dict()

class Mutation:
    def __init__(self):
        self.args = dict()