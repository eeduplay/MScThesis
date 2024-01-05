'''
    Utility functions for PCB Piezotronics pressure transducer data
'''
from dotenv import load_dotenv
load_dotenv()
import os
import numpy as np
from scipy.signal import lfilter
from enum import Enum

DATAPATH = os.getenv('DATAPATH')
loadtxtparams = {'skiprows': 3, 'delimiter': ','}

def get_channel_files(directory: str) -> list[int]:
    '''
        Utility function to identify the files exported by a Hantek oscilloscope in the
        correct order.
        ### Parameters
        directory : str
            Path to the directory containing the WaveData files exported by the 
            oscilloscope.
        ### Returns
        filenumbers : list of int
            List of the WaveData file numbers, in increasing order.
    '''
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
        '''
            Object containing pressure data collected from an 113B28 pressure 
            transducer.
            ### Parameters
            sensor : Member of `Sensor` enumeration, default=`Sensor.LW41871`
                The specific, unique pressure transducer that provided the data.
                Transducers used in the lab have already been pre-programmed in the
                `Sensor` enumeration.
            imperial : bool, optional, default=`False`
                Set to `True` to work in psi, otherwise will use kPa.
        '''
        self.imperial = imperial
        if imperial:
            self.conversion = sensor.value['psi_conversion']
        else:
            self.conversion = sensor.value['kPa_conversion']
    
    def load_from_array(self, array, time=True, offset: float | str ='auto', 
                        trimstart=False) -> None:
        '''
            Load pressure data from an existing numpy `ndarray`.
            ### Parameters
            time : bool, optional, default=`True`
                Set to `True` (default) to load temporal data.
            offset : float or 'auto', optional, default=`'auto'`
                Sets the zero-offset of the data. 'auto' uses the mean of the first 40%
                of the data as the offset. Otherwise, a float value can be provided.
            trimstart : bool, optional, default=`False`
                Truncates the first half of the dataset when set to `True`. This is
                useful when dealing with data from an oscilloscope that contains data
                from before the trigger point.
            ### Returns
                None. Processes and loads the data as 1-D arrays in the `pressure` and 
                `time` properties
        '''
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
        '''
            Getter function returning an `np.ndarray` of shape (2,N) of the time and 
            pressure.
        '''
        return np.stack((self.time, self.pressure), axis=1)

    def filter_data(self, n=30):
        '''
            Filters the pressure data using `scipy.signal.lfilter`. The `a` parameter
            of `lfilter` is set to 1. Consult the documentation on `lfilter` for more 
            information.
            ### Parameters
            n : int, default=30
                Controls the value of the `b` parameter passed to `lfilter` as follows:
                `b = [1.0/n]*n`
            ### Returns
            Nothing. Stores the unfiltered pressure signal in the `pressure_raw`
            property and updates `pressure` with the filtered signal.
        '''
        self.pressure_raw = self.pressure
        b = [1.0/n]*n
        self.pressure = lfilter(b, 1, self.pressure)

    def load_from_wavedata(self, shot_id: str, offset: float | str ='auto', 
                           trimstart=False):
        '''
            Legacy method used for LSP experiments. This allows specifying a shot
            identifier instead of a file or array to streamline data processing for the
            LTP project. This method is included for use in projects using the 
            following file structure:
            ```
            📂 DATAPATH/  # Full path of the experimental data directory
            └── 📂 Pressure Data/
                ├── 📂 LSP1_PS1/  # Directory named with shot identifier
                │   ├── 📄 WaveData1111.csv  # Channel 1 data
                │   └── 📄 WaveData1112.csv  # Channel 2 data
                ├── 📁 LSP2_PS2
                ├── 📁 LSP3_PS3
                └── ...
            ```
            This assumes the WaveDataXXXX.csv files are exported from a Hantek scope, 
            and that the first file (with a lesser number) is data from Channel 1,
            connected to the IPG laser's internal power meter, while the other file is 
            data from Channel 2, connected to the signal conditioner of the pressure 
            transducer.

            Loads pressure data from a given shot identifier code. Returns 
            laser power meter data too as a ✨bonus✨.
            ### Parameters
            shot_id : str
                Identifier for a specific experimental trial (shot)
            offset, trimstart : See documentation for `load_from_array`
            ### Returns
            1-D array of the Channel 1 signal. Also saves the pressure and time data to
            the `pressure` and `time` properties using `load_from_array`.
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