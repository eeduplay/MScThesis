from Pressure.pcb import PressureData
from datamanager import shotlist
import matplotlib.pyplot as plt
import numpy as np
from Laser import util

SAVE = False

# Comparison of raw vs filtered signal
fig0, ax0 = plt.subplots(figsize=(5.8, 4))
pressure = PressureData()
power = pressure.load_from_wavedata('LSP1_PS1')
pressure.filter_data()
window_right_edge = int(0.4*power.shape[0])
power -= np.mean(power[:window_right_edge, 1])
ax0.plot(pressure.time[:-50]*1000, pressure.pressure_raw[:-50], color='#00A6D6', 
         alpha=0.33, label='Noisy Signal')
ax0.plot(pressure.time[:-50]*1000, pressure.pressure[:-50], color='#00A6D6',
         label='Filtered Signal')
y1, y2 = ax0.get_ylim()
ax0.fill_between(pressure.time*1000, 10, -10, 
                 where=power[:,1] > 0.25,
                 edgecolor='#ED1B2F',
                 facecolor=(0,0,0,0),
                #  alpha=0.33, 
                 hatch=r'\\\ '[:-1],
                 label='Laser On')
ax0.set_ylim(y1, y2)
ax0.legend()
ax0.set_xlabel('Time $t$ [ms]')
ax0.set_ylabel(r'Pressure change $\Delta p$ [kPa]')
if SAVE: plt.savefig('report/assets/5 results/pressure_noise.pdf')

# Comparison of pressure profiles at different starting pressures
identifiers = [
    'LSP51_S1',
    'LSP16_PS16',
    'LSP60_S9'
]

linestyles = [':', '--', '-']

fig1, ax1 = plt.subplots(figsize=(5.8, 4))
for shot in identifiers:
    nominal_pressure = shotlist.loc[shot]['Pressure [bar]']
    pressure = PressureData()
    pressure.load_from_wavedata(shot)
    pressure.filter_data()
    ax1.plot(pressure.time[1750:-250]*1000, pressure.pressure[1750:-250], linestyles.pop(),
                label='{} bar'.format(nominal_pressure))
ax1.legend()
ax1.set_xlabel('Time $t$ [ms]')
ax1.set_ylabel(r'Pressure change $\Delta p$ [kPa]')
if SAVE: plt.savefig('report/assets/5 results/pressure_pressures.pdf')

# Comparison of pressure profiles at different laser powers
indices_20b = [*range(51, 56), 57]
identifiers_20b = ['LSP{}_S{}'.format(i, i-50) for i in indices_20b]
identifiers_10b = ['LSP60_S9', 'LSP61_S10', 'LSP62_S11', 'LSP64_S13', 
                   'LSP66_S15', 'LSP72_X12']

fig2, axes2 = plt.subplots(1, 2, sharey=True, figsize=(5.8, 4))
for i, idset in enumerate([identifiers_20b, identifiers_10b]):
    for shot in idset:
        energy = util.energy_from_shot_data(shotlist.loc[shot])
        energy *= util.entryFactor
        pressure = PressureData()
        pressure.load_from_wavedata(shot, trimstart=True)
        pressure.filter_data()
        axes2[i].plot(pressure.time[:750]*1000, pressure.pressure[:750], 
                      label='{:.1f} J'.format(energy))
    axes2[i].set_xlabel('Time $t$ [ms]')
    axes2[i].legend()
    axes2[i].text(pressure.time.min()*1000, 8, 
                  'Nominal pressure: {} bar'.format(20-i*10), va='top', 
                  fontfamily='monospace', fontsize='x-small')
    
axes2[0].set_ylabel(r'Pressure change $\Delta p$ [kPa]')
if SAVE: plt.savefig('report/assets/5 results/pressure_powers.pdf')

plt.show()