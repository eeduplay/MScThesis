import numpy as np
import matplotlib.pyplot as plt

excitationVoltage = 4.4  # V
OpAmpGain = 21
sensitivity = 1.8e-3  # V/V/N
voltToN = 1/(sensitivity*excitationVoltage*OpAmpGain)

def read_WinDAQ_csv(path):
    signal = np.loadtxt(path, usecols=0)
    load = signal*voltToN
    return signal, load-load[0]

if __name__ == '__main__':
    
    voltage, load = read_WinDAQ_csv(r"E:\Cold Flow Tests\weight test 2.csv")
    # plt.plot(load)
    plt.plot(voltage-voltage[0])
    plt.xlabel('Sample')
    # plt.ylabel('Load [N]')
    plt.show()