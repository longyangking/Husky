import numpy as np

def IntegerStriction(chrome,LB,UB,IntCon):
    newchrome = chrome
    intchrome = np.floor(newchrome[IntCon])
    intchrome = intchrome + 1*(np.random.random(len(intchrome))>0.5)
    intchrome = intchrome - 1*(intchrome>UB[IntCon])
    intchrome = intchrome + 1*(intchrome<LB[IntCon])
    newchrome[IntCon] = intchrome
    return newchrome