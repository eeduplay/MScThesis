import os
import pandas as pd
from GentecDataLoader import load_csv_data

PATH_PREFIX = 'rawdata/laser_tests/Pulse Loss/'

pulseData_J = pd.concat([
    load_csv_data(PATH_PREFIX+'maxPower.csv', 'sse', 'No Optics'),
    load_csv_data(PATH_PREFIX+'maxPower3.csv', 'sse', 'No Optics 20s'),
    load_csv_data(PATH_PREFIX+'maxPower_optics.csv', 'sse', 'Optics')
], axis=1)


print(pulseData_J.describe())

print('Mean Relative Loss: {:.2f}%'.format(
    100*(pulseData_J['No Optics'].mean()-pulseData_J['Optics'].mean())/pulseData_J['No Optics'].mean()
    ))