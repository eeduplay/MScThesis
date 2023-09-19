'''
    Utility functions for PCB Piezotronics pressure transducer data
'''
from dotenv import load_dotenv
load_dotenv()
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import lfilter
from enum import Enum
from datamanager import shotlist

DATAPATH = os.getenv('DATAPATH')
loadtxtparams = {'skiprows': 3, 'delimiter': ','}

def get_channel_files(directory):
    filenumbers = []
    for f in os.listdir(directory):
        if f.startswith('WaveData') & f.endswith('.csv'):
            filenumbers.append(int(f[8:-4]))
    filenumbers.sort()
    return filenumbers

class Sensor(Enum):
    '''
        Enumeration of 113B28 pressure transducers used in the lab, with their
        sensitivity values taken from their calibration certificate, attached 
        to their respective serial number.
    '''
    LW41871 = {
        'psi_conversion': 103.0e-3,  # V/psi
        'kPa_conversion': 14.94e-3,  # V/kPa 
    }
    LW41374 = {
        'psi_conversion': 100.0e-3,  # V/psi
        'kPa_conversion': 14.51e-3,  # V/kPa
    }

class PressureData:
    def __init__(self, sensor: Sensor = Sensor.LW41871, imperial = False):
        self.imperial = imperial
        if imperial:
            self.conversion = sensor.value['psi_conversion']
        else:
            self.conversion = sensor.value['kPa_conversion']
    
    def load_from_array(self, array, time=True, offset='auto', 
                        trimstart=False):
        self.pressure = array[:,1]/self.conversion
        if time:
            self.time = array[:,0]
        if offset == 'auto':
            window_right_edge = int(0.4*self.pressure.size)
            zero = np.mean(self.pressure[:window_right_edge])
        else:
            zero = -offset
        self.pressure -= zero
        if trimstart: 
            startindex = int(array.shape[0]/2)
            self.pressure = np.delete(self.pressure, np.s_[:startindex], 0)
            self.time = np.delete(self.time, np.s_[:startindex], 0)


    def get_data(self):
        return np.stack((self.time, self.pressure), axis=1)

    def filter_data(self, n=30):
        self.pressure_raw = self.pressure
        b = [1.0/n]*n
        self.pressure = lfilter(b, 1, self.pressure)

    def load_from_wavedata(self, shot_id, offset='auto', trimstart=False):
        '''
            Loads pressure data from a given shot identifier code. Returns 
            laser power meter data too as a bonus.
        '''
        data_directory = DATAPATH+'Pressure Data/{}/'.format(shot_id)
        fnumbers = get_channel_files(data_directory)
        power_signal = np.loadtxt('{}WaveData{}.csv'.format(data_directory,
                                                            fnumbers[0]),
                                                            **loadtxtparams)
        pressure_signal = np.loadtxt('{}WaveData{}.csv'.format(data_directory,
                                                               fnumbers[1]),
                                                               **loadtxtparams)
        self.load_from_array(pressure_signal, 
                             offset=offset, 
                             trimstart=trimstart)
        return power_signal

if __name__ == '__main__':
    ...