import numpy as np
import scipy.constants as c
from constants import PLANCK_h as h
from constants import BOLTZMANN_kb as kb
from constants import MASS_ELECTRON as me

def deBroglieThermal(temperature):
    GAMMA = np.sqrt(h**2/(2*np.pi*me*kb*temperature))
    return GAMMA

# Simplified Saha approach
def degreeIonization_simple(temperature, pressure, ion_E):
    '''
        Computes the degree of ionization using the CHEE 543 assumptions
            temperature:    temperature, K
            pressure:       pressure, Pa
            ion_E:          ionization energy, eV
        Returns alpha_i, the ratio of ions to (ions+neutrals)
    '''
    alpharatio = 3.2e-2 * (temperature**(5/2)/pressure) \
        * np.exp(-c.eV*ion_E/(kb*temperature))
    return np.sqrt(alpharatio/(1+alpharatio))

def degreeIonization(temperature, ion_E, n_0, pfr=1):
    '''
        Computes the degree of ionization according to Akarapu et al.
            temperature:    temperature, K
            ion_E:          ionization energy, eV
            pfr:            partition function ratio, 1 for low (few 1000 K's)
                            temperatures
        Returns n_e, the electron density
    '''
    l = deBroglieThermal(temperature)
    ratio = (2/l**3)*pfr*np.exp(-c.eV*ion_E/(kb*temperature))
    return (-ratio+np.sqrt(ratio**2+4*ratio*n_0))/2

def curvefit(T, c1, c2, n_0):
    ratio = c1*T**1.5*np.exp(c2*T**-1)
    return (-ratio+np.sqrt(ratio**2+4*ratio*n_0))/2