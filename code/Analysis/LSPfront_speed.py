import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

wavefrontData = pd.read_csv('rawdata/LSP6_wavefrontTracking.csv',
                            header=None,
                            sep=',',
                            usecols=[0,4],
                            names=['Time [ms]', 'Position [mm]'],
                            skiprows=55)
wavefrontData.dropna(inplace=True)
wavefrontData['Position [mm]'] = -(wavefrontData['Position [mm]'] - wavefrontData['Position [mm]'][0])
wavefrontData['Speed [m/s]'] = np.gradient(wavefrontData['Position [mm]'], wavefrontData['Time [ms]'])
# plt.plot(wavefrontData['Time [ms]'], wavefrontData['Position [mm]'])
# plt.show()

# The following was written in most part by ChatGPT (3.5)
# Create the subplots
fig, axs = plt.subplots(2, 1, sharex=True, figsize=(5,5))

# Plot the first column ('Position [mm]')
axs[0].plot(wavefrontData['Time [ms]'], wavefrontData['Position [mm]'])
axs[0].set_ylabel('Position [mm]')

# Plot the second column ('Speed [mm/s]')
axs[1].plot(wavefrontData['Time [ms]'], wavefrontData['Speed [m/s]'])
axs[1].set_ylabel('Speed [m/s]')

# Set the x-axis label
plt.xlabel('Time [ms]')

# Display the plot
plt.show()

