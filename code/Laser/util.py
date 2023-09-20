'''
    Laser power/energy processing utilities
'''

from dotenv import load_dotenv
load_dotenv()
import numpy as np
import pandas as pd
import warnings
import os

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

if __name__ == '__main__':
    generate_database()