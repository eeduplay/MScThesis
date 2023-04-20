'''
    Plots Argon electron density vs temperature at different pressures
'''

import numpy as np 
import matplotlib.pyplot as plt
import saha
import scipy.constants as const

Ei_argon = 15.759610  # eV
R_argon = 208.1  # J kg^-1 K^-1
M_argon = 39.95  # kg kmol^-1
init_temp = 300  # K
temperature = np.linspace(1000, 30000, 100)  # K

pressure_bar = np.array([1, 10, 14, 20])
pressure = pressure_bar*1e5  # Pa

pfr = saha.get_argon_pfr(temperature)


for p in pressure:
    rho = p/(R_argon*init_temp)
    n_0 = (1000*const.Avogadro*rho/M_argon)
    n_e = saha.degreeIonization(temperature, Ei_argon, n_0, pfr)  # m^-3
    plt.semilogy(temperature, n_e/100**3, label='{} bar'.format(p/1e5))

plt.xlabel('Temperature $T$/K')
plt.ylabel(r'Electron density $n_\mathrm{e}$/cm$^{-3}$')
plt.ylim(bottom=1e15)
plt.legend()
plt.show()