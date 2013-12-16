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
    'SolOpenCmd' : False, #Whether valve is open or not
    'PressureRawInputReg' : 0 # Value an analog pressure meter would read
}
config['sim_constants']={
    'valve_rate' : -2 ,#psi/sec
    'pump_rate' : 1 #psi/sec
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
            {'name':'GasWriteOK',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':1019, 'blockname':'coil',
                'blocktype':1, 'datatype':'boolean'}}},
            {'name':'GasWriteErr',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':1020, 'blockname':'coil',
                'blocktype':1, 'datatype':'boolean'}}},
            {'name':'GasWriteBP',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':1021, 'blockname':'coil',
                'blocktype':1, 'datatype':'boolean'}}},
            {'name':'GasBypCmd',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':1100, 'blockname':'coil',
                'blocktype':1, 'datatype':'boolean'}}},
            {'name':'CommSeqCounter',  'typ':0, 'value':1, 'metadata':{
                'modbus':{ 'addr':2000, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'float'}}},
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
            {'name':'MstrWGasControlPump/Sol',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':3515, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'unsigned'}}},
            {'name':'MstrWGasSystemMode',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':3516, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'unsigned'}}},
            {'name':'MstrWGasMANPumpCmd',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':3517, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'unsigned'}}},
            {'name':'MstrWGasMANSolCmd',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':3518, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'unsigned'}}},
            {'name':'MstrWGasNothing1',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':3519, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'unsigned'}}},
            {'name':'MstrWGasNothing2',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':3520, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'unsigned'}}},
            {'name':'MstrWGasPIDSetpoint',  'typ':0, 'value':10, 'metadata':{
                'modbus':{ 'addr':3521, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'float'}}},
            {'name':'MstrWGasPIDGain',  'typ':0, 'value':115, 'metadata':{
                'modbus':{ 'addr':3523, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'float'}}},
            {'name':'MstrWGasPIDResetRate',  'typ':0, 'value':0.2, 'metadata':{
                'modbus':{ 'addr':3525, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'float'}}},
            {'name':'MstrWGasPIDRate',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':3527, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'float'}}},
            {'name':'MstrWGasPIDDeadband',  'typ':0, 'value':0.5, 'metadata':{
                'modbus':{ 'addr':3529, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'float'}}},
            {'name':'MstrWGasPIDCycleTime',  'typ':0, 'value':1, 'metadata':{
                'modbus':{ 'addr':3531, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'float'}}},
 
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
        'id' : 4,
        'points' : [
            {'name':'PumpRunCmd',  'typ':2, 'value':0, 'metadata':{
                'modbus':{ 'addr':4, 'blockname':'coil',
                'blocktype':1, 'datatype':'boolean'}}},
            {'name':'SolOpenCmd',  'typ':2, 'value':0, 'metadata':{
                'modbus':{ 'addr':5, 'blockname':'coil',
                'blocktype':1, 'datatype':'boolean'}}},
            {'name':'LEDOn',  'typ':0, 'value':1, 'metadata':{
                'modbus':{ 'addr':12, 'blockname':'coil',
                'blocktype':1, 'datatype':'boolean'}}},
            {'name':'ControlPump/Sol',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':99, 'blockname':'coil',
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
            {'name':'MANSolOpenCmd',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':103, 'blockname':'coil',
                'blocktype':1, 'datatype':'boolean'}}},
            {'name':'PIDIncrease',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':104, 'blockname':'coil',
                'blocktype':1, 'datatype':'boolean'}}},
            {'name':'PIDDecrease',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':105, 'blockname':'coil',
                'blocktype':1, 'datatype':'boolean'}}},
            {'name':'AUTOPumpRunCmd',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':106, 'blockname':'coil',
                'blocktype':1, 'datatype':'boolean'}}},
            {'name':'AUTOSolOpenCmd',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':107, 'blockname':'coil',
                'blocktype':1, 'datatype':'boolean'}}},
            {'name':'DigInputReg',  'typ':1, 'value':0, 'metadata':{
                'modbus':{ 'addr':0, 'blockname':'statusreg',
                'blocktype':2, 'datatype':'boolean'}}},
            {'name':'PressureRawInputReg',  'typ':1, 'value':3131, 'metadata':{
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
            {'name':'PressureScaled',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':1005, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'float'}}},
            {'name':'ComparisonReg',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':1999, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'uint'}}},
            {'name':'MstrRDigOut',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':2999, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'boolean'}}},
            {'name':'MstrRDigIn',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':3000, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'boolean'}}},
            {'name':'MstrRPressureInRaw',  'typ':0, 'value':0, 'metadata':{
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
            {'name':'MstrRPressureScaled',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':3006, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'float'}}},
            {'name':'MstrWControlPump/Sol',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':3049, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'uint'}}},
            {'name':'MstrWSystemMode',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':3050, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'uint'}}},
            {'name':'MstrWMANPumpCmd',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':3051, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'uint'}}},
            {'name':'MstrWMANSolCmd',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':3052, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'uint'}}},
            {'name':'MstrWNothing1',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':3053, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'uint'}}},
            {'name':'MstrWNothing2',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':3054, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'uint'}}},
            {'name':'MstrWPIDSetpoint',  'typ':0, 'value':10, 'metadata':{
                'modbus':{ 'addr':3055, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'float'}}},
            {'name':'MstrWPIDGain',  'typ':0, 'value':115, 'metadata':{
                'modbus':{ 'addr':3057, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'float'}}},
            {'name':'MstrWPIDResetRate',  'typ':0, 'value':0.2, 'metadata':{
                'modbus':{ 'addr':3059, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'float'}}},
            {'name':'MstrWPIDRate',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':3061, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'float'}}},
            {'name':'MstrWPIDDeadband',  'typ':0, 'value':0.5, 'metadata':{
                'modbus':{ 'addr':3063, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'float'}}},
            {'name':'MstrWPIDCycleTime',  'typ':0, 'value':1, 'metadata':{
                'modbus':{ 'addr':3065, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'float'}}},
            {'name':'PIDPressureScaled',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':3999, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'float'}}},
            {'name':'PIDSetpoint',  'typ':0, 'value':10, 'metadata':{
                'modbus':{ 'addr':4001, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'float'}}},
            {'name':'PIDGain',  'typ':0, 'value':115, 'metadata':{
                'modbus':{ 'addr':4003, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'float'}}},
            {'name':'PIDResetRate',  'typ':0, 'value':0.2, 'metadata':{
                'modbus':{ 'addr':4005, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'float'}}},
            {'name':'PIDRate',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':4007, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'float'}}},
            {'name':'PIDDeadband',  'typ':0, 'value':0.5, 'metadata':{
                'modbus':{ 'addr':4009, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'float'}}},
            {'name':'PIDFullPercent',  'typ':0, 'value':100, 'metadata':{
                'modbus':{ 'addr':4011, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'float'}}},
            {'name':'PIDZeroPercent',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':4013, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'float'}}},
            {'name':'PIDCycleTime',  'typ':0, 'value':1, 'metadata':{
                'modbus':{ 'addr':4015, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'float'}}},
            {'name':'PIDManualModeOutput',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':4017, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'float'}}},
            {'name':'MotorOutputEnabled',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':4019, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'float?'}}},
            {'name':'PIDOutputPercent',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':4020, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'float'}}},
            {'name':'PIDOldProcessValue',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':4022, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'float'}}},
            {'name':'PIDOlderProcessValue',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':4024, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'float'}}},
            {'name':'PIDOldErrorValue',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':4026, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'float'}}},
            {'name':'PIDLastScanTime',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':4028, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'uint32'}}},
            {'name':'PIDOnTime',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':4030, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'uint32'}}},
 
        ],
                    'timeout' : .1, #timeout for logic loop
                    'simiface' : {
                        #these values should correspond to those in config['simiface']
                        'typ' : 'udp',
                        'sport' : 9913,
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
                            'id' : 4,
                           }
                   ],
                   'clientifaces' : []
            }#End vdev2


config.write()


