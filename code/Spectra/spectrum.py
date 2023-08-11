import numpy as np
import matplotlib.pyplot as plt

class Spectrum:
    def __init__(self) -> None:
        pass

    def loadFromOceanView(self, path):
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
        self.rawmetadata = ''.join(preamble)
        self.data = np.loadtxt(path, skiprows=13)
        self.wavelengths = self.data[:,0]
        self.counts = self.data[:,1]

    def plot(self, metadata=False):
        fig, ax = plt.subplots()
        ax.plot(self.wavelengths, self.counts, linewidth=0.5)
        if metadata:
            ax.text(self.wavelengths.min(), self.counts.max(), self.rawmetadata, va='top', fontfamily='monospace', fontsize='x-small')
        ax.set_xlabel(r'Wavelength $\lambda$ [nm]')
        ax.set_ylabel(r'Count $N$ [-]')
        return fig, ax

if __name__ == '__main__':
    s = Spectrum()
    # s.loadFromOceanView('rawdata/spectra/calibration/CalibrationHalogen.txt') 
    # s.loadFromOceanView('rawdata/spectra/calibration/Mercury-Argog_Spectrum.txt') 
    s.loadFromOceanView('rawdata/spectra/LSP52_S2_Subt2_15-13-04-066.txt') 
    fig, ax = s.plot(metadata=True)
    plt.show()