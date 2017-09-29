# Author: Yang Long <longyang_123@yeah.net>
#
# License: LGPL-2.1

import numpy as np 

def fminsearch(fun,x0,numofpoints=None,
    alpha=1.0,gamma=2.0,rho=0.5,sigma=0.5,
    alpha0=1.0,
    stalliteration=50,tolfun=1e-6):
    '''
    Find minimum of unconstrained multivariable function using derivative-free method
    This algorithm is based on Nelder-Mead simplex direct search
    '''
    (N,) = x0.shape
    if numofpoints is None:
        numofpoints = 3*N 
    xs = np.zeros((numofpoints,N))
    values = np.zeros(numofpoints)

    # Initiate points
    for i in range(numofpoints):
        xs[i,:] = x0 + alpha0*x0*np.random.random(N)

    for i in range(numofpoints):
        values[i] = fun(xs[i,:])
        
    valuer = np.max(values)
    count = 0
    bestvalue = None
    bestx = None

    while 1:
        # Order
        orders = np.argsort(values)
        if bestvalue is None:
            bestvalue = values[orders[0]]
            bestx = xs[orders[0]]
        else:
            if np.abs((bestvalue-values[orders[0]])) <= tolfun*bestvalue:
                count += 1
            bestvalue = values[orders[0]]
            bestx = xs[orders[0]]

            if count >= stalliteration:
                break

        xo = np.mean(xs,0)

        # Reflection
        xr = xo + alpha*(xo - xs[orders[-1]])
        valuer = fun(xr)

        maxvalue = values[orders[-1]]
        minvalue = values[orders[0]]

        if (valuer < maxvalue) and (valuer >= minvalue):
            xs[orders[-1]] = xr
            values[orders[-1]] = valuer
            continue

        # Expansion
        if (valuer < np.min(values)):
            xe = xo + gamma*(xr - xo)
            valuee = fun(xe)
            if valuee < valuer:
                xs[orders[-1]] = xe
                values[orders[-1]] = valuee
            else:
                xs[orders[-1]] = xr
                values[orders[-1]] = valuer
            continue

        # Contraction
        if (valuer >= maxvalue):
            xc = xo + rho*(xs[orders[-1]] - xo)
            valuec = fun(xc)
            if valuec < maxvalue:
                xs[orders[-1]] = xc
                values[orders[-1]] = valuec
                continue

        # Shrink
        xbest = xs[orders[0]]
        for i in range(numofpoints):
            xs[i] = xbest + sigma*(xs[i] - xbest)
            values[i] = fun(xs[i])

    return [bestx,bestvalue]

        