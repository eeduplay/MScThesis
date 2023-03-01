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
        Computes the degree of ionization.
            temperature:    temperature, K
            pressure:       pressure, Pa
            ion_E:          ionization energy, eV
    '''
    alpharatio = 3.2e-2 * (temperature**(5/2)/pressure) \
        * np.exp(-c.e*ion_E/(kb*temperature))
    return np.sqrt(alpharatio/(1+alpharatio))
