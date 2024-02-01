'''
    Analyzes the pressure data from a given LSP shot
'''

import sys
import matplotlib.pyplot as plt
import numpy as np
from datamanager import shotlist
from Pressure.pcb import PressureData
from Laser import util

plt.style.use(['dark_background', './code/presentationPlots.mplstyle'])

# Thermo constants
Ar_cv = 312  # J/kg K
Ar_cp = 520  # J/kg K
Ar_R = 208  # J/kg K
init_T = 293.15  # K
volume = 0.335*np.pi*0.25*0.0381**2  # m^3, Approximate test section volume

U_DP = 0.4  # kPa, Delta P uncertainty
Ur_V = 0.037  # relative volume uncertainty
U_P = 1.0  # kPa, Nominal pressure uncertainty

DEFAULT_SHOT_ID = 'LSP1_PS1'
SAVE = 'save' in sys.argv and sys.argv[1] != 'save'
NOISY = 'noisy' in sys.argv and sys.argv[1] != 'noisy'
bbox_props = {
    'boxstyle': 'square, pad=0.1',
    'color': (1,1,1, 0.7)
}
REPORT_STRING = \
'''IDENTIFIER               PULSE
{:<15}{:>15}
------------------------------
Pulse width:        {:>6.2f} ms 
Nominal pressure:   {:>6.3f} bar
Pulse energy:       {:>6.2f} J  
Input energy:       {:>6.2f} J  
Argon mass:         {:>6.1f} g  
Temperature change: {:>6.2f} K  
Heat deposition:    {:>6.2f} J  
Efficiency:         {:>6.1f} %  '''

def plot_point(axes, x, y, label: str, above=False):
    offset = 0.3 if above else -0.3
    align = 'bottom' if above else 'top'
    axes.plot(x, y, 'o', mfc=(0,0,0,0), mec='black')
    axes.plot(x, y, 'k.', markersize=2)
    axes.text(x, y+offset, label+'\n{:.1f} ms\n{:.2f} kPa'.format(x, y),
              ha='center', va=align, fontfamily='monospace', 
              fontsize='x-small', backgroundcolor='white', bbox=bbox_props)

def analyze(shot_id: str, plot=False, save='', noisy=False, use_cp=False):
    '''
        Analyzes the pressure profile of a shot and determines heat deposition 
        and efficiency.
        ### Parameters
        `shot_id`: The LSP shot identifier, e.g. "LSP1_PS1"\\
        `plot`: Set to `True` for plot output\\
        `save`: If set to a path, saves plot to path. If empty string (default) 
        plot is not saved.
        ### Return
        `stats`: `dict` with the following keys:
        - 'E_in' Laser energy [J] into the chamber (Laser energy minus losses 
        from lens and window)
        - 'DeltaT' Change in temperature [K] calculated from change in pressure
        - 'Q_in' Heat [J] deposited into Argon in the chamber
        - 'eta' Heat transfer efficiency = Q_in/E_in
        - 'keypoints' a list of tuples for each key pressure points, ordered in
        time, i.e., first maximum, local minimum, second maximum. Each tuple
        is in the form (time [s], pressure [kPa]).
        - 'Ar_mass' Mass [kg] of Argon in the test section
        - 'uncertainty' relative uncertainty for Q_in, eta, and, in practice, 
        DeltaT too
    '''
    pressure = PressureData()
    power = pressure.load_from_wavedata(shot_id)
    pressure.filter_data()
    window_right_edge = int(0.4*power.shape[0])
    power -= np.mean(power[:window_right_edge, 1])
    heat_cap = Ar_cp if use_cp else Ar_cv

    # time slicing indices
    a, b = (window_right_edge, -50)
    laser_on = power[:,1] > 0.25
    laser_end = pressure.time[laser_on].max()

    # find key points
    peak1_window = (pressure.time > laser_end - 0.002) * (pressure.time < laser_end + 0.002)
    peak1_index = pressure.pressure[peak1_window].argmax()
    peak1_p = pressure.pressure[peak1_window].max()
    peak1_t = pressure.time[peak1_window][peak1_index]
    trough_window = (pressure.time > peak1_t) * (pressure.time < laser_end + 0.01)
    peak2_index = pressure.pressure.argmax()
    peak2_p = pressure.pressure.max()
    peak2_t = pressure.time[peak2_index]
    trough_index = pressure.pressure[trough_window].argmin()
    trough_p = pressure.pressure[trough_window].min()
    trough_t = pressure.time[trough_window][trough_index]

    # print('First peak: {:.2f} kPa, {:.1f} ms'.format(peak1_p, peak1_t*1000))
    # print('Second peak: {:.2f} kPa, {:.1f} ms'.format(peak2_p, peak2_t*1000))
    # print('Trough: {:.2f} kPa, {:.1f} ms'.format(trough_p, trough_t*1000))

    # Compute heat transfer estimates
    shotdata = shotlist.loc[shot_id]
    pw = shotdata['Pulse width [ms]']
    nomp = shotdata['Pressure [bar]']*1e5  # Pa
    pulse_type = shotdata['Pulse Spec']
    laser_energy = util.energy_from_shot_data(shotdata)
    input_energy = util.entryFactor*laser_energy  # J
    Ar_mass = nomp*volume/(Ar_R*init_T)  # kg, approximate Argon mass
    deltaT = (peak2_p*1e3/nomp) * init_T  # K
    Qin = Ar_mass*heat_cap*deltaT  # J
    thermal_efficiency = Qin/input_energy
    rel_uncertainty = np.sqrt((U_DP/peak2_p)**2 + (U_P/nomp)**2 + Ur_V**2)
    report_text = REPORT_STRING.format(shot_id, pulse_type, pw, nomp/1e5, 
                                    laser_energy, input_energy, Ar_mass*1000, 
                                    deltaT, Qin, thermal_efficiency*100)
    stats = {
        'E_in': input_energy,
        'DeltaT': deltaT,
        'Q_in': Qin,
        'eta': thermal_efficiency,
        'keypoints': [(peak1_t, peak1_p), (trough_t, trough_p), 
                      (peak2_t, peak2_p)],
        'Ar_mass': Ar_mass,
        'uncertainty': rel_uncertainty
    }
    if not plot and not save: return stats

    # Plotting
    fig0, ax0 = plt.subplots(figsize=(5.8, 4))
    if noisy: ax0.plot(pressure.time[a:b]*1000, pressure.pressure_raw[a:b], 
                       color='#00A6D6', alpha=0.33)
    ax0.plot(pressure.time[a:b]*1000, pressure.pressure[a:b], color='#00A6D6')
    y1, y2 = ax0.get_ylim()
    ax0.fill_between(pressure.time[a:b]*1000, 10, -10, 
                    where=power[a:b,1] > 0.25,
                    edgecolor='#ED1B2F',
                    facecolor=(0,0,0,0),
                    #  alpha=0.33, 
                    hatch=r'\\\ '[:-1],
                    label='Laser On')
    # Plotting key points
    plot_point(ax0, peak1_t*1000, peak1_p, 'First maximum', above=True)
    plot_point(ax0, peak2_t*1000, peak2_p, 'Second maximum')
    plot_point(ax0, trough_t*1000, trough_p, 'Minimum')

    ax0.set_ylim(y1, y2)

    ax0.text(pressure.time[b]*1000, 0, report_text, fontfamily='monospace', 
            fontsize='x-small', ha='right', va='bottom', bbox=bbox_props,
            backgroundcolor='white')

    ax0.legend()
    ax0.set_xlabel('Time $t$ [ms]')
    ax0.set_ylabel(r'Pressure change $\Delta p$ [kPa]')
    if save:
        plt.savefig(save)
    if plot: plt.show()
    return stats

if __name__ == '__main__':
    shot_id = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_SHOT_ID
    if SAVE: s = 'report/assets/5 results/pressure_an_{}.pdf'.format(shot_id)
    else: s = ''
    analyze(shot_id, plot=True, save=s, noisy=NOISY)