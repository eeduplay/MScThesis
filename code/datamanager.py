'''
    Performs data import and processing for the LSP shotlist, exposing a mostly
    clean and usable DataFrame for use in other scripts
'''

from dotenv import load_dotenv
load_dotenv()
from os import getenv
import pandas as pd

DATAPATH = getenv('DATAPATH')

def __stability_converter__(content):
    return content == 'TRUE' or content == True

shotlist = pd.read_excel(DATAPATH+'LSP/shotlist.xlsx', 'Shotlist V2', 
                              index_col=3, usecols='A:P, R:U',
                            #   true_values=['TRUE'], 
                            #   false_values=['FALSE'],
                              converters={'Stable': __stability_converter__},
                              dtype={'Notes': str}
                              )
shotlist.fillna(value={'Nozzle Diameter [mm]': 0.0, 'Notes': ''}, inplace=True)
shotlist.dropna(subset=['Laser Setpoint'], inplace=True)