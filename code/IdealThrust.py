import numpy as np

def getGAMMA(gamma):
    return np.sqrt(gamma)*(2/(gamma+1))**((gamma+1)/(2*(gamma-1)))

def cf_ideal(gamma, pback, pc):
    GAMMA = getGAMMA(gamma)
    pressureRatio = pback/pc
    return GAMMA*np.sqrt(
        2*gamma/(gamma-1)*(1-pressureRatio**((gamma-1)/gamma))
    )

def Aratio_ideal(gamma, pback, pc):
    GAMMA = getGAMMA(gamma)
    pressureRatio = pback/pc
    return GAMMA**2/(pressureRatio**(1/gamma)*cf_ideal(gamma, pback, pc))