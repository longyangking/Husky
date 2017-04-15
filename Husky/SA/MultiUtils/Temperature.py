# Author: Yang Long <longyang_123@yeah.net>
#
# License: LGPL-2.1

import numpy as np

def TemperatureExp(temperature,k,args):
    '''
    Annealing in Exponent form (Default)
    '''
    return temperature*np.power(0.97,k)

def TemperatureFast(temperature,k,args):
    '''
    Annealing in Fast linear form
    '''
    return temperature/k

def TemperatureBoltz(temperature,k,args):
    '''
    Annealing in Boltzmann form
    '''
    return temperature/np.log(k)