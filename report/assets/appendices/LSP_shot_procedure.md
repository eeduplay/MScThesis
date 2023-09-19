# LSP Shot Procedure

This checklist is used for starting up, using, then shutting down the Laser-Sustained Plasma (LSP) experiment to perform and LSP test. This checklist assumes the laser has already been aligned.

Not all components are used for all experiments (e.g. spark igniter). Avoid setting them up if not necessary.

### STARTUP PROCEDURE

1. Power on triggering and monitoring station
    1. Turn on delay generators, oscilloscope
    2. Oscilloscope trigger should be set to “Normal” mode
    3. Turn on laser in LOCAL mode
    4. Verify that timing delays have the correct value *****and***** unit (ms)
    5. Verify that delay generators, camera, and laser are connected according to wiring diagram
2. Setup camera
    1. Turn on camera
    2. Connect to camera using Yellow Cat 6 cable
    3. Start PFV4 software and acquire live camera feed
    4. Calibrate sensor
    5. Remove lens cap
    6. Attach ND Filter and UV-IR Cut Filter to lens
    7. Adjust camera position and focus to frame the LSP ignition point (spark plug tips) at a 300 mm focal length
        
        <aside>
        ℹ️ Use low-light mode, set the lens aperture to f/4, set the ND Filter to minimum, and use additional lighting if needed
        
        </aside>
        
    8. Turn off low-light mode, set the camera frame rate to 10000 fps
    9. Set the aperture to f/22 and the ND filter to the maximum level
3. Setup power meter
    1. The black rubber protective cap should be on
    2. Plug in the power meter’s fan power supply and ensure the fan is running
    3. Turn on the BLU emitter (blue button)
    4. Connect to the power meter on the PC Gentec-EO software using the Bluetooth dongle (attached to blue USB extension cord)
        
        <aside>
        ℹ️ For best results, leave the Bluetooth dongle within the test area
        
        </aside>
        
    5. Remove the black rubber protective cap and allow the power meter’s signal to stabilize
    6. Set the wavelength to 1070 nm and perform the zeroing procedure
    7. Set the power meter to “SSE (J)” (Single Shot Energy) mode
    8. Suggested: set the display mode to “Statistics”
    9. If applicable, set your acquisition settings (filename, etc)
4. Setup spectrometer
    1. Use a laser pointer and a 100 micron fiber attached to the fiber mount to ensure the fiber tip is pointed at the ignition point, then re-attach the spectrometer fiber (10 micron) to the fiber mount
    2. Connect to the spectrometer via USB and start the OceanView Lite software, in “Quick View” mode
    3. Click “Create dark background spectrum”
    4. Set the integration time to 4 ms and the trigger mode to “Edge”
5. Setup pressure transducer
    1. If the transducer is already mounted, all that is needed is to turn on the signal conditioner and check that the Channel 1 indicator is green
6. Prepare test area
    1. Ensure the laser protection panels (2) are installed over the beam path between the collimator and the test section
    2. Ensure that the collimator cap is **************OFF************** and no obstacle is present in the beam path. Use the guide laser to check.
    3. Pressurize the test section to the target pressure. If performing a flowing test, pressurize the feed lines upstream of the solenoid valve, and set the valve’s safety switch to the FIRE mode
        
        <aside>
        ℹ️ Before pressurizing to target pressure, evacuate the air in the test section by filling it with Argon to 5 bar then venting it to 1.5 bar, repeating this process three times.
        
        </aside>
        
        <aside>
        ⚠️ ********************************************************************The laser windows are rated for a maximum internal pressure of 20 bar. Do not exceed this pressure.******************************************************************** Some tolerance for overpressure (~1 bar) is available in order to let the system stabilize to 20 bar, but do not run tests in overpressure conditions. *Destructive testing has not been performed to determine the actual failure pressure.*
        
        </aside>
        
    4. Plug in the spark igniter to the mains
        
        ⚠️ The igniter is now **ON** and will spark when receiving a signal
        
    5. Exit the area enclosed by the laser safety curtains and close them

The experiment is now ready to be run.

### RUNNING THE EXPERIMENT

1. Perform a final check on the control station to verify the timings and connections of the delay generators, oscilloscope, and laser.
2. Prepare the laser
    1. Restart the laser in REMOTE mode
    2. Connect to the laser via the router, using the Black Cat 6 cable
    3. Use the laser’s web interface to set up the pulse. Check the following settings:
        
        `HW Emission Control` should be ENABLED
        
        `Pulse Mode` should be ENABLED
        
        <aside>
        ℹ️ For more information on the web interface, consult the laser user guide
        
        </aside>
        
    4. Set the pulse power setpoint to the desired value
    5. Set the pulse duration to the desired value
3. Connect to camera using Yellow Cat 6 cable, and confirm connection in PFV4
4. Click “Record” in PFV4. The button should read “Ready”
5. Set the spectrometer save settings by clicking “Configure graph saving” in OceanView, entering the appropriate LSP shot identifier code as the BaseName, click “Apply”
6. Click the “Save graph to files” icon in OceanView—this should turn the button red.
7. **********************************************************************All personnel present in the laboratory,********************************************************************** regardless of their involvement in the experiment, ********************************************************************************************************************************************must equip laser safety goggles rated for 1070 nm wavelengths beyond this step
8. Turn on the laboratory’s laser warning light (confirm visually) and ensure the door is closed
    
    🛑 Entering/exiting the laboratory is not permitted beyond this step
    
9. Disengage the laser’s front-panel E-stop. Call out “Safety OFF”.
10. Find the power supply switch wired in the back of the laser. Flick the switch ON then OFF. Call out “Laser is ARMED”.
    
    <aside>
    ℹ️ This starts the laser’s main power supply, this is indicated by a louder fan volume and the green button on the front panel being lit up
    
    </aside>
    
    ⚠️ The laser is now **armed** - it will emit a laser pulse when the trigger signal is active
    
11. The experiment is ready to run, go through the following checklist before firing:
    - [ ]  Curtains are ************CLOSED************
    - [ ]  Laboratory warning light is ****ON****
    - [ ]  Laser is **********ARMED**********
    - [ ]  Camera is **********READY**********
    - [ ]  Power meter monitor is active and awaiting pulses
    - [ ]  All delay generators are ****ON****
    - [ ]  Oscilloscope is ****ON****
    - [ ]  ******************************ALL LAB PERSONNEL IS WEARING LASER SAFETY GOGGLES******************************
12. If performing a flowing test, use the valve switch near the control station to initiate flow. Allow for 5 seconds for the flow to stabilize, or up to 45 seconds for the pressure transducer signal to return to 0.
13. You may press the `MAN TRIG` button to emit a laser pulse. Watch the ceiling above the test area to spot the flash of a successful LSP ignition
14. Press the front panel E-stop to safe the laser. Call out “SAFE”.
15. Regardless of ignition, the camera will have recorded footage. To perform a new shot, resume from step 4

<aside>
ℹ️ If at any point after step 6, someone must remove their safety glasses, enter, or leave the lab, press the E-stop to safe the laser. Resume procedure from step 5.

</aside>

### SHUTDOWN PROCEDURE

1. Press the laser’s front-panel E-stop
    
    ℹ️ Laboratory personnel is now free to remove their laser safety glasses, and can freely enter/leave the lab
    
2. Disable laser warning light
3. Open the laser safety curtains
4. Unplug the igniter
5. Vent the test section
6. Shut off the camera
7. Shut off the power meter, unplug its fan, and place the rubber protective cap back on
8. Screw on the collimator cap
9. Switch off the delay generators and the oscilloscope
10. Switch off the laser, place the keys in the “Miscellaneous” drawer of the component cabinet