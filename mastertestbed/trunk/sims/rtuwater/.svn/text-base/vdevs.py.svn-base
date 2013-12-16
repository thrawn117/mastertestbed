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

#NOTE: Instead of returning None, it might be smarter to take a copy
#      of the points and return a new set -- this would make slave changes
#      to point values essentially atomic and eliminate consistency issues 
def slave(points, *args, **kwds):
    ## Ladder Logic Page 1
    points['LEDOn'].set(True)

    ## Ladder Logic Page 2 -- Set up blocks of registers for the master to read
    ##      and write to
    points['MstrRDigOut'].set(0) # Should actually be Register 00001
    points['MstrRDigIn'].set(0) # Should actually be Register 00001
    points['MstrRLevelInRaw'].set(points['LevelRawInputReg'].get())
    #MstrRAnalogIn1..4 should also be set, but there are no values for those
    points['MstrRLevelScaled'].set(points['LevelScaledFloat'].get())

    ##Ladder Logic Page 3: Convert raw pressure in into PSI
    points['CalcReg1'].set(float(points['LevelRawInputReg'].get()))
    points['CalcReg2'].set(points['CalcReg1'].get() - 3563.00)
    points['CalcReg3'].set(points['CalcReg2'].get() / 3518)
    points['LevelScaledFloat'].set(points['CalcReg3'].get() *100)
    level_f = points['LevelScaledFloat'].get()
    points['LevelScaledInt'].set(0 if int(level_f) < 0 else int(level_f) & 0xFFFF )

    ##Ladder Logic Page 4: Determine operation mode and manual pump command
    #This implementation doesn't use the comparison reg. to hold comp. values
    points['SystemInMAN'].set(points['MstrWSystemMode'].get() == 1)
    points['SystemInAUTO'].set(points['MstrWSystemMode'].get() > 1)
    points['MANPumpRunCmd'].set(points['SystemInMAN'].get() 
                                and points['MstrWMANPumpCmd'].get())


    ## Ladder Logic Page 5: Determine if alarms are set
    level = points['LevelScaledInt'].get()
    points['LowLevelAlarm'].set(level < points['MstrWLowAlarmLevel'].get())
    points['HighLevelAlarm'].set(level > points['MstrWHighAlarmLevel'].get())

    ## Ladder Logic Page 6: Set alarm status
    if points['LowLevelAlarm'].get():
        points['MstrRAlarms'].set(2)
    elif points['HighLevelAlarm'].get():
        points['MstrRAlarms'].set(1)
    else:
        points['MstrRAlarms'].set(0)

    ## Ladder Logic Page 7: Determine if we've hit setpoints or not
    level = points['LevelScaledInt'].get()
    points['LowLevelFloat'].set(level < points['MstrWLowSetpoint'].get())
    points['HighLevelFloat'].set(level > points['MstrWHighSetpoint'].get())

    ## Ladder Logic Page 8: Determine if pump should be turned on or not
    if (points['SystemInAUTO'].get() and not points['HighLevelFloat'].get()
         and (points['LowLevelFloat'].get() or points['PumpRunCmd'].get() )):
        points['PumpRunCmd'].set(True)
    elif points['SystemInMAN'].get() and points['MANPumpRunCmd'].get():
        points['PumpRunCmd'].set(True)
    else:
        points['PumpRunCmd'].set(False)

    ##BR: Keep a list of levels every time we loop through:
    f = open('/tmp/slave_levels','a')
    out = str(time.time()) + ' : ' + str(points['LevelScaledFloat'].get()) + '\n'
    f.write(out)
    f.close()

def master_delay_time():
    """This function models the variable processing delay using a piecewise
        probabilistic approximation.
        @returns Amount of time to sleep before completing master logic call"""
    eq = lambda x: 0 if x<.4 else .03265 if .4<=x<.835 else .61234*x-.46744
    x = random.random() #Interval: [0,1)
    return eq(x)

def master(points, clients, *args, **kwds):
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
    last_read_status = getattr(master, "last_read_status", False)
    read_status = points['GasReadOK'].get() or points['Water2ReadOK'].get()
    #if read_status has just become true, read_done should be true
    points['SingleReadDone'].set(read_status and not last_read_status)
    master.last_read_status = read_status

    ##Ladder Logic Page 3 -- Set the SingleWriteDone oneshot
    last_write_status = getattr(master, "last_write_status", False)
    write_status = points['GasWriteOK'].get() or points['Water2WriteOK'].get()
    #if write status has become true, write_done should be true
    points['SingleWriteDone'].set( write_status and not last_write_status)
    master.last_write_status = write_status 

    ##Ladder Logic Page 4 -- Set SingleReadErr oneshot
    last_read_err = getattr(master, "last_read_err", False)
    read_err = points['GasReadErr'].get()  or points['Water2ReadErr'].get()
    points['SingleReadErr'].set(read_err and not last_read_err)
    master.last_read_err = read_err

    ##Ladder Logic Page 5 -- Set SingleWriteErr oneshot
    last_write_err = getattr(master, "last_write_err", False)
    write_err = points['GasWriteErr'].get() and points['Water2WriteErr'].get() 
    #if write_err has changed, so shouls singlewriteerr
    points['SingleWriteErr'].set( write_err and not last_write_err)
    master.last_write_err = write_err


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

    ## Ladder Logic Page 11: Send Water2 Read Message
    if points['CommSeqCounter'].get() == 5: 
        #names of points on slave to read
        points_to_read = ['MstrRDigOut','MstrRDigIn','MstrRLevelInRaw',
                          'MstrRAnalogIn1','MstrRAnalogIn2','MstrRAnalogIn3',
                          'MstrRAnalogIn4','MstrRLevelScaled','MstrRAlarms']
        #names of points on the master where response is stored. These are in
        #   order corresponding to the points read
        points_to_store = ['MstrRWater2DigOut','MstrRWater2DigIn',
                           'MstrRWater2LevelInRaw','MstrRWater2AnalogIn1',
                           'MstrRWater2AnalogIn2','MstrRWater2AnalogIn3',
                           'MstrRWater2AnalogIn4','MstrRWater2LevelScaled',
                           'MstrRWater2Alarms']
        try:
            reply = clients['slave'].readPoints(points_to_read)
            for index, point_name in enumerate(points_to_read):
                #Set points to read values
                points[points_to_store[index]].set(reply[index]) 

        except Exception as error:
            #TODO: Log error here
            print "BRDEBUG: Caught exception when reading points."
            print error


    ## Ladder Logic Page 13: Send gas write message
    if points['CommSeqCounter'].get() == 6: 
        #list of names of master pts to write to slave
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
            import traceback
            traceback.print_exc()

    ## Ladder Logic Page 16: Send water2 write message
    if points['CommSeqCounter'].get() == 10: 
        #list of names of master pts to write to slave
        points_to_write = ['MstrWWater2SystemMode','MstrWWater2MANPumpRunCmd',
                           'MstrWWater2Null1','MstrWWater2Null2',
                           'MstrWWater2Null3','MstrWWater2Null4',
                           'MstrWWater2LowAlarmLevel','MstrWWater2LowSetpoint',
                           'MstrWWater2HighSetpoint','MstrWWater2HighAlarmLevel']

        values_to_write = [points[name].get() for name in points_to_write] 
        #list of names of slave pts to write
        points_to_write_to = ['MstrWSystemMode','MstrWMANPumpCmd','MstrWNull1',
                              'MstrWNull2','MstrWNull3',
                              'MstrWNull4','MstrWLowAlarmLevel',
                              'MstrWLowSetpoint','MstrWHighSetpoint',
                              'MstrWHighAlarmLevel']
        points_values = zip(points_to_write_to, values_to_write)

        try:
            reply = clients['slave'].writePoints(points_values)
        except Exception as error:
            #TODO: Log error here
            print "BRDEBUG: Caught exception when writing points"
            print error
            import sys, traceback
            traceback.print_exc()



    ## Set appropropriate counter values that govern message transmission
    #   This must be done at the end, otherwise the write immediately follows
    #       the read
    default_values = [5,10]
    master.counter_values = (getattr(master, 'counter_values', default_values))
    if master.counter_values == []:
        master.counter_values = default_values
    points['CommSeqCounter'].set(master.counter_values.pop(0)) 

    ##BRDEBUG: Keep a list of pressures every time we loop through for testing:
    f =open('/tmp/master_level','a')
    out = str(time.time()) + ' : ' + str(points['MstrRWater2LevelScaled'].get()) + '\n'
    f.write(out)
    f.close()#Opening, closing, and writing the files takes about 300 usec.
    
    ## Model processing time
    time.sleep(master_delay_time()) 

