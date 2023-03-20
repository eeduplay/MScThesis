import numpy as np
import matplotlib.pyplot as plt
import CoolProp.CoolProp as cp
from conversions import *
from PIL import Image

argon = {
    'p2Ph': 26*(1e5**2)*1000,  # Pa^2 W
    'Pr': 240  # W
}

xenon = {
    'p2Ph': 7.7*(1e5**2)*1000,
    'Pr': 7  # W
}

def threshold_power(pressure, gas):
    return gas['p2Ph']*pressure**-2 + gas['Pr']

if __name__ == '__main__':
    ps = np.linspace(3e5, 20e5)

    zimakovData = np.loadtxt('rawdata/ZimakovExperimental.csv', delimiter=',')

    # zimakovData = np.asarray(Image.open('../rawdata/zimakov2.png'))

    # plt.imshow(zimakovData, 
    #     extent=(0, 16e5, 1e2, 1e4)
    #     )
    plt.semilogy(ps, threshold_power(ps, argon), label='Empirical Formula')
    plt.semilogy(zimakovData[:,0]*1e5, zimakovData[:,1], 'o', label='Experimental Data')
    plt.xlabel('Pressure $p$ [Pa]')
    plt.ylabel('Laser threshold power $P_t$ [W]')
    # plt.xlim((0, 16e5))
    # plt.ylim((1e2, 1e4))
    # plt.yscale('log')
    # ax = plt.gca()
    # ax.set_aspect(((1e4-1e2)/16e5)*622/426)
    convertAxis('x', (Pa2psi, psi2Pa), 'Pressure $p$ [psi]')
    plt.legend()
    plt.show()