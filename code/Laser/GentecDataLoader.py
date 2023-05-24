import pandas as pd
import os

def load_csv_data(path: str, mode: str, name: str):
    if mode == 'power':
        skip = 19
    elif mode == 'sse':
        skip = 18
    return pd.read_csv(path, 
                       header=None, 
                       sep='\t', 
                       usecols=[0], 
                       names=[name],
                       skiprows=skip)