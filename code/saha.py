# from dotenv import load_dotenv  # Necessary to import CHIANTI
# load_dotenv()
# import ChiantiPy.core as ch
import numpy as np
import scipy.constants as c
from constants import PLANCK_h as h
from constants import BOLTZMANN_kb as kb
from constants import MASS_ELECTRON as me

def deBroglieThermal(temperature):
    LAMBDA = np.sqrt(h**2/(2*np.pi*me*kb*temperature))
    return LAMBDA

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

# def degreeIonization_chianti(temperature, n_0, element):
#     '''
#         Computes the degree of ionization using the CHIANTI database. Assumes 
#         single-ionization
#         ### Parameters
#         temperature: array_like
#             The range of temperatures over which to calculate the ionization
#         n_0: float
#             Initial number density of ground state atoms
#         element: int or string
#             Element for which to compute the ionization. `int` is interpreted as the 
#             atomic number, `string` is interpreted as the element symbol, e.g. 'Ar' for
#             Argon
#     '''
#     ion = ch.ioneq(element)
#     ion.load()
#     ion.calculate(temperature)
#     return ion.Ioneq[1,:]*n_0

def curvefit(T, c1, c2, n_0):
    ratio = c1*T**1.5*np.exp(c2*T**-1)
    return (-ratio+np.sqrt(ratio**2+4*ratio*n_0))/2

def get_argon_pfr(temperature):
    pfr_coeffs = [  -2.3077e-29,  # for T^7
                 2.3474e-24,   # for T^6
                -8.8453e-20,  # and so on...
                 1.4851e-15,
                -9.8430e-12,
                -1.2477e-08,
                 0.00047534,
                 3.79710000]
    pfr_coeffs.reverse()
    pfr = np.polynomial.polynomial.polyval(temperature, pfr_coeffs)
    return pfr