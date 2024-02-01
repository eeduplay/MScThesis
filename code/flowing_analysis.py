import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from datamanager import shotlist
from Laser import util as lu
from Pressure.pcb import PressureData
import pressure_analysis as pa
from Spectra.spectrum import Spectrum, get_filepath_from_ID
from IdealThrust import mass_flow_constant

from dotenv import load_dotenv
load_dotenv()
from os import getenv
plt.style.use(['dark_background', 'code/presentationPlots.mplstyle'])
FIGTARGET = getenv('PPTASSETPATH')

SAVE = True
chamber_diameter = 1.5*25.4  # mm
Rg = 208.1  # J kg^-1 K^-1, Argon gas constant
gamma = 1.667
Km = mass_flow_constant(gamma, Rg)  # "K_m" choked mass flow constant for Argon
T_0 = 293.15  # K, assumed flow temperature
c_0 = np.sqrt(gamma*Rg*T_0)
TstarT0 = 2/(gamma + 1)
v_nozzle = c_0*np.sqrt(TstarT0)  # for choked orifice nozzle, v_exit = c*

def compute_velocity(shot: pd.DataFrame):
    throat_diameter = shot['Nozzle Diameter [mm]']
    if not throat_diameter: throat_diameter = 0
    v_chamber = Km*Rg*np.sqrt(T_0)*(throat_diameter/chamber_diameter)**2
    return v_chamber

pressure_shots = [
    'LSP88_F10',
    'LSP85_F7',
    'LSP87_F9',
    'LSP60_S9',
    ]

spectra_shots = [
    # 'LSP60_S9',
    'LSP88_F10',
    'LSP85_F7',
    'LSP87_F9',
]

fig0, ax0 = plt.subplots(figsize=(4.5,3.5))
fig1, ax1 = plt.subplots(figsize=(2.9,3))
vees = []
etas = []
u_eta = []
etas_cp = []
u_eta_cp = []
for s in pressure_shots:
    shot = shotlist.loc[s]
    v_i = compute_velocity(shot)
    vees.append(v_i)
    pressure = PressureData()
    data = pa.analyze(s)
    etas.append(data['eta'])
    u_eta.append(data['uncertainty']*data['eta'])
    # data = pa.analyze(s, use_cp=True)
    # etas_cp.append(data['eta'])
    # u_eta_cp.append(data['uncertainty']*data['eta'])
    pressure.load_from_wavedata(s)
    pressure.filter_data()
    fmt = 'w--' if s == 'LSP60_S9' else '-'
    ax0.plot(pressure.time[:-250]*1000, pressure.pressure[:-250], fmt, 
             label='{:.2f} m/s'.format(v_i))

ax0.set_xlim(150,350)
ax0.set_xlabel('Time $t$ [ms]')
ax0.set_ylabel(r'Pressure change $\Delta p$ [kPa]')
ax0.legend(loc='lower right')
fig0.tight_layout()

ax1.errorbar(vees, etas, yerr=u_eta, fmt='o', ecolor=(0,0,0,0.5), 
             elinewidth=1.0, capsize=3, label='$c_V$')
# ax1.errorbar(vees, etas_cp, yerr=u_eta_cp, fmt='o', ecolor=(0,0,0,0.5), 
#              elinewidth=1.0, capsize=3, label='$c_p$')
ax1.set_xlabel(r'Bulk flow velocity $v$ [m s$^{-1}$]')
ax1.set_ylabel(r'Heat deposition efficiency $\eta$ [-]')
ax1.set_ylim(0)
fig1.tight_layout()

if SAVE:
    fig0.savefig(FIGTARGET+'flow_deltap.svg')
    # fig0.savefig('report/assets/5 results/flow_deltap.png', dpi=72)
    # fig1.savefig('report/assets/5 results/flow_eta.pdf')
    # fig1.savefig('report/assets/5 results/flow_eta.png', dpi=72)

fig2, ax2 = plt.subplots()
for s in spectra_shots:
    shot = shotlist.loc[s]
    v_i = compute_velocity(shot)
    spectrumPath = get_filepath_from_ID(s)
    spectrum = Spectrum(spectrumPath, trimL=48, trimR=600)
    spectrum.calibrate_irradiance(2800,
                        'rawdata/spectra/calibration/Halogen_Light.txt',
                        'rawdata/spectra/calibration/Halogen_Dark.txt')
    scaleFactor = 100/spectrum.counts.max()
    scaleFactor = 1
    ax2.plot(spectrum.wavelengths, spectrum.counts*scaleFactor, linewidth=0.5, 
             label='{:.2f} m/s'.format(v_i))

ax2.set_xlabel(r'Wavelength $\lambda$ [nm]')
ax2.set_ylabel(r'Intensity $I$ [arb. units]')
ax2.set_xlim(690,860)
ax2.legend()

plt.show()