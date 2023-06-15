LW1_LOSS = 0.0059  # Relative power loss through lens and first window
W2_LOSS  = 0.0030  # Relative power loss through second window

def get_transmission(measured, emitted):
    '''
        Estimates the transmission factor of the LSP
        ## Parameters:
            `measured`  Measured power or energy
            `emitted`   Emitted power or energy at collimator
        Can be either power or energy, unit does not matter as long as it's the same
    '''
    return measured/(emitted*(1-LW1_LOSS)*(1-W2_LOSS))

def get_emission(measured):
    '''
        Estimates the emitted power/energy based on a power meter reading through the
        entire facility (lens and both windows)
        ## Parameters:
            `measured`  Measured power or energy
        Can be either power or energy, output will be in the same unit
    '''
    return measured/((1-LW1_LOSS)*(1-W2_LOSS))