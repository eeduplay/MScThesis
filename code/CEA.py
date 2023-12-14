import pandas as pd
import numpy as np
from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt

pressures = []
temperatures = []
ArI_fraction = []
ArII_fraction = []

# with open('../rawdata/CEA_tv_Argon_P1-20b_T1000-20000K.txt', 'r') as f:
#     # i = 1
#     for line in f:
#         # if i > 240: break
#         # i += 1
#         if 'P, BAR' in line:
#             pressures.extend(map(float, line.split()[2:]))
#         elif 'T, K' in line:
#             temperatures.extend(map(float, line.split()[2:]))
#         elif '*Ar+' in line:  # Check for Ar+ first since 'Ar' in 'Ar+'
#             ArII_fraction.extend(map(float, line.split()[1:]))
#         elif '*Ar' in line:
#             ArI_fraction.extend(map(float, line.split()[1:]))

# # print(pressures)
# # print(temperatures)
# # print(ArI_fraction)
# # print(ArII_fraction)

# def get_ionization(p: int):
#     if p not in range(1,21):
#         raise ValueError('Invalid pressure (1-20 bars only)')
#     startindex = int((p-1)*20)
#     return (
#         np.array(temperatures[startindex:startindex+19]),
#         np.array(ArII_fraction[startindex:startindex+19])
#     )

DEFAULT_PATH = '../rawdata/CEA_tp_Argon_tab.txt'

class ThermoProps:
    def __init__(self, pressure: float, path=DEFAULT_PATH) -> None:
        data = pd.read_table(path, sep='\s+')
        self.datatable = data[data.p == pressure]
        self.p = pressure*1e5  # Pa
        self.T = self.datatable.t
        self.rho = CubicSpline(self.T, self.datatable.rho, extrapolate=True)
        self.cp = CubicSpline(self.T, 1000*self.datatable.cp, extrapolate=True)  # J kg^-1 K^-1
        self.gam = CubicSpline(self.T, self.datatable.gam, extrapolate=True)
        self.cv = CubicSpline(self.T,  # J kg^-1 K^-1
                              1000*self.datatable.cp/self.datatable.gam, extrapolate=True)
        self.h = CubicSpline(self.T, self.datatable.h*1000, extrapolate=True)  # J kg^-1
        
if __name__ == '__main__':
    argon_0p1 = ThermoProps(0.1, path='rawdata/CEA_tp_Argon_tab.txt')
    argon_1 = ThermoProps(1, path='rawdata/CEA_tp_Argon_tab.txt')
    argon_10 = ThermoProps(10, path='rawdata/CEA_tp_Argon_tab.txt')

    temps = np.linspace(200, 20000, 100)
    for gas in [argon_0p1, argon_1, argon_10]:
        plt.plot(temps, gas.cp(temps, extrapolate=True)/1000, 
                 label='{:.1f} bar'.format(gas.p*1e-5))
    # plt.plot(temps, argon_10.h(temps, extrapolate=True))
    plt.xlabel('$T$ [K]')
    plt.ylabel('$c_p$ [kJ kg$^{-1}$ K$^{-1}$]')
    # plt.ylabel('$h$ [J kg$^{-1}$]')
    plt.legend()

    fig1, ax1 = plt.subplots(figsize=(2.9,2.5))
    fig2, ax2 = plt.subplots(figsize=(2.9,2.5))

    ax1.plot(temps, argon_10.cp(temps)/1000)
    ax1.set_ylabel('$c_p$ [kJ kg$^{-1}$ K$^{-1}$]')
    ax1.set_xlabel('$T$ [K]')

    ax2.plot(temps, argon_10.h(temps)/1000000)
    ax2.set_ylabel('$h$ [MJ kg$^{-1}$]')
    ax2.set_xlabel('$T$ [K]')

    fig1.tight_layout()
    fig1.savefig('report/assets/4 models/Ar10_cp.pdf')
    fig2.tight_layout()
    fig2.savefig('report/assets/4 models/Ar10_h.pdf')

    plt.show()