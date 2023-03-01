import numpy as np
from constants import PLANCK_h as h
from constants import BOLTZMANN_kb as kb
from constants import MASS_ELECTRON as me

def deBroglieThermal(temperature):
    GAMMA = np.sqrt(h**2/(2*np.pi*me*kb*temperature))
    return GAMMA
