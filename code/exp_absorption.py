from datamanager import shotlist
from Laser import util
import matplotlib.pyplot as plt

pulse_buffer_width = 1  # ms, laser pulse duration BEFORE spark

# Create mask for valid absorption data
mask = (shotlist['Series Prefix'] == 'SPX') \
    * (shotlist['Output Energy [J]'] > 0)

shots = shotlist[mask]

pulse_energy = util.sp2energy(shots['Laser Setpoint'], 
                              shots['Pulse width [ms]'])
buffer_fraction = (pulse_buffer_width/shots['Pulse width [ms]'])
buffer_energy = pulse_energy*buffer_fraction*util.entryFactor*util.exitFactor
energy_m_nobuffer = shotlist[mask]['Output Energy [J]']-buffer_energy

transmitted_energy = energy_m_nobuffer/util.exitFactor
input_energy = (1-buffer_fraction)*pulse_energy*util.entryFactor

absorption = 1-transmitted_energy/input_energy

print(absorption)

plt.plot(shots['Pressure [bar]'], absorption, 'o')
plt.xlabel('Pressure $p$ [bar]')
plt.ylabel('Absorption $a$ [-]')
plt.show()