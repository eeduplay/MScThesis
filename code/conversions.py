'''
    Defines some convenient unit conversions
    Includes a quick function to generate secondary axes in an alternate unit
'''
import matplotlib as mpl

psiPerPa = 0.0254**2/(0.45359237*9.80665)

def Pa2psi(x):
    return x*psiPerPa

def psi2Pa(x):
    return x/psiPerPa

def convertAxis(which, convertorTuple, label=''):
    ax = mpl.pyplot.gca()
    if which == 'x':
        secax = ax.secondary_xaxis('top', functions=convertorTuple)
        secax.set_xlabel(label)
    elif which == 'y':
        secax = ax.secondary_yaxis('right', functions=convertorTuple)
        secax.set_ylabel(label)
    