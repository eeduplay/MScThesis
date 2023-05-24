import numpy as np
import matplotlib.pyplot as plt
import CoolProp.CoolProp as cp
from conversions import *
from PIL import Image
from enum import Enum

class Gas(Enum):
    Argon = {
        'p2Ph': 26*(1e5**2)*1000,  # Pa^2 W
        'Pr': 240  # W
    }
    Xenon = {
        'p2Ph': 7.7*(1e5**2)*1000,
        'Pr': 7  # W
    }


def threshold_power(pressure, gas):
    gasprops = gas.value
    return gasprops['p2Ph']*pressure**-2 + gasprops['Pr']

if __name__ == '__main__':
    ps = np.linspace(3e5, 20e5)

    zimakovData = np.loadtxt('rawdata/ZimakovExperimental.csv', delimiter=',')

    exp_success = np.loadtxt('rawdata/thresholdSearch_success.csv', 
        delimiter=',', skiprows=1)
    exp_failure = np.loadtxt('rawdata/thresholdSearch_failure.csv', 
        delimiter=',', skiprows=1)

    # zimakovData = np.asarray(Image.open('../rawdata/zimakov2.png'))

    # plt.imshow(zimakovData, 
    #     extent=(0, 16e5, 1e2, 1e4)
    #     )
    plt.semilogy(ps/1e5, threshold_power(ps, Gas.Argon), 
                 label='Empirical Formula')
    plt.semilogy(zimakovData[:,0], zimakovData[:,1], 'o', 
                 label='Zimakov (2019) Data')
    plt.semilogy(exp_success[:,0], exp_success[:,1], 
                 'o', label='Successful LSP', markerfacecolor='#fff0',
                 markeredgecolor='g')
    plt.semilogy(exp_failure[:,0], exp_failure[:,1], 'xg', label='Failed LSP')
    plt.xlabel('Pressure $p$ [bar]')
    plt.ylabel('Laser threshold power $P_t$ [W]')
    # plt.xlim((0, 16e5))
    # plt.ylim((1e2, 1e4))
    # plt.yscale('log')
    # ax = plt.gca()
    # ax.set_aspect(((1e4-1e2)/16e5)*622/426)
    convertAxis('x', (Pa2psi, psi2Pa), 'Pressure $p$ [psi]')
    plt.legend()
    plt.grid(which='both')
    plt.show()