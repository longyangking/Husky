import numpy as np

def Code(feature):
    '''
    Transform Features into Chrome Form
    '''
    return feature

def Decode(chrome,IntCon=None):
    '''
    Transform Chrome into Features Form
    '''
    chrome = np.array(chrome)
    if IntCon is not None:
        intchrome = np.floor(chrome[IntCon])
        intchrome = intchrome + 1*(np.random.random([1,len(intchrome)]))
        chrome[IntCon] = intchrome
    return chrome

def Rand(chromesize,chromerange=1,IntCon=None):
    '''
    Generate chrome randomly
    '''
    chrome = chromerange*np.random.random([1,chromesize])
    if IntCon is not None:
        intchrome = np.floor(chrome[IntCon])
        intchrome = intchrome + 1*(np.random.random([1,len(intchrome)]))
        chrome[IntCon] = intchrome
    return chrome 
