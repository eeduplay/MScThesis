from datamanager import shotlist
from Laser import util
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit
import numpy as np

SAVE = True

pulse_buffer_width = 1  # ms, laser pulse duration BEFORE spark

# Create mask for valid absorption data
mask = (shotlist['Series Prefix'] == 'SPX') \
    * (shotlist['Output Energy [J]'] > 0)

shots = shotlist[mask]

mask20bar = shots['Pressure [bar]'] > 19.5

pulse_energy = util.sp2energy(shots['Laser Setpoint'], 
                              shots['Pulse width [ms]'])
buffer_fraction = (pulse_buffer_width/shots['Pulse width [ms]'])
buffer_energy = pulse_energy*buffer_fraction*util.entryFactor*util.exitFactor
energy_m_nobuffer = shotlist[mask]['Output Energy [J]']-buffer_energy

transmitted_energy = energy_m_nobuffer/util.exitFactor
input_energy = (1-buffer_fraction)*pulse_energy*util.entryFactor

absorption = 1-transmitted_energy/input_energy

pulse_energy.rename('Ep')
input_energy.rename('Ein')
transmitted_energy.rename('t')
absorption.rename('a')
alldata = shots.assign(Ep=pulse_energy, Ein=input_energy, t=transmitted_energy, a=absorption)
# if SAVE:
#     alldata.to_latex(
#         buf='report/assets/5 results/absorptionTable.tex',
#         index=True,
#         columns=['Pressure [bar]', 'Ep', 'Ein', 't', 'a'],
#         header=['$p$ [bar]', r'$E_\mathrm{pulse}$ [J]', r'$E_\mathrm{in}$ [J]', r'$E_\tau$ [J]', r'$a$ [-]'],
#         escape=False,
#         float_format='%.2f',
#         column_format=r'@{}lrrrrr@{}',
#         caption=(r'LSP energy absorption data. $p$ is the nominal pressure; $E_\mathrm{pulse}$, $E_\mathrm{in}$, $E_\tau$, and $E_a$ are the laser pulse energy, input energy, transmitted energy, and computed absorption of the LSP', 'LSP energy absorption data'),
#         label='tab:LSP_absorption',
#         position='h'
#     )

plt.figure(figsize=(2.9,3))
plt.plot(shots['Pressure [bar]'], absorption, 'o')
plt.xlabel('Pressure $p$ [bar]')
plt.ylabel('Absorption $a$ [-]')
plt.tight_layout()
if SAVE:
    plt.savefig('report/assets/5 results/absorption_ia.pdf')
    plt.savefig('report/assets/5 results/absorption_ia.png', dpi=72)

plt.figure(figsize=(2.9,3))
model = lambda Ein, a: a*Ein
Espan = np.array([10, 28])
popt, pcov = curve_fit(model, input_energy[mask20bar], 
                       input_energy[mask20bar]-transmitted_energy[mask20bar])
plt.plot(input_energy[mask20bar], 
         input_energy[mask20bar]-transmitted_energy[mask20bar], 'o')
plt.plot(Espan, model(Espan, popt[0]), '--')
plt.xlabel(r'Input energy $E_\mathrm{in}$ [J]')
plt.ylabel('Absorbed energy $E_a$ [J]')
plt.annotate(r'$E_a = aE_\mathrm{in}$', (0.49, 0.5), xycoords='axes fraction',
             ha='right')
plt.annotate(r'$a = $'+'{:.2f}'.format(popt[0]), (0.51, 0.45), 
             xycoords='axes fraction', color='C1')
plt.tight_layout()
if SAVE:
    plt.savefig('report/assets/5 results/absorption_20bar.pdf')
    plt.savefig('report/assets/5 results/absorption_20bar.png', dpi=72)
plt.show()