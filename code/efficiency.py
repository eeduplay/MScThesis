import pressure_analysis as pa
import Laser.util as lu
from datamanager import shotlist
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from scipy.optimize import curve_fit

SAVE = True

PulseEnergy_shots = {
    20: [
        'LSP51_S1',
        'LSP52_S2',
        'LSP53_S3',
        'LSP54_S4',
        'LSP55_S5',
        'LSP56_S6',
        # 'LSP57_S7'
        ],
    10: [
        'LSP60_S9',
        'LSP61_S10',
        'LSP62_S11',
        'LSP63_S12',
        'LSP64_S13',
        'LSP66_S15'
        ]
}

Pressure_shots_100 = [
    'LSP1_PS1',
    'LSP91_PP1',
    'LSP92_PP2',
    'LSP16_PS16',
    'LSP60_S9',
    'LSP93_PP3',
    'LSP94_PP4'
]
Pressure_shots_33 = [
    'LSP95_PP5',
    'LSP96_PP6',
    'LSP97_PP7',
    'LSP98_PP8',
    'LSP99_PP9',
    'LSP100_PP10'
]

# Effect of changing pulse energy on heat transfer efficiency
fig, axes = plt.subplots(1, 2, figsize=(5.8,4))
ax1, ax2 = axes
# fig1, ax1 = plt.subplots(figsize=(5.8, 4))
model = lambda E, a: a*E
computed_avg_eta = []
for nom_pressure, shot_ids in PulseEnergy_shots.items():
    cn = 'C'+str(int(nom_pressure/10 - 1))
    efficiencies = []
    energies = []
    heats = []
    yerr = []
    for shot in shot_ids:
        data = pa.analyze(shot)
        efficiencies.append(data['eta'])
        heats.append(data['Q_in'])
        yerr.append(data['Q_in']*data['uncertainty'])
        energies.append(data['E_in'])
    # ax1.errorbar(energies, efficiencies, yerr, fmt='o', ecolor=(0,0,0,0.5),
    #              elinewidth=1.0, capsize=3, label=str(nom_pressure)+' bar')
    popt, pcov = curve_fit(model, energies, heats)
    print('Average efficiency {} bar: {:.2f} %'.format(nom_pressure, popt[0]*100))
    energies_model = np.array([energies[0], energies[-1]])
    ax1.errorbar(energies, heats, yerr, fmt=cn+'o', ecolor=(0,0,0,0.5), 
                 elinewidth=1.0, capsize=3, label=str(nom_pressure)+' bar')
    ax1.plot(energies_model, model(energies_model, popt[0]), cn+':', 
             label=str(nom_pressure)+' bar, fit')
    computed_avg_eta.append(popt[0])

ax1.annotate(r'$Q_\mathrm{in} = \eta E_\mathrm{in}$', (0.4, 0.4),
             xycoords='axes fraction', ha='right')
ax1.annotate(r'$\eta = $'+'{:.3f}'.format(computed_avg_eta[0]), (0.45, 0.32),
             xycoords='axes fraction', color='C0')
ax1.annotate(r'$\eta = $'+'{:.3f}'.format(computed_avg_eta[1]), (0.45, 0.27),
             xycoords='axes fraction', color='C1')
# ax1.set_ylim(0, 0.3)
ax1.legend()
ax1.set_xlabel(r'Pulse energy $E_\mathrm{in}$ [J]')
# ax1.set_ylabel(r'Heat deposition efficiency $\eta$ [-]')
ax1.set_ylabel(r'Heat deposition $Q_\mathrm{in}$ [J]')

# Effect of changing pressure on heat transfer efficiency
# fig2, ax2 = plt.subplots(figsize=(5.8, 4))
for pshotseries in [Pressure_shots_100, Pressure_shots_33]:
    efficiencies = []
    pressures = []
    yerr = []
    for shot in pshotseries:
        data = pa.analyze(shot)
        efficiencies.append(data['eta'])
        yerr.append(data['eta']*data['uncertainty'])
        pressures.append(shotlist.loc[shot]['Pressure [bar]'])
    ax2.errorbar(pressures, np.array(efficiencies)*100, np.array(yerr)*100, 
                 fmt='o', ecolor=(0,0,0,0.5), elinewidth=1.0, capsize=3)
ax2.set_ylim(0, 20)
ax2.legend(['30.6 J pulse', '16.4 J pulse'])
# ax1.legend()
ax2.set_xlabel(r'Nominal pressure $p_0$ [bar]')
ax2.set_ylabel(r'Heat deposition efficiency $\eta$ [%]')
fig.tight_layout()

if SAVE:
    # fig1.savefig('report/assets/5 results/heatEfficiency.pdf')
    # fig2.savefig('report/assets/5 results/heatEfficiency.pdf')
    fig.savefig('report/assets/5 results/heatEfficiency.pdf')
    fig.savefig('report/assets/5 results/heatEfficiency.png', dpi=72)
plt.show()