'''
    Evaluates the ratio of partition functions between Ar I and Ar II
    Scrapes partition function data from the NIST Atomic Spectra Database
'''

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import requests
from bs4 import BeautifulSoup

ROOT_URL = 'https://physics.nist.gov/cgi-bin/ASD/energy1.pl?de=0&spectrum={}&temp={}&submit=Retrieve+Data'
CACHE_PATH = '../cachedata/'

class Partition:
    def __init__(self, species) -> None:
        self.species = species
    
    def get_web_data(self, temperatures: np.ndarray, saveData=True):
        self.temperatures = temperatures
        self.data = buildDatabase(self.species, temperatures, save=saveData)
    
    def get_stored_data(self):
        self.data = useDatabase(self.species)
        self.temperatures = self.data[self.species[0]][:,0]

    def get_ratio(self, numerator, denominator, temp):
        if numerator not in self.species:
            raise ValueError(numerator+' specie not found in loaded data')
        if denominator not in self.species:
            raise ValueError(denominator+' specie not found in loaded data')
        a = np.interp(temp, self.temperatures, self.data[numerator][:,1])
        b = np.interp(temp, self.temperatures, self.data[denominator][:,1])
        return a/b
    
    def plot(self):
        for s in self.species:
            plt.plot(self.temperatures, self.data[s][:,1], label=s)
        plt.ylabel('Partition function $Z$')
        plt.xlabel('Temperature $T$ [K]')
        plt.legend()
        plt.show()

def getZfromNIST(specie: str, temp: float):
    temp_eV = round(temp/11606, 5)
    url = ROOT_URL.format(specie.replace(' ', '+'), temp_eV)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    target_span = soup.find_all('span', class_='one')[0]
    Z = float(target_span.find('b').text.split()[-1])
    return Z

def buildDatabase(species, temperatures, save=True):
    returnDict = {}
    for specie in species:
        array = np.column_stack((temperatures, np.ones(temperatures.shape)))
        for i, t in enumerate(temperatures):
            array[i,1] = getZfromNIST(specie, t)
        print('Data for', specie)
        print(array)
        if save: np.savetxt(CACHE_PATH+specie+'.csv', array,
                   header='Partition function values Z for '+specie+' at given temperatures [K]')
        returnDict[specie] = array
    return returnDict

def useDatabase(species):
    returnDict = {}
    for specie in species:
        returnDict[specie] = np.loadtxt(CACHE_PATH+specie+'.csv', skiprows=1)
    return returnDict

if __name__ == '__main__':
    species = ['Ar I', 'Ar II']
    CACHE_PATH = 'cachedata/'
    # temperatures = np.linspace(1000, 20000, 100)
    # data = buildDatabase(species, temperatures)
    # data = useDatabase(species)
    # temperatures = data['Ar I'][:,0]

    # fig, axs = plt.subplots(3, 1, sharex=True)
    # axs[0].plot(temperatures, data['Ar I'][:,1], label='Ar I')
    # axs[0].plot(temperatures, data['Ar II'][:,1], label='Ar II')
    # axs[0].set_ylabel('Partition function $Z$')
    # axs[1].plot(temperatures, data['Ar I'][:,1]/data['Ar II'][:,1])
    # axs[1].set_ylabel(r'Ratio $Z_\mathrm{Ar}/Z_\mathrm{Ar+}$')
    # axs[2].plot(temperatures, data['Ar II'][:,1]/data['Ar I'][:,1])
    # axs[2].set_ylabel(r'Ratio $Z_\mathrm{Ar+}/Z_\mathrm{Ar}$')
    # axs[2].set_xlabel('Temperature $T$ [K]')
    # plt.show()

    part = Partition(species)
    part.get_web_data(np.linspace(1000, 30000, 100), saveData=True)
    # part.get_stored_data()
    print(part.get_ratio('Ar I', 'Ar II', [5000, 6000, 7000, 25000]))
    part.plot()