'''
    Utility functions for PCB Piezotronics pressure transducer data
'''

import numpy as np
from enum import Enum

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
            self.conversion = sensor.values['psi_conversion']
        else:
            self.conversion = sensor.values['kPa_conversion']
    
    def load_from_array(self, array, time=True):
        self.pressure = array[:,1]/self.conversion
        if time:
            self.time = array[:,0]
            self.data = np.stack((self.time, self.pressure), axis=1)
            return self.data
        else: return self.pressure