'''
    Processes raw CW laser test data
'''

import pandas as pd
import matplotlib.pyplot as plt
import os

REL_DATA_DIR = '../../rawdata/laser_tests/CW'
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), REL_DATA_DIR))
SAMPLE_RATE = 6  # Hz

i = 0
with os.scandir(DATA_DIR) as it:
    for entry in it:
        if entry.name.endswith('.csv'):
            setpoint = entry.name.removesuffix('.csv')[entry.name.rfind('_')+1:]
            if i == 0:
                compiledData = pd.read_csv(entry.path, header=None, sep='\t', 
                                           usecols=[0], names=['Setpoint '+setpoint], 
                                           skiprows=19)
                i += 1
            else: 
                newdf = pd.read_csv(entry.path, header=None, sep='\t', usecols=[0], 
                                    names=['Setpoint '+setpoint], skiprows=19)
                compiledData = pd.concat([compiledData, newdf], axis=1)
print(compiledData)