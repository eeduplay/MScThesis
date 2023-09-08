'''
    Processes raw CW laser test data
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as sciopt
import os

CSV_OUT = False

REL_DATA_DIR = '../../rawdata/laser_tests/CW'
REL_PROC_DIR = '../../processed_data'
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), REL_DATA_DIR))
PROC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), REL_PROC_DIR))
SAMPLE_RATE = 6  # Hz

i = 0
csv_to_PD = lambda pathstr : pd.read_csv(pathstr, 
                                         header=None, 
                                         sep='\t', 
                                         usecols=[0], 
                                         names=[setpoint],
                                         skiprows=19)
with os.scandir(DATA_DIR) as it:
    for entry in it:
        if entry.name.endswith('.csv'):
            setpoint = entry.name.removesuffix('.csv')[entry.name.rfind('_')+1:]
            if i == 0:
                compiledData = csv_to_PD(entry.path)
                i += 1
            else: 
                newdf = csv_to_PD(entry.path)
                compiledData = pd.concat([compiledData, newdf], axis=1)

if CSV_OUT:
    compiledData.to_csv(PROC_DIR+'/CW_power.csv', index_label='Sample (6 Hz)')

plt.figure(figsize=(2.5,3))
for series in compiledData.columns:
    if compiledData[series].max() < 0.5:
        continue
    if series in ['27.0', '33.3']:
        plt.plot(compiledData.index/SAMPLE_RATE, 
             compiledData[series]/compiledData[series].max(), 
             label=series+' %')
plt.xlabel('Time [s]')
plt.ylabel('Relative power [-]')
plt.legend()
plt.tight_layout()
plt.savefig('report/assets/3 design/cw_power_time.pdf')

setpoints = compiledData.columns.to_numpy(dtype='float')
maximums = compiledData.max().to_numpy()
affineFunc = lambda x, a, b: a*x+b
popt, pcov = sciopt.curve_fit(affineFunc, setpoints[5:], maximums[5:])
xproj = np.linspace(25, 100, 20)
plt.figure(figsize=(3.3, 3))
plt.plot(xproj, affineFunc(xproj, popt[0], popt[1]), '--')
plt.plot(setpoints, maximums, '.', color='#00A6D6', markersize=2)
plt.plot(setpoints, maximums, 'o', mec='#00A6D6', mfc=(0,0,0,0))
plt.text(30, 100, '$P = {:.3f}{}{:+.3f}$'.format(popt[0], r'n_\mathrm{sp}', popt[1]),
         rotation=45)
plt.xlabel('Power Setpoint $n_\mathrm{sp}$ [%]')
plt.ylabel('Measured Maximum CW Power $P$ [W]')
plt.tight_layout()
plt.savefig('report/assets/3 design/cw_power_setpoint.pdf')
plt.show()