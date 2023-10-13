import pressure_analysis as pa
import Laser.util as lu
from datamanager import shotlist
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

SAVE = False

PulseEnergy_shots = {
    20: [
        'LSP51_S1',
        'LSP52_S2',
        'LSP53_S3',
        'LSP54_S4',
        'LSP55_S5',
        'LSP56_S6',
        'LSP57_S7'
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

Pressure_shots = [
    'LSP1_PS1',
    'LSP16_PS16',
    'LSP60_S9'
]

# Effect of changing pulse energy on heat transfer efficiency
fig1, ax1 = plt.subplots(figsize=(5.8, 4))
for nom_pressure, shot_ids in PulseEnergy_shots.items():
    efficiencies = []
    energies = []
    yerr = []
    for shot in shot_ids:
        data = pa.analyze(shot)
        efficiencies.append(data['eta'])
        yerr.append(data['eta']*data['uncertainty'])
        energies.append(data['E_in'])
    ax1.errorbar(energies, efficiencies, yerr, fmt='o', ecolor=(0,0,0,0.5),
                 elinewidth=1.0, capsize=3, label=str(nom_pressure)+' bar')
ax1.legend()
ax1.set_xlabel(r'Pulse energy $E_\mathrm{in}$ [J]')
ax1.set_ylabel(r'Heat deposition efficiency $\eta$ [-]')

# Effect of changing pressure on heat transfer efficiency
fig2, ax2 = plt.subplots(figsize=(5.8, 4))
efficiencies = []
pressures = []
yerr = []
for shot in Pressure_shots:
    data = pa.analyze(shot)
    efficiencies.append(data['eta'])
    yerr.append(data['eta']*data['uncertainty'])
    pressures.append(shotlist.loc[shot]['Pressure [bar]'])
ax2.errorbar(pressures, efficiencies, yerr, fmt='o', ecolor=(0,0,0,0.5),
                elinewidth=1.0, capsize=3)
ax2.set_ylim(bottom=0)
# ax1.legend()
ax2.set_xlabel(r'Nominal pressure $p_0$ [bar]')
ax2.set_ylabel(r'Heat deposition efficiency $\eta$ [-]')


if SAVE:
    fig1.savefig('report/assets/5 results/heatEfficiency.pdf')
    fig2.savefig('report/assets/5 results/heatEfficiency.pdf')
plt.show()