#!/usr/bin/env python
#Brad Reaves
#February 10, 2011

#This file generates a configuration file for the tank simulation
from configobj import ConfigObj


config=ConfigObj('./config', unrepr=True)

simifacetype='udp'

config['simiface']={
    'typ':'udp', 
    'sport':9912, #9912-9949 are unassigned
    'recipients' : [('127.0.0.1',9913)], #list of vdevs to send updates to
    'timeout' : .1 
}
config['sim_state']={
    'simtime' : 0, #time in the simulation
    'PumpRunCmd' : False, #Whether pump is on or off
    'LevelRawInputReg' :3518 # Value an analog pressure meter would read
}
config['sim_constants']={
    'minimum_level' :  -15.66, #percent full
    'maximum_level' :  99.68, #percent full
    'drain_rate' : -0.5486949 ,#percent/sec
    'pump_rate' : 0.9679714 #percent/sec
}
config['vdevs'] = { }
config['vdevs']['master'] = { 
        'name':'master',
        'id' : 0,
        'points' : [
            {'name':'LEDOn',  'typ':2, 'value':0, 'metadata':{
                'modbus':{ 'addr':12, 'blockname':'coil',
                'blocktype':1, 'datatype':'boolean'}}},
            {'name':'SingleReadDone',  'typ':2, 'value':0, 'metadata':{
                'modbus':{ 'addr':99, 'blockname':'coil',
                'blocktype':1, 'datatype':'boolean'}}},
            {'name':'SingleReadErr',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':100, 'blockname':'coil',
                'blocktype':1, 'datatype':'boolean'}}},
            {'name':'StationBypassed',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':101, 'blockname':'coil',
                'blocktype':1, 'datatype':'boolean'}}},
            {'name':'SingleWriteDone',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':102, 'blockname':'coil',
                'blocktype':1, 'datatype':'boolean'}}},
            {'name':'SingleWriteErr',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':103, 'blockname':'coil',
                'blocktype':1, 'datatype':'boolean'}}},
            {'name':'SeqCntDone',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':1000, 'blockname':'coil',
                'blocktype':1, 'datatype':'boolean'}}},
            {'name':'GasReadOK',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':1004, 'blockname':'coil',
                'blocktype':1, 'datatype':'boolean'}}},
            {'name':'GasReadErr',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':1005, 'blockname':'coil',
                'blocktype':1, 'datatype':'boolean'}}},
            {'name':'GasReadBypass',  'typ':1, 'value':0, 'metadata':{
                'modbus':{ 'addr':1006, 'blockname':'coil',
                'blocktype':1, 'datatype':'boolean'}}},
            {'name':'Water2ReadOK',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':1014, 'blockname':'coil',
                'blocktype':1, 'datatype':'boolean'}}},
            {'name':'Water2ReadErr',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':1015, 'blockname':'coil',
                'blocktype':1, 'datatype':'boolean'}}},
            {'name':'Water2Bypassed',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':1016, 'blockname':'coil',
                'blocktype':1, 'datatype':'boolean'}}},
            {'name':'GasWriteOK',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':1019, 'blockname':'coil',
                'blocktype':1, 'datatype':'boolean'}}},
            {'name':'GasWriteErr',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':1020, 'blockname':'coil',
                'blocktype':1, 'datatype':'boolean'}}},
            {'name':'GasWriteBP',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':1021, 'blockname':'coil',
                'blocktype':1, 'datatype':'boolean'}}},
            {'name':'Water2WriteOK',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':1029, 'blockname':'coil',
                'blocktype':1, 'datatype':'boolean'}}},
            {'name':'Water2WriteErr',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':1030, 'blockname':'coil',
                'blocktype':1, 'datatype':'boolean'}}},
            {'name':'Water2WriteBP',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':1031, 'blockname':'coil',
                'blocktype':1, 'datatype':'boolean'}}},
            {'name':'GasBypCmd',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':1100, 'blockname':'coil',
                'blocktype':1, 'datatype':'boolean'}}},
            {'name':'Water2BypCmd',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':1104, 'blockname':'coil',
                'blocktype':1, 'datatype':'boolean'}}},
            {'name':'CommSeqCounter',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':2000, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'undigned'}}},
            {'name':'MstrRGasDigOut',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':3010, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'boolean'}}},
            {'name':'MstrRGasDigIn',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':3011, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'boolean'}}},
            {'name':'MstrRGasPressureInRaw',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':3012, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'unsigned'}}},
            {'name':'MstrRGasAnalogIn1',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':3013, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'unsigned'}}},
            {'name':'MstrRGasAnalogIn2',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':3014, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'unsigned'}}},
            {'name':'MstrRGasAnalogIn3',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':3015, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'unsigned'}}},
            {'name':'MstrRGasAnalogIn4',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':3016, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'unsigned'}}},
            {'name':'MstrRGasPressureScaled',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':3017, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'float'}}},
            {'name':'MstrRWater2DigOut',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':3045, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'unsigned'}}},
            {'name':'MstrRWater2DigIn',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':3046, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'unsigned'}}},
            {'name':'MstrRWater2LevelInRaw',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':3047, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'unsigned'}}},
            {'name':'MstrRWater2AnalogIn1',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':3048, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'unsigned'}}},
            {'name':'MstrRWater2AnalogIn2',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':3049, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'unsigned'}}},
            {'name':'MstrRWater2AnalogIn3',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':3050, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'unsigned'}}},
            {'name':'MstrRWater2AnalogIn4',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':3051, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'unsigned'}}},
            {'name':'MstrRWater2LevelScaled',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':3052, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'unsigned'}}},
            {'name':'MstrRWater2Alarms',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':3053, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'unsigned'}}},
            {'name':'MstrWGasControlPump/Sol',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':3516, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'unsigned'}}},
            {'name':'MstrWGasSystemMode',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':3517, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'unsigned'}}},
            {'name':'MstrWGasMANPumpCmd',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':3518, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'unsigned'}}},
            {'name':'MstrWGasMANSolCmd',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':3519, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'unsigned'}}},
            {'name':'MstrWGasNothing1',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':3520, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'unsigned'}}},
            {'name':'MstrWGasNothing2',  'typ':0, 'value':10, 'metadata':{
                'modbus':{ 'addr':3521, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'float'}}},
            {'name':'MstrWGasPIDSetpoint',  'typ':0, 'value':115, 'metadata':{
                'modbus':{ 'addr':3523, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'float'}}},
            {'name':'MstrWGasPIDGain',  'typ':0, 'value':0.2, 'metadata':{
                'modbus':{ 'addr':3525, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'float'}}},
            {'name':'MstrWGasPIDResetRate',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':3527, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'float'}}},
            {'name':'MstrWGasPIDRate',  'typ':0, 'value':0.5, 'metadata':{
                'modbus':{ 'addr':3529, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'float'}}},
            {'name':'MstrWGasPIDDeadband',  'typ':0, 'value':1, 'metadata':{
                'modbus':{ 'addr':3531, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'float'}}},
            {'name':'MstrWGasPIDCycleTime',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':3532, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'unsigned'}}},
            {'name':'MstrWWater2SystemMode',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':3546, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'unsigned'}}},
            {'name':'MstrWWater2MANPumpRunCmd',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':3547, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'unsigned'}}},
            {'name':'MstrWWater2Null1',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':3548, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'unsigned'}}},
            {'name':'MstrWWater2Null2',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':3549, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'unsigned'}}},
            {'name':'MstrWWater2Null3',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':3550, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'unsigned'}}},
            {'name':'MstrWWater2Null4',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':3551, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'unsigned'}}},
            {'name':'MstrWWater2LowAlarmLevel',  'typ':0, 'value':30, 'metadata':{
                'modbus':{ 'addr':3552, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'unsigned'}}},
            {'name':'MstrWWater2LowSetpoint',  'typ':0, 'value':50, 'metadata':{
                'modbus':{ 'addr':3553, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'unsigned'}}},
            {'name':'MstrWWater2HighSetpoint',  'typ':0, 'value':60, 'metadata':{
                'modbus':{ 'addr':3554, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'unsigned'}}},
            {'name':'MstrWWater2HighAlarmLevel',  'typ':0, 'value':90, 'metadata':{
                'modbus':{ 'addr':3555, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'unsigned'}}},
 
        ],
        'timeout' : .1, #timeout for logic loop
        'simiface' : {
            #These values should correspond to those in config['simiface']
            'typ' : 'virtual',
            'timeout' : .1 
        },  #Dummy sim interface for this vdev because it doesn't affect the sim
        'clientifaces' : [
           {
                'name' : 'Modbus',
                'memory_model' : 'control_microsystems',
                'typ' : 'ModbusRTU',
                'port' : './pty/0',                
                'baudrate' : 9600,
               }
        ],
        'icsifaces' : []# No ICS interface for this vdev
} #End vdev0

config['vdevs']['slave'] = {
        'name':'slave',
        'id' : 7,
        'points' : [
            {'name':'PumpRunCmd',  'typ':2, 'value':0, 'metadata':{
                'modbus':{ 'addr':5, 'blockname':'coil',
                'blocktype':1, 'datatype':'boolean'}}},
            {'name':'LEDOn',  'typ':0, 'value':1, 'metadata':{
                'modbus':{ 'addr':12, 'blockname':'coil',
                'blocktype':1, 'datatype':'boolean'}}},
            {'name':'SystemInMAN',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':100, 'blockname':'coil',
                'blocktype':1, 'datatype':'boolean'}}},
            {'name':'SystemInAUTO',  'typ':0, 'value':1, 'metadata':{
                'modbus':{ 'addr':101, 'blockname':'coil',
                'blocktype':1, 'datatype':'boolean'}}},
            {'name':'MANPumpRunCmd',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':102, 'blockname':'coil',
                'blocktype':1, 'datatype':'boolean'}}},
            {'name':'LowLevelAlarm',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':103, 'blockname':'coil',
                'blocktype':1, 'datatype':'boolean'}}},
            {'name':'HighLevelAlarm',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':104, 'blockname':'coil',
                'blocktype':1, 'datatype':'boolean'}}},
            {'name':'LowLevelFloat',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':105, 'blockname':'coil',
                'blocktype':1, 'datatype':'boolean'}}},
            {'name':'HighLevelFloat',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':106, 'blockname':'coil',
                'blocktype':1, 'datatype':'boolean'}}},
            {'name':'LevelRawInputReg',  'typ':1, 'value':3563, 'metadata':{
                'modbus':{ 'addr':0, 'blockname':'inputreg',
                'blocktype':4, 'datatype':'uint'}}},
            {'name':'CalcReg1',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':999, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'float'}}},
            {'name':'CalcReg2',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':1001, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'float'}}},
            {'name':'CalcReg3',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':1003, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'float'}}},
            {'name':'LevelScaledFloat',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':1005, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'float'}}},
            {'name':'LevelScaledInt',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':1007, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'uint'}}},
            {'name':'ComparisonReg',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':1999, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'uint'}}},
            {'name':'MstrRDigOut',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':2999, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'boolean'}}},
            {'name':'MstrRDigIn',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':3000, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'boolean'}}},
            {'name':'MstrRLevelInRaw',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':3001, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'uint'}}},
            {'name':'MstrRAnalogIn1',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':3002, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'uint'}}},
            {'name':'MstrRAnalogIn2',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':3003, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'uint'}}},
            {'name':'MstrRAnalogIn3',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':3004, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'uint'}}},
            {'name':'MstrRAnalogIn4',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':3005, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'uint'}}},
            {'name':'MstrRLevelScaled',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':3006, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'float'}}},
            {'name':'MstrRAlarms',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':3008, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'uint'}}},
            {'name':'MstrWSystemMode',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':3049, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'uint'}}},
            {'name':'MstrWMANPumpCmd',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':3050, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'uint'}}},
            {'name':'MstrWNull1',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':3051, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'uint'}}},
            {'name':'MstrWNull2',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':3052, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'uint'}}},
            {'name':'MstrWNull3',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':3053, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'uint'}}},
            {'name':'MstrWNull4',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':3054, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'uint'}}},
            {'name':'MstrWLowAlarmLevel',  'typ':0, 'value':30, 'metadata':{
                'modbus':{ 'addr':3055, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'uint'}}},
            {'name':'MstrWLowSetpoint',  'typ':0, 'value':50, 'metadata':{
                'modbus':{ 'addr':3056, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'uint'}}},
            {'name':'MstrWHighSetpoint',  'typ':0, 'value':60, 'metadata':{
                'modbus':{ 'addr':3057, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'uint'}}},
            {'name':'MstrWHighAlarmLevel',  'typ':0, 'value':90, 'metadata':{
                'modbus':{ 'addr':3058, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'uint'}}},

        ],
        'timeout' : .1, #timeout for logic loop
        'simiface' : {
            #these values should correspond to those in config['simiface']
            'typ' : 'udp', 'sport' : 9913,
            'recipients' : [('127.0.0.1', 9912)],
            'timeout' : .1 
        },
        'icsifaces' : [
           {
                'name' : 'Modbus',
                'memory_model' : 'control_microsystems',
                'typ' : 'ModbusRTU',
                'port' : './pty/1',                
                'baudrate' : 9600,
                'id' : 7,
               }
       ],
       'clientifaces' : []
}#End vdev2


config.write()


