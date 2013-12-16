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
                'modbus':{ 'addr':13, 'blockname':'coil',
                'blocktype':1, 'datatype':'boolean'}}},
            {'name':'SingleReadDone',  'typ':2, 'value':0, 'metadata':{
                'modbus':{ 'addr':100, 'blockname':'coil',
                'blocktype':1, 'datatype':'boolean'}}},
            {'name':'SingleReadErr',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':101, 'blockname':'coil',
                'blocktype':1, 'datatype':'boolean'}}},
            {'name':'StationBypassed',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':102, 'blockname':'coil',
                'blocktype':1, 'datatype':'boolean'}}},
            {'name':'SingleWriteDone',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':103, 'blockname':'coil',
                'blocktype':1, 'datatype':'boolean'}}},
            {'name':'SingleWriteErr',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':104, 'blockname':'coil',
                'blocktype':1, 'datatype':'boolean'}}},
            {'name':'SeqCntDone',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':1001, 'blockname':'coil',
                'blocktype':1, 'datatype':'boolean'}}},
            {'name':'GasReadOK',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':1005, 'blockname':'coil',
                'blocktype':1, 'datatype':'boolean'}}},
            {'name':'GasReadErr',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':1006, 'blockname':'coil',
                'blocktype':1, 'datatype':'boolean'}}},
            {'name':'GasReadBypass',  'typ':1, 'value':0, 'metadata':{
                'modbus':{ 'addr':1007, 'blockname':'coil',
                'blocktype':1, 'datatype':'boolean'}}},
            {'name':'GasWriteOK',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':1020, 'blockname':'coil',
                'blocktype':1, 'datatype':'boolean'}}},
            {'name':'GasWriteErr',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':1021, 'blockname':'coil',
                'blocktype':1, 'datatype':'boolean'}}},
            {'name':'GasWriteBP',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':1022, 'blockname':'coil',
                'blocktype':1, 'datatype':'boolean'}}},
            {'name':'GasBypCmd',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':1101, 'blockname':'coil',
                'blocktype':1, 'datatype':'boolean'}}},
            {'name':'CommSeqCounter',  'typ':0, 'value':1, 'metadata':{
                'modbus':{ 'addr':42001, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'float'}}},
            {'name':'MstrRGasDigOut',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':43011, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'boolean'}}},
            {'name':'MstrRGasDigIn',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':43012, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'boolean'}}},
            {'name':'MstrRGasPressureInRaw',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':43013, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'unsigned'}}},
            {'name':'MstrRGasAnalogIn1',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':43014, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'unsigned'}}},
            {'name':'MstrRGasAnalogIn2',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':43015, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'unsigned'}}},
            {'name':'MstrRGasAnalogIn3',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':43016, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'unsigned'}}},
            {'name':'MstrRGasAnalogIn4',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':43017, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'unsigned'}}},
            {'name':'MstrRGasPressureScaled',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':43018, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'float'}}},
            {'name':'MstrWGasControlPump/Sol',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':43516, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'unsigned'}}},
            {'name':'MstrWGasSystemMode',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':43517, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'unsigned'}}},
            {'name':'MstrWGasMANPumpCmd',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':43518, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'unsigned'}}},
            {'name':'MstrWGasMANSolCmd',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':43519, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'unsigned'}}},
            {'name':'MstrWGasNothing1',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':43520, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'unsigned'}}},
            {'name':'MstrWGasNothing2',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':43521, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'unsigned'}}},
            {'name':'MstrWGasPIDSetpoint',  'typ':0, 'value':10, 'metadata':{
                'modbus':{ 'addr':43522, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'float'}}},
            {'name':'MstrWGasPIDGain',  'typ':0, 'value':115, 'metadata':{
                'modbus':{ 'addr':43524, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'float'}}},
            {'name':'MstrWGasPIDResetRate',  'typ':0, 'value':0.2, 'metadata':{
                'modbus':{ 'addr':43526, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'float'}}},
            {'name':'MstrWGasPIDRate',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':43528, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'float'}}},
            {'name':'MstrWGasPIDDeadband',  'typ':0, 'value':0.5, 'metadata':{
                'modbus':{ 'addr':43530, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'float'}}},
            {'name':'MstrWGasPIDCycleTime',  'typ':0, 'value':1, 'metadata':{
                'modbus':{ 'addr':43532, 'blockname':'holdingreg',
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
                'typ' : 'ModbusTCP',
                'address' : '127.0.0.1',
                'port' : 502,                
               }
        ],
        'icsifaces' : []# No ICS interface for this vdev
} #End vdev0

config['vdevs']['slave'] = {
        'name':'slave',
        'id' : 4,
        'points' : [
            {'name':'PumpRunCmd',  'typ':2, 'value':0, 'metadata':{
                'modbus':{ 'addr':5, 'blockname':'coil',
                'blocktype':1, 'datatype':'boolean'}}},
            {'name':'SolOpenCmd',  'typ':2, 'value':0, 'metadata':{
                'modbus':{ 'addr':6, 'blockname':'coil',
                'blocktype':1, 'datatype':'boolean'}}},
            {'name':'LEDOn',  'typ':0, 'value':1, 'metadata':{
                'modbus':{ 'addr':13, 'blockname':'coil',
                'blocktype':1, 'datatype':'boolean'}}},
            {'name':'ControlPump/Sol',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':100, 'blockname':'coil',
                'blocktype':1, 'datatype':'boolean'}}},
            {'name':'SystemInMAN',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':101, 'blockname':'coil',
                'blocktype':1, 'datatype':'boolean'}}},
            {'name':'SystemInAUTO',  'typ':0, 'value':1, 'metadata':{
                'modbus':{ 'addr':102, 'blockname':'coil',
                'blocktype':1, 'datatype':'boolean'}}},
            {'name':'MANPumpRunCmd',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':103, 'blockname':'coil',
                'blocktype':1, 'datatype':'boolean'}}},
            {'name':'MANSolOpenCmd',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':104, 'blockname':'coil',
                'blocktype':1, 'datatype':'boolean'}}},
            {'name':'PIDIncrease',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':105, 'blockname':'coil',
                'blocktype':1, 'datatype':'boolean'}}},
            {'name':'PIDDecrease',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':106, 'blockname':'coil',
                'blocktype':1, 'datatype':'boolean'}}},
            {'name':'AUTOPumpRunCmd',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':107, 'blockname':'coil',
                'blocktype':1, 'datatype':'boolean'}}},
            {'name':'AUTOSolOpenCmd',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':108, 'blockname':'coil',
                'blocktype':1, 'datatype':'boolean'}}},
            {'name':'DigInputReg',  'typ':1, 'value':0, 'metadata':{
                'modbus':{ 'addr':10001, 'blockname':'statusreg',
                'blocktype':2, 'datatype':'boolean'}}},
            {'name':'PressureRawInputReg',  'typ':1, 'value':3131, 'metadata':{
                'modbus':{ 'addr':30001, 'blockname':'inputreg',
                'blocktype':4, 'datatype':'uint'}}},
            {'name':'CalcReg1',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':41000, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'float'}}},
            {'name':'CalcReg2',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':41002, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'float'}}},
            {'name':'CalcReg3',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':41004, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'float'}}},
            {'name':'PressureScaled',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':41006, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'float'}}},
            {'name':'ComparisonReg',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':42000, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'uint'}}},
            {'name':'MstrRDigOut',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':43000, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'boolean'}}},
            {'name':'MstrRDigIn',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':43001, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'boolean'}}},
            {'name':'MstrRPressureInRaw',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':43002, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'uint'}}},
            {'name':'MstrRAnalogIn1',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':43003, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'uint'}}},
            {'name':'MstrRAnalogIn2',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':43004, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'uint'}}},
            {'name':'MstrRAnalogIn3',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':43005, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'uint'}}},
            {'name':'MstrRAnalogIn4',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':43006, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'uint'}}},
            {'name':'MstrRPressureScaled',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':43007, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'float'}}},
            {'name':'MstrWControlPump/Sol',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':43050, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'uint'}}},
            {'name':'MstrWSystemMode',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':43051, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'uint'}}},
            {'name':'MstrWMANPumpCmd',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':43052, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'uint'}}},
            {'name':'MstrWMANSolCmd',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':43053, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'uint'}}},
            {'name':'MstrWNothing1',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':43054, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'uint'}}},
            {'name':'MstrWNothing2',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':43055, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'uint'}}},
            {'name':'MstrWPIDSetpoint',  'typ':0, 'value':10, 'metadata':{
                'modbus':{ 'addr':43056, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'float'}}},
            {'name':'MstrWPIDGain',  'typ':0, 'value':115, 'metadata':{
                'modbus':{ 'addr':43058, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'float'}}},
            {'name':'MstrWPIDResetRate',  'typ':0, 'value':0.2, 'metadata':{
                'modbus':{ 'addr':43060, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'float'}}},
            {'name':'MstrWPIDRate',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':43062, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'float'}}},
            {'name':'MstrWPIDDeadband',  'typ':0, 'value':0.5, 'metadata':{
                'modbus':{ 'addr':43064, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'float'}}},
            {'name':'MstrWPIDCycleTime',  'typ':0, 'value':1, 'metadata':{
                'modbus':{ 'addr':43066, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'float'}}},
            {'name':'PIDPressureScaled',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':44000, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'float'}}},
            {'name':'PIDSetpoint',  'typ':0, 'value':10, 'metadata':{
                'modbus':{ 'addr':44002, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'float'}}},
            {'name':'PIDGain',  'typ':0, 'value':115, 'metadata':{
                'modbus':{ 'addr':44004, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'float'}}},
            {'name':'PIDResetRate',  'typ':0, 'value':0.2, 'metadata':{
                'modbus':{ 'addr':44006, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'float'}}},
            {'name':'PIDRate',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':44008, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'float'}}},
            {'name':'PIDDeadband',  'typ':0, 'value':0.5, 'metadata':{
                'modbus':{ 'addr':44010, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'float'}}},
            {'name':'PIDFullPercent',  'typ':0, 'value':100, 'metadata':{
                'modbus':{ 'addr':44012, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'float'}}},
            {'name':'PIDZeroPercent',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':44014, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'float'}}},
            {'name':'PIDCycleTime',  'typ':0, 'value':1, 'metadata':{
                'modbus':{ 'addr':44016, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'float'}}},
            {'name':'PIDManualModeOutput',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':44018, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'float'}}},
            {'name':'MotorOutputEnabled',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':44020, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'float?'}}},
            {'name':'PIDOutputPercent',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':44021, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'float'}}},
            {'name':'PIDOldProcessValue',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':44023, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'float'}}},
            {'name':'PIDOlderProcessValue',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':44025, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'float'}}},
            {'name':'PIDOldErrorValue',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':44027, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'float'}}},
            {'name':'PIDLastScanTime',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':44029, 'blockname':'holdingreg',
                'blocktype':3, 'datatype':'uint32'}}},
            {'name':'PIDOnTime',  'typ':0, 'value':0, 'metadata':{
                'modbus':{ 'addr':44031, 'blockname':'holdingreg',
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
                            'typ' : 'ModbusTCP',
                            'address' : '127.0.0.1',
                            'port' : 502,                
                            'id' : 4,
                           }
                   ],
                   'clientifaces' : []
            }#End vdev2


config.write()


