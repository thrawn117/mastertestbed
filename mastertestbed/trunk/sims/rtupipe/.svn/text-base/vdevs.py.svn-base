#!/usr/bin/env python

"""
@author Brad Reaves
@version 0.1
February 2011
License: GPL2

This module defines functions containing the control logic for the tank
virtual logic.
#vim: tw=80
"""
import time, struct, math, random
import cPickle

def pidd_controller(value, setpoint, gain, reset_time, rate_time, deadband,
                 full, zero, cycle_time, manual_mode_output, motor_output_enabled,
                 output, old_value,
                 older_value, old_error, last_run_time, on_time):
    #FIXME: Finish the logic, the docstring, and add the required points.
    """Implements the digital PID controller block for a Control Microsystems
    PLC. The functionality is described on page 307 of the Telepace User Manual.
    All arguments are Point-type objects. In the Control Microsystems memory
    model, all the listed registers are floating points and are contiguous and
    consecutive in memory. The arguments are listed in the order in which they
    appear in memory, so a list of these variables in memory order can be 
    provided as the argument list.
    The parameters match directly with the descriptions in the manual. 
    @returns A tuple of booleans of form (increase, decrease), where if increase
                is true, the process value should be increased, and if decrease
                is true, the process value should be decreased.
    """
    #This commented code is used to test that all variables were loaded 
    #correctly.
    #from pprint import pprint
    #print "BRDEBUG: locals():", pprint(locals())
    #raise Exception("Kill this thread")

    #Execution period in equation is cycle_time
    #Housekeeping
    old_output = output

    ##Calculate current error:
    error = setpoint.get() - value.get()

    ##Calculate raw output:
    first_term =  error - old_error.get()
    second_term = (cycle_time.get() / reset_time.get()) * error
    third_term = ((rate_time.get()/cycle_time.get()) 
                    *(value.get() - 2* old_value.get() + older_value.get()))
    raw_output = ( old_output.get()
                + gain.get() * (first_term + second_term+third_term)) 

    # Make sure that raw input is in proper range, else peg at +/- [zero,full]
    sign = -1 if raw_output < 0 else 1
    if math.fabs(raw_output) > full.get():
        raw_output = full.get() * sign
    elif math.fabs(raw_output) < zero.get():
        raw_output = zero.get() * sign
    
    #set output
    output.set(raw_output)

    #Housekeeping
    older_value.set(old_value.get())
    old_value.set(value.get())
    old_error.set(error)
    #last_run_time.set( time.time()) #This value is not clearly defined in docs

    #Set return values
    increase, decrease = False, False
    if output.get() > 0:
        increase = True
    elif output.get() < 0:
        decrease = True
    if math.fabs(error) < deadband.get(): #then we should do nothing
        pass
        #increase = False
        #decrease = False
    return increase, decrease


#NOTE: Instead of returning None, it might be smarter to take a copy
#      of the points and return a new set -- this would make slave changes
#      to point values essentially atomic and eliminate consistency issues 
def slave(points, *args, **kwds):
    ## Ladder Logic Page 1
    points['LEDOn'].set(True)

    ## Ladder Logic Page 2 -- Set up blocks of registers for the master to read
    ##      and write to
    points['MstrRDigIn'].set(0) # Should actually be Register 00001
    points['MstrRPressureInRaw'].set(points['PressureRawInputReg'].get())
    #MstrRAnalogIn1..4 should also be set, but there are no values for those
    points['MstrRPressureScaled'].set(points['PressureScaled'].get())
    points['PIDSetpoint'].set(points['MstrWPIDSetpoint'].get())
    points['PIDGain'].set(points['MstrWPIDGain'].get())
    points['PIDResetRate'].set(points['MstrWPIDResetRate'].get())
    points['PIDRate'].set(points['MstrWPIDRate'].get())
    points['PIDDeadband'].set(points['MstrWPIDDeadband'].get())
    points['PIDCycleTime'].set(points['MstrWPIDCycleTime'].get())

    ##Ladder Logic Page 3: Convert raw pressure in into PSI
    points['CalcReg1'].set(float(points['PressureRawInputReg'].get()))
    points['CalcReg2'].set(points['CalcReg1'].get() - 3131.00)
    points['CalcReg3'].set(points['CalcReg2'].get() / 8700)
    points['PressureScaled'].set(points['CalcReg3'].get() *100)
    points['PIDPressureScaled'].set(points['PressureScaled'].get())

    ##Ladder Logic Page 4: Determine operation mode.
    #This implementation doesn't use the comparison reg. to hold comp. values
    points['ControlPump/Sol'].set(points['MstrWControlPump/Sol'].get())
    points['SystemInMAN'].set(points['MstrWSystemMode'].get() == 1)
    points['SystemInAUTO'].set(points['MstrWSystemMode'].get() > 1)

    ## Ladder Logic Page 5: Determine if manual Pump or solenoid is set
    if points['SystemInMAN'].get() and points['MstrWMANPumpCmd'].get():
        points['MANPumpRunCmd'].set(True)
    else:
        points['MANPumpRunCmd'].set(False)

    if points['SystemInMAN'].get() and points['MstrWMANSolCmd'].get():
        points['MANSolOpenCmd'].set(True)
    else:
        points['MANSolOpenCmd'].set(False)


    ## Ladder Logic Page 6: Set Pump and Solenoid open or closed
    points['PumpRunCmd'].set(False)
    if points['SystemInAUTO'].get():
        if points['AUTOPumpRunCmd'].get() and not points['ControlPump/Sol'].get():
            points['PumpRunCmd'].set(True)
        elif points['ControlPump/Sol'].get():
            points['PumpRunCmd'].set(True)
    if points['SystemInMAN'].get() and points['MANPumpRunCmd'].get():
        points['PumpRunCmd'].set(True)

    points['SolOpenCmd'].set(False)
    if points['SystemInAUTO'].get():
        if points['AUTOSolOpenCmd'].get() and points['ControlPump/Sol'].get():
            points['SolOpenCmd'].set(True)
        elif not points['ControlPump/Sol'].get():
            points['SolOpenCmd'].set(True)
    if points['SystemInMAN'].get() and points['MANSolOpenCmd'].get():
        points['SolOpenCmd'].set(True)

    ## Ladder Logic Page 7a: Use PID controller to handle "Auto" mode 
    #   Get the PID points from the configuration using their hardcoded address
    #   and sort them by their address so they are in the order the PID 
    #   code expects. 
    pid_vars = [pt for pt in points.values() 
                    if pt.metadata['modbus']['addr'] in xrange(4000-1,4032-1) ]
    pid_vars = sorted(pid_vars, key = lambda pt: pt.metadata['modbus']['addr'])
    if points['SolOpenCmd'].get() or points['PumpRunCmd'].get():
        inc, dec = pidd_controller(*pid_vars)
        points['PIDIncrease'].set(inc)
        points['PIDDecrease'].set(dec)
    
    ## Ladder Logic Page 7b: Determine if control action is needed
    if points['PIDIncrease'].get() and not points['ControlPump/Sol'].get():
        points['AUTOPumpRunCmd'].set(True)
    else:
        points['AUTOPumpRunCmd'].set(False)

    if not points['PIDIncrease'].get() and points['ControlPump/Sol'].get():
        points['AUTOSolOpenCmd'].set(True)
    else:
        points['AUTOSolOpenCmd'].set(False)
        
    ##BR: Keep a list of pressures every time we loop through:
    f = open('/tmp/slave_pressures','a')
    out = str(time.time()) + ' : ' + str(points['PIDPressureScaled'].get()) + '\n'
    f.write(out)
    f.close()

def master_delay_time():
    """This function models the variable processing delay using a piecewise
        probabilistic approximation.
        @returns Amount of time to sleep before completing master logic call"""
    slope1 = 0.089230769230769238
    slope2 = 0.4081293706293706
    eq1 = lambda x: x* slope1
    eq2 = lambda x: x* slope2 - .229
    eq  = lambda x: eq1(x) if x<.722167  else eq2(x)
    x = random.random() #Interval: [0,1)
    return eq(x)

def master_proper(points, clients, *args, **kwds):
    """Function implementing the master functionality emulating the ladder logic
        as closely as possible."""
    import warnings
    warnings.simplefilter('error')
    ## Set all coils to False -- this emulates the ladder logic memory model
    for point in points.values(): 
        if point.metadata['modbus']['blockname'] == 'coil':
            point.set(False)

    ## Ladder Logic Page 1 -- Turn "LED" On
    points['LEDOn'].set(True)

    ## Ladder Logic Page 2 -- Set the SingleWriteDone oneshot
    last_gas_read = getattr(master, "last_gas_read", False)
    if points['GasReadOK'].get() and not last_gas_read: #if GasReadOk has changed
        points['SingleReadDone'].set(True)
    master.last_gas_read = points['GasReadOK'].get()

    ##Ladder Logic Page 3 -- Set the SingleWriteDone oneshot
    last_gas_write = getattr(master, "last_gas_write", False)
    if points['GasWriteOK'].get() and not last_gas_write: #if GasReadOk has changed
        points['SingleWriteDone'].set(True)
    master.last_gas_write = points['GasWriteOK'].get()

    ##Ladder Logic Page 4 -- Set SingleReadErr oneshot
    last_gas_rerr = getattr(master, "last_gas_rerr", False)
    if points['GasReadErr'].get() and not last_gas_rerr: #if GasReadOk has changed
        points['SingleReadErr'].set(True)
    master.last_gas_rerr = points['GasReadErr'].get()

    ##Ladder Logic Page 5 -- Set SingleWriteErr oneshot
    last_gas_werr = getattr(master, "last_gas_werr", False)
    if points['GasWriteErr'].get() and not last_gas_werr: #if GasReadOk has changed
        points['SingleWriteErr'].set(True)
    master.last_gas_werr = points['GasWriteErr'].get()

    ##Ladder Logic Page 8 -- Send gas read message
    if points['CommSeqCounter'].get() == 1: 
        #names of points on slave to read
        points_to_read = ['MstrRDigOut', 'MstrRDigIn', 'MstrRPressureInRaw', 
                            'MstrRAnalogIn1', 'MstrRAnalogIn2', 'MstrRAnalogIn3',
                            'MstrRAnalogIn4', 'MstrRPressureScaled']
        #names of points on the master where response is stored. These are in
        #   order corresponding to the points read
        points_to_store = ['MstrRGasDigOut', 'MstrRGasDigIn', 
                            'MstrRGasPressureInRaw', 'MstrRGasAnalogIn1', 
                            'MstrRGasAnalogIn2', 'MstrRGasAnalogIn3',
                            'MstrRGasAnalogIn4', 'MstrRGasPressureScaled']
        try:
            reply = clients['slave'].readPoints(points_to_read)
            for index, point_name in enumerate(points_to_read):
                #Set points to read values
                points[points_to_store[index]].set(reply[index]) 

        except Exception as error:
            #TODO: Log error here
            print "BRDEBUG: Caught exception when reading points."
            print error

    ## Ladder Logic Page 13: Send gas write mesage
    if points['CommSeqCounter'].get() == 6: 
        #list of names of master pts to write to slave#FIXME
        points_to_write = ['MstrWGasControlPump/Sol', 'MstrWGasSystemMode', 
                                'MstrWGasMANPumpCmd', 'MstrWGasMANSolCmd', 
                                'MstrWGasNothing1', 'MstrWGasNothing2', 
                                'MstrWGasPIDSetpoint', 'MstrWGasPIDGain', 
                                'MstrWGasPIDResetRate', 'MstrWGasPIDRate', 
                                'MstrWGasPIDDeadband', 'MstrWGasPIDCycleTime']

        values_to_write = [points[name].get() for name in points_to_write] 
        #list of names of slave pts to write
        points_to_write_to = ['MstrWControlPump/Sol', 'MstrWSystemMode', 
                                'MstrWMANPumpCmd', 'MstrWMANSolCmd', 
                                'MstrWNothing1', 'MstrWNothing2', 
                                'MstrWPIDSetpoint', 'MstrWPIDGain', 
                                'MstrWPIDResetRate', 'MstrWPIDRate', 
                                'MstrWPIDDeadband', 'MstrWPIDCycleTime']
        points_values = zip(points_to_write_to, values_to_write)

        try:
            reply = clients['slave'].writePoints(points_values)
        except Exception as error:
            #TODO: Log error here
            print "BRDEBUG: Caught exception when writing points"
            print error
            import sys, traceback
            traceback.print_exc()
            pass


    ## Set appropropriate counter values 
    #   This must be done at the end, otherwise the write immediately follows
    #       the read
    if points['CommSeqCounter'].get() == 6:
        points['CommSeqCounter'].set(1) # Set into read mode
    else:
        points['CommSeqCounter'].set(6) # Set into write mode

    ##BR: Keep a list of pressures every time we loop through for testing:
    f =open('/tmp/master_pressures','a')
    out = str(time.time()) + ' : ' + str(points['MstrRGasPressureScaled'].get()) + '\n'
    f.write(out)
    f.close()#Opening, closing, and writing the files takes about 300 usec.
    
    ## Model processing time
    time.sleep(master_delay_time())


master = master_proper

