import numpy as np
from numpy.polynomial import polynomial
import matplotlib.pyplot as plt
from scipy import constants

wien_constant = 2.897771955e-3  # m K, proportionality constant for Wien's law

def planck(wavelength: np.float_, temperature: np.float_) -> np.float_:
    '''
        Computes theoretical black-body radiation for given wavelength/temperature
        
        `wavelength` : wavelength in meter \\
        `temperature` : temperature in Kelvin
    '''
    return (2*constants.h*constants.c**2) / \
            (wavelength**5*(np.exp(constants.h*constants.c / 
                                   (wavelength*constants.k*temperature))-1))

class Spectrum:
    def __init__(self, path, trimL=0, trimR=0, calibrate=True, 
                          coeff_path='rawdata/spectra/calibration/HgAr_pixel.csv'):
        '''
            Loads spectral data from an Ocean View spectrometer output file

            `path` : Path to spectral data file (.txt) \\
            `calibrate` : Set to False to use raw data, set to True (default) to 
                perform wavelength calibration \\
            `trimL` : Number of pixels to reject at the start of file, usually to 
                ignore bad pixels.
            `trimR` : Number of pixels to reject at the end of file, usually to 
                ignore bad pixels.
        '''
        self.metadata = {}
        with open(path, 'r') as f:
            preamble = list(f)[2:12]
            for l in preamble:
                label, value = l[:-1].split(': ', 1)
                try:
                    if value.isdigit():
                        value = int(value)
                    else:
                        value = float(value)
                except(ValueError):
                    pass
                self.metadata.update([(label, value)])
        self.metadata['Number of Pixels in Spectrum'] -= trimL+trimR
        data = np.loadtxt(path, skiprows=13+trimL, 
                               max_rows=self.metadata['Number of Pixels in Spectrum'])
        newpreamble = preamble[:-1]
        newpreamble.append('Number of Pixels in Spectrum: '
                           +str(self.metadata['Number of Pixels in Spectrum']))
        self.rawmetadata = ''.join(newpreamble)
        if calibrate:
            pixelcounts = np.loadtxt(coeff_path, delimiter=',', skiprows=1)
            wavelength_coeffs = polynomial.polyfit(
                pixelcounts[:,1]-trimL, pixelcounts[:,0], 3)
            self.wavelengths = polynomial.polyval(
                np.arange(self.metadata['Number of Pixels in Spectrum']), 
                wavelength_coeffs)
        else:
            self.wavelengths = data[:,0]
        self.counts = data[:,1]
        self.trimL = trimL
        self.trimR = trimR
        self.wavelength_calibrated = calibrate

    def calibrate_irradiance(self, temperature, ref_spectrum_path, 
                             ref_dark_spectrum_path, dark_spectrum_path=None):
        '''
            Calibrates spectrum based on radiometric calibration source spectrum

            `temperature` : Temperature of calibration source in Kelvin\\
            `ref_spectrum` : Measured spectral data of calibration source\\
            `dark_spectrum` : Measured spectral data of dark background
        '''
        max_lambda = wien_constant/temperature
        N = 100/planck(max_lambda, temperature)
        ref_spectrum = Spectrum(ref_spectrum_path, 
                                trimL=self.trimL, 
                                trimR=self.trimR,
                                calibrate=self.wavelength_calibrated)
        ref_dark_spectrum = Spectrum(ref_dark_spectrum_path, 
                                trimL=self.trimL, 
                                trimR=self.trimR,
                                calibrate=self.wavelength_calibrated)
        if dark_spectrum_path:
            dark_spectrum = Spectrum(dark_spectrum_path, 
                                trimL=self.trimL, 
                                trimR=self.trimR,
                                calibrate=self.wavelength_calibrated)
            DL_exp = dark_spectrum.counts()
        else:
            DL_exp = np.zeros_like(self.counts)
        irradiance_coeffs = N*planck(self.wavelengths, temperature) / \
                            (ref_spectrum.counts - ref_dark_spectrum.counts)
        self.counts = irradiance_coeffs*(self.counts-DL_exp)
                

    def plot(self, metadata=False, semilog=False):
        fig, ax = plt.subplots()
        if semilog:
            ax.semilogy(self.wavelengths, self.counts, linewidth=0.5)
        else:
            ax.plot(self.wavelengths, self.counts, linewidth=0.5)
        if metadata:
            ax.text(self.wavelengths.min(), self.counts.max(), 
                    self.rawmetadata, va='top', fontfamily='monospace', 
                    fontsize='x-small')
        ax.set_xlabel(r'Wavelength $\lambda$ [nm]')
        ax.set_ylabel(r'Count $N$ [-]')
        return fig, ax

if __name__ == '__main__':
    # s = Spectrum('rawdata/spectra/calibration/CalibrationHalogen.txt') 
    # s = Spectrum('rawdata/spectra/calibration/Mercury-Argog_Spectrum.txt') 
    s = Spectrum('rawdata/spectra/LSP52_S2_Subt2_15-13-04-066.txt', 
                        trimL=1) 
    fig, ax = s.plot(metadata=True, semilog=False)
    plt.show()