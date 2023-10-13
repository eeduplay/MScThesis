from dotenv import load_dotenv
load_dotenv()
import numpy as np
from numpy.polynomial import polynomial
import matplotlib.pyplot as plt
from scipy import constants, signal, integrate, optimize, special
from os import listdir, getenv

DATAPATH = getenv('DATAPATH')

wien_constant = 2.897771955e-3  # m K, proportionality constant for Wien's law
DEFAULT_SPECTRA_PATH = DATAPATH+'/Spectra/'

def planck(wavelength: np.float_, temperature: np.float_) -> np.float_:
    '''
        Computes theoretical black-body radiation for given wavelength/temperature
        
        `wavelength` : wavelength in meter \\
        `temperature` : temperature in Kelvin
    '''
    return (2*constants.h*constants.c**2) / \
            (wavelength**5*(np.exp(constants.h*constants.c / 
                                   (wavelength*constants.k*temperature))-1))

def voigt_fit(x, x0, A, s, g):
    '''
        Wrapper for the voigt_profile that includes an x-offset parameter for emission
        line fitting.
    '''
    return A*special.voigt_profile(x-x0,s,g)

class Spectrum:
    def __init__(self, path, trimL=0, trimR=0, calibrate=True, raw=False,
                 coeff_path=DEFAULT_SPECTRA_PATH+'calibration/HgAr_pixel.csv'):
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
        if raw:
            with open(path, 'r') as f:
                data = np.loadtxt(path, delimiter=',')
                self.metadata['Number of Pixels in Spectrum'] = data.shape[0]
                self.rawmetadata = '{} pixels in spectrum'.format(data.shape[0])
        else:
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
        self.resolution = (self.wavelengths[-1] - self.wavelengths[0]) / \
            (self.wavelengths.size - 1)  #  nm/px, spectral resolution

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
        irradiance_coeffs = N*planck(self.wavelengths*1e-9, temperature) / \
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
    
    def find_lines(self, target_lines, hf=0.05, array=False, integrate=False,
                   verbose=False, voigt=False):
        '''
            Detects emission lines in the spectrum, by finding peaks, then
            matching them to the given emission lines in nm

            Returns a dictionary with `target_lines` as the keys, and a tuple
            of the corresponding measured wavelength, its height, and the
            corresponding index in self.wavelengths
        '''
        peak_indices, props = signal.find_peaks(self.counts, 
                                                height=hf*self.counts.max())
        measured_lines = []
        line_coeffs = []  # Either line heights or integrated spectral emission
        line_indices = []

        for line in target_lines:
            distances = np.absolute(self.wavelengths[peak_indices]-line)
            closest_p_idx = np.nanargmin(distances)
            m_lambda = self.wavelengths[peak_indices][closest_p_idx]
            measured_lines.append(m_lambda)
            line_indices.append(peak_indices[closest_p_idx])
            if integrate:
                line_coeffs.append(self.integrate_line(m_lambda, voigt=voigt))
            else:
                line_coeffs.append(self.counts[peak_indices][closest_p_idx])

        results_dict = dict(zip(target_lines, 
                        zip(measured_lines, line_coeffs, line_indices)))
        if verbose:
            print('Line [nm]    Observed [nm]   Value [-]   Index [-]')
            print('\n'.join(['{:>9.2f}{:>17.2f}{:>12.2f}{:>12d}'\
                             .format(key, *value) for key, value in \
                                results_dict.items()]))

        if array:
            return np.array([*zip(target_lines, measured_lines, line_coeffs, 
                                line_indices)])
        else:
            return results_dict
        
    def integrate_line(self, wavelength: float, radius: float = 3.0, 
                       voigt: bool = False) -> float:
        '''
            Returns the integrated emissive power (in arb. units per nm) of a
            given spectral line using cumulative trapezoid integration, with 
            the option to fit a voigt line profile beforehand.

            `wavelength`: The wavelength of the target emission line\\
            `radius`: How much of the spectrum to integrate on either side of 
            the line, must have same unit as `wavelength`. Default is 3.0. 
            Larger values are more likely to include other emission lines.\\
            `voigt`: If `True`, fit a voigt line profile to the data and 
            integrate over profile instead of the raw data. Default is `False`.
        '''
        data_slice = (self.wavelengths >= wavelength - radius) \
                        * (self.wavelengths <= wavelength + radius)
        if voigt:
            voigt_params, voigt_cov = optimize.curve_fit(
                voigt_fit, 
                self.wavelengths[data_slice],
                self.counts[data_slice],
                p0=[wavelength, 1.0, 1.0, 1.0],
                bounds=(0, np.inf))
            voigt_x = np.linspace(self.wavelengths[data_slice].min(), 
                                  self.wavelengths[data_slice].max())
            return integrate.trapezoid(voigt_fit(voigt_x, *voigt_params), 
                                       voigt_x)
        else:
            return integrate.trapezoid(self.counts[data_slice], 
                                       self.wavelengths[data_slice])
                
    
def get_filepath_from_ID(shotID):
    '''
        Searches a directory for the requested shot identifier, returns path
        to file as '`directory`/`shotID`_[rest of filename].txt'
    '''
    for filename in listdir(DEFAULT_SPECTRA_PATH):
        if filename.startswith(shotID):
            return DEFAULT_SPECTRA_PATH+filename

    return None

if __name__ == '__main__':
    shot_ID = 'LSP60_S9'
    spectrum_path = get_filepath_from_ID(shot_ID)
    # s = Spectrum('rawdata/spectra/calibration/Halogen_Light.txt', trimL=5) 
    # s = Spectrum('rawdata/spectra/calibration/Mercury-Argog_Spectrum.txt')
    s = Spectrum(spectrum_path, trimL=48, trimR=600)
    s.calibrate_irradiance(2800, 
                           'rawdata/spectra/calibration/Halogen_Light.txt',
                           'rawdata/spectra/calibration/Halogen_Dark.txt') 
    fig, ax = s.plot(metadata=True, semilog=False)
    print('Resolution: {:.3f} nm'.format(s.resolution))
    # planck2800 = planck(s.wavelengths*1e-9, 2800)
    # planck4800 = planck(s.wavelengths*1e-9, 4800)
    # plt.plot(s.wavelengths, s.counts/np.max(s.counts), label='HL-2000')
    # plt.plot(s.wavelengths, planck2800/np.max(planck2800), label='Black body 2800 K')
    # plt.plot(s.wavelengths, planck4800/np.max(planck4800), label='Black body 4800 K')
    # plt.legend()
    # plt.xlabel(r'Wavelength $\lambda$ [nm]')
    # plt.ylabel(r'Relative Irradiance [-]')
    observed_lines = s.find_lines(
        [
        696.54,
        706.72,
        750.39,
        751.47,
        763.51,
        794.82,
        826.45,
    ], integrate=True, verbose=True, voigt=True, array=True
    )
    ax.plot(observed_lines[:,1], s.counts[np.int32(observed_lines[:,-1].flatten())], 'o')
    plt.grid()
    plt.show()