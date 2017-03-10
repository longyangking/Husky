# Author: Yang Long <longyang_123@yeah.net>
#
# License: LGPL-2.1

import numpy as np

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
        pass

    def setparameter(self,parameter,value):
        return True

class Selection:
    '''
    Set parameters for Selection Function
    '''
    def __init__(self):
        self.TournamentSize = 3

    def setparameter(self,parameter,value):
        if parameter == 'TournamentSize':
            self.TournamentSize = value
            return True
        return False

class FitnessScale:
    '''
    Set parameters for FitnessScale Function
    '''
    def __init__(self):
        self.ProportionalFactor = 1.0
        self.ShiftLinearRate = 2.0
        self.TopQuality = 0.4
    
    def setparameter(self,parameter,value):
        if parameter == 'ProportionalFactor':
            self.ProportionalFactor = value
            return True
        if parameter == 'ShiftLinearRate':
            self.ShiftLinearRate = value
            return True
        if parameter == 'TopQuality':
            self.TopQuality = value
            return True
        return False
    
class Crossover:
    '''
    Set parameters for Crossover Function
    '''
    def __init__(self):
        self.LaplacianA = 0.0
        self.LaplacianBreal = 0.5
        self.LaplacianBint = 0.75
        self.IntermediateRatio = 1.0
        self.HeuristicR = 1.2

    def setparameter(self,parameter,value):
        if parameter == 'LaplacianA':
            self.LaplacianA = value
            return True
        if parameter == 'LaplacianBreal':
            self.LaplacianBreal = value
            return True
        if parameter == 'LaplacianBint':
            self.LaplacianBint = value
            return True
        if parameter == 'IntermediateRatio':
            self.IntermediateRatio = value
            return True
        if parameter == 'HeuristicR':
            self.HeuristicR = value
            return True
        return False

class Mutation:
    '''
    Set parameters for Mutation Function
    '''
    def __init__(self):
        self.UniformPreal = 0.1
        self.UniformPint = 0.2
        self.GaussianShrink = 1.0
        self.GaussianScale = 1.0

    def setparameter(self,parameter,value):
        if parameter == 'UniformPreal':
            self.UniformPreal = value
            return True
        if parameter == 'UniformPint':
            self.UniformPint = value
            return True
        if parameter == 'GaussianShrink':
            self.GaussianShrink = value
            return True
        if parameter == 'GaussianScale':
            self.GaussianScale = value
            return True
        return False