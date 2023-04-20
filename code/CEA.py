import pandas as pd
import numpy as np

pressures = []
temperatures = []
ArI_fraction = []
ArII_fraction = []

with open('../rawdata/CEA_tv_Argon_P1-20b_T1000-20000K.txt', 'r') as f:
    # i = 1
    for line in f:
        # if i > 240: break
        # i += 1
        if 'P, BAR' in line:
            pressures.extend(map(float, line.split()[2:]))
        elif 'T, K' in line:
            temperatures.extend(map(float, line.split()[2:]))
        elif '*Ar+' in line:  # Check for Ar+ first since 'Ar' in 'Ar+'
            ArII_fraction.extend(map(float, line.split()[1:]))
        elif '*Ar' in line:
            ArI_fraction.extend(map(float, line.split()[1:]))

# print(pressures)
# print(temperatures)
# print(ArI_fraction)
# print(ArII_fraction)

def get_ionization(p: int):
    if p not in range(1,21):
        raise ValueError('Invalid pressure (1-20 bars only)')
    startindex = int((p-1)*20)
    return (
        np.array(temperatures[startindex:startindex+19]),
        np.array(ArII_fraction[startindex:startindex+19])
    )