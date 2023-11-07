'''
    Laser power/energy processing utilities
'''

from dotenv import load_dotenv
load_dotenv()
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import warnings
import os
import sys

DATAPATH = os.getenv('DATAPATH')

entryFactor = 0.99414
exitFactor = 0.95008
maxpower_RP = 3080.0  # W
maxpower_CW = 349.33  # W
maxenergy_RP = 30.8  # J

def sp2power_cw(sp):
    '''
        Returns CW power in W given a decimal setpoint value
    '''
    if sp < 0.3: warnings.warn('Setpoint ({:.2f} %) below linear range, resulting CW power is unlikely to be correct'
                               .format(sp*100))
    return 495.1*sp - 145.77

def sp2power_rp(sp):
    return sp*maxpower_RP

def power2sp_rp(P):
    return P/maxpower_RP

def sp2energy(sp, pw):
    '''
        Returns pulse energy based on decimal setpoint value and pulse width in
        ms, assuming constant power.
    '''
    return sp*maxenergy_RP*pw/10.0

def generate_database():
    # When running script directly, builds the pulse profile database based on 
    # the pulse shapes found in the data directory
    pulseshapefilepath = DATAPATH+'Pulse Shapes/'

    # Initialize DataFrame dict
    df_dict = {
        'ID': [],
        'Filename': [],
        'High SP': [],
        'Low SP': [],
        'Duration [ms]': [],
        'High duration [ms]': [],
        'Low duration [ms]': [],
        'Energy [J]': []
    }

    # Go through each file to build the DataFrame
    for f in os.listdir(pulseshapefilepath):
        if not f.endswith('.shp'):
            continue
        pulseData = pd.read_xml(pulseshapefilepath+f, parser='etree', 
                                xpath='./Points/*')
        hsp = pulseData['Power'][0]/100
        lsp = pulseData['Power'][2]/100
        pw = pulseData['Time'][3]
        th = pulseData['Time'][1]
        tl = pw-th
        E = sp2energy(hsp, th)+sp2energy(lsp, tl)
        df_dict['ID'].append(f[:-4])
        df_dict['Filename'].append(f)
        df_dict['High SP'].append(hsp)
        df_dict['Low SP'].append(lsp)
        df_dict['Duration [ms]'].append(pw)
        df_dict['High duration [ms]'].append(th)
        df_dict['Low duration [ms]'].append(tl)
        df_dict['Energy [J]'].append(E)

    # Export DataFrame in some useful format
    pulse_database = pd.DataFrame(df_dict, df_dict['ID'])
    pulse_database.to_pickle(pulseshapefilepath+'pulseDB.pkl')
    pulse_database.to_csv(pulseshapefilepath+'pulseDB.csv')
    return pulse_database

if os.path.isfile(DATAPATH+'Pulse Shapes/pulseDB.pkl'):
    pulseDB = pd.read_pickle(DATAPATH+'Pulse Shapes/pulseDB.pkl')
else:
    print('No pulse database found. Generating now...')
    pulseDB = generate_database()

def energy_from_shot_data(shot_data: pd.DataFrame):
    pulse_type = shot_data['Pulse Spec']
    if pulse_type == 'Constant':
        return sp2energy(shot_data['Laser Setpoint'], 
                         shot_data['Pulse width [ms]'])
    else:
        return pulseDB.loc[pulse_type]['Energy [J]']
    
def plot_pulseshape(pulseID):
    pulse = pulseDB.loc[pulseID]
    setpoint = np.array([0]+[pulse['High SP']]*2+[pulse['Low SP']]*2+[0])
    timing = np.array([0, 0] + [pulse['High duration [ms]']]*2 
                      + [pulse['Duration [ms]']]*2)
    fig, ax = plt.subplots(figsize=(5.8,3))
    ax.plot(timing, setpoint*100)
    ax.set_xlabel('Time $t$ [ms]')
    ax.set_ylabel(r'Setpoint $n_\mathrm{sp}$ [%]')
    ax.text(timing.max(), setpoint.max()*100, pulseID, fontfamily='monospace', 
            fontsize='x-small', ha='right', va='top')
    ax.grid(which='both')
    secax = ax.secondary_yaxis('right', functions=(
        lambda s: sp2power_rp(s/100)/1000, lambda p: power2sp_rp(p*1000)*100))
    secax.set_ylabel(r'Power $P$ [kW]')
    plt.tight_layout()
    plt.show()

def db_to_latex(**kwargs):
    buf='report/assets/appendices/pulseDB.tex'
    out = pulseDB.to_latex(
            index=False,
            columns=['ID', 'High SP', 'Low SP', 'Duration [ms]', 'High duration [ms]', 'Low duration [ms]', 'Energy [J]'],
            header=['ID', r'High $n_\mathrm{sp}$ [-]', r'Low $n_\mathrm{sp}$ [-]', '$t$ [ms]', r'$t_\mathrm{high}$ [ms]', r'$t_\mathrm{low}$ [ms]', '$E$ [J]'],
            float_format='%.3f',
            formatters={'ID': '\\verb|{}|'.format},
            column_format=r'@{}lrrrrrr@{}',
            escape=False,
            caption=(r'Programmed pulse specifications. $n_\mathrm{sp}$ is the laser setpoint; $t$, $t_\mathrm{high}$, and $t_\mathrm{low}$ are the total pulse, high setpoint, and low setpoint durations, respectively; and $E$ is the pulse energy.', 'Programmed pulse specifications'),
            label='tab:app_pulseShapes',
            position='h',
            **kwargs
        )
    if out: print(out)

if __name__ == '__main__':
    if len(sys.argv) == 3 and sys.argv[1] == 'pulse':
        plot_pulseshape(sys.argv[2])
    elif len(sys.argv) > 1 and sys.argv[1] == 'latex':
        db_to_latex(buf=sys.argv[2] if len(sys.argv) == 3 else None)
    else:
        generate_database()