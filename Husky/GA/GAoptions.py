# Author: Yang Long <longyang_123@yeah.net>
#
# License: LGPL-2.1

import numpy as np
from . import Creation
from . import Selection
from . import FitnessScale
from . import Mutation
from . import Crossover

class GAoptions:
    '''
    Set parameter for GA
    '''
    def __init__(self):
        self.Creation = Creation()
        self.Selection = Selection()
        self.FitnessScale = FitnessScale()
        self.Crossover = Crossover()
        self.Mutation = Mutation()

    def setparameter(self,section,parameter,value):
        '''
        Set parameter for single request
        '''
        if section == 'System':
            # TODO the options of system
            return True
        if section == 'Creation':
            return self.Creation.setparameter(parameter,value)
        if section == 'Selection':
            return self.Selection.setparameter(parameter,value)
        if section == 'FitnessScale':
            return self.FitnessScale.setparameter(parameter,value)
        if section == 'Crossover':
            return self.Crossover.setparameter(parameter,value)
        if section == 'Mutation':
            return self.Mutation.setparameter(parameter,value)
        return False

    def setparameterlist(self,parameterlist):
        '''
        Set parameters accroding to the setting list
        '''
        length = np.size(parameterlist,axis=0)
        for i in range(length):
            [section,parameter,value] = parameterlist[i]
            if not self.setparameter(section,parameter,value):
                code = 'Error in setting {i} for section {section}: {parameter} -> {value}'.format(\
                    section=section,\
                    parameter=parameter,\
                    value=value)
                return False,code
        return True,None

class Creation:
    '''
    Set parameters for Creation Function
    '''
    def __init__(self):
        self.args = dict()

    def setparameter(self,parameter,value):
        return True

class Selection:
    '''
    Set parameters for Selection Function
    '''
    def __init__(self):
        self.args = dict()
        self.args['tournamentsize'] = 3

    def setparameter(self,parameter,value):
        if parameter == 'TournamentSize':
            self.args['tournamentsize'] = value
            return True
        return False

class FitnessScale:
    '''
    Set parameters for FitnessScale Function
    '''
    def __init__(self):
        self.args = dict()
        self.args['factor'] = 1.0
        self.args['rate'] = 2.0
        self.args['quality'] = 0.4
    
    def setparameter(self,parameter,value):
        if parameter == 'ProportionalFactor':
            self.args['factor'] = value
            return True
        if parameter == 'ShiftLinearRate':
            self.args['rate'] = value
            return True
        if parameter == 'TopQuality':
            self.args['quality'] = value
            return True
        return False
    
class Crossover:
    '''
    Set parameters for Crossover Function
    '''
    def __init__(self):
        self.args = dict()
        self.args['a'] = 0.0
        self.args['breal'] = 0.5
        self.args['bint'] = 0.75
        self.args['ratio'] = 1.0
        self.args['R'] = 1.2

    def setparameter(self,parameter,value):
        if parameter == 'LaplacianA':
            self.args['a'] = value
            return True
        if parameter == 'LaplacianBreal':
            self.args['breal'] = value
            return True
        if parameter == 'LaplacianBint':
            self.args['bint'] = value
            return True
        if parameter == 'IntermediateRatio':
            self.args['ratio'] = value
            return True
        if parameter == 'HeuristicR':
            self.args['R'] = value
            return True
        return False

class Mutation:
    '''
    Set parameters for Mutation Function
    '''
    def __init__(self):
        self.args = dict()
        self.args['preal'] = 0.1
        self.args['pint'] = 0.2
        self.args['shrink'] = 1.0
        self.args['scale'] = 1.0

    def setparameter(self,parameter,value):
        if parameter == 'UniformPreal':
            self.args['preal'] = value
            return True
        if parameter == 'UniformPint':
            self.args['pint'] = value
            return True
        if parameter == 'GaussianShrink':
            self.args['shrink'] = value
            return True
        if parameter == 'GaussianScale':
            self.args['scale'] = value
            return True
        return False
