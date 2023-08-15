import numpy as np
import matplotlib.pyplot as plt
import CoolProp.CoolProp as cp
from conversions import *
from PIL import Image
from enum import Enum
from cycler import cycler
import pandas as pd

# custom_cycler = cycler(color=['#ED1B2F', 'c', '#EC6842'])
# plt.rc('axes', prop_cycle=custom_cycler)

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
    matsuiData = np.loadtxt('rawdata/matsui_lu_pP.csv', delimiter=',', skiprows=2, usecols=[0,1])
    luData = np.loadtxt('rawdata/matsui_lu_pP.csv', delimiter=',', skiprows=2, usecols=[2,3], max_rows=6)

    # Early LSP experiments
    exp_success = np.loadtxt('rawdata/thresholdSearch_success.csv', 
        delimiter=',', skiprows=1)
    success_front = []
    unique_pressures = np.unique(exp_success[:,0])
    for i in unique_pressures:
        relevant_pressures = exp_success[:,0] == i
        success_front.append(np.min(exp_success[relevant_pressures,1]))
    exp_failure = np.loadtxt('rawdata/thresholdSearch_failure.csv', 
        delimiter=',', skiprows=1)
    
    # Solid target ignition experiments
    STI_shots = pd.read_excel('rawdata/shotlist_Aug9.xlsx', 'Shotlist V2', 
                              index_col=0, usecols='A:N', true_values=['TRUE'], 
                              false_values=['FALSE'],
                              dtype={'Stable': np.bool_}, nrows=49)
    STI_successes = STI_shots[(STI_shots['Series Prefix'] == 'PS') & (STI_shots['Stable'] == True)]
    STI_successes.sort_values('Pressure [bar]', inplace=True)
    lowest_power = 1.1
    front_mask = []
    for row in STI_successes.itertuples():
        if front_mask == [] or row[5] <= lowest_power:
            front_mask.append(True)
            lowest_power = row[5]
        else:
            front_mask.append(False)

    # zimakovData = np.asarray(Image.open('../rawdata/zimakov2.png'))

    # plt.imshow(zimakovData, 
    #     extent=(0, 16e5, 1e2, 1e4)
    #     )
    plt.figure(figsize=(6,5))
    plt.semilogy(ps/1e5, threshold_power(ps, Gas.Argon), '--k',
                 label='Zimakov et al. Model', linewidth=1)
    plt.semilogy(zimakovData[:,0], zimakovData[:,1], 'Dk', 
                 label='Zimakov et al. (2016) Data')
    plt.semilogy(matsuiData[:,0], matsuiData[:,1], '^k', 
                 label='Matsui et al. (2019) Data')
    plt.semilogy(luData[:,0], luData[:,1], 'sk', 
                 label='Lu et al. (2022) Data')
    plt.semilogy(unique_pressures, success_front, 
                 'o', label='Arc Ignition')
    plt.semilogy(STI_successes[front_mask]['Pressure [bar]'], 
                 STI_successes[front_mask]['Laser Setpoint']*3000, 
                 '-o', label='Wire Ignition', linewidth=1)
    # plt.semilogy(exp_success[:,0], exp_success[:,1], 
    #              'o', label='Successful LSP', markerfacecolor='#fff0',
    #              markeredgecolor='g')
    # plt.semilogy(exp_failure[:,0], exp_failure[:,1], 'x', label='Failed LSP')
    plt.xlabel('Pressure $p$ [bar]')
    plt.ylabel('Laser threshold power $P_t$ [W]')
    # plt.xlim((0, 16e5))
    # plt.ylim((1e2, 1e4))
    # plt.yscale('log')
    # ax = plt.gca()
    # ax.set_aspect(((1e4-1e2)/16e5)*622/426)
    convertAxis('x', (bar2psi, psi2bar), 'Pressure $p$ [psi]')
    plt.legend()
    plt.grid(which='both')
    plt.show()