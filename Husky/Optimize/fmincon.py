import numpy as np 

def fmincon(func,x0,A,b,Aeq,beq,LB,UB,nonlcon):
    '''
    Find minimum of constrained nonlinear multivariable function
    This algorithm is based on :
        1. Trust-Region-Reflective Optimization
        2. Active-Set Optimization
        3. Interior-Point Optimization
        4. SQP Optimization
    '''
    pass