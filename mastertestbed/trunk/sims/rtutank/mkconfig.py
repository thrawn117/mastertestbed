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
    'pump' : True, #Whether pump is on or off
    'valve' : False, #Whether valve is open or not
    'pressure' : 0 #Current pressure in the tank (psi)
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
            {'name':'pump',  'typ':2, 'value':False, 
                    'metadata':{'modbus':{ 'addr':'10', 'blockname':'coil',
                                    'blocktype':1},
                                'dnp3': {} }
            }, {'name':'valve', 'typ':2, 'value':False, 
                    'metadata':{'modbus':{ 'addr':'11', 'blockname':'coil',
                                    'blocktype':1},
                                'dnp3': {} }
            }, {'name':'pressure','typ':1, 'value':0.0, 
                    'metadata':{'modbus':{ 'addr':'30002', 'blockname':'inputreg',
                                    'blocktype':4, 'datatype':'float'},
                                'dnp3': {} }
            }, {'name':'setpoint',  'typ':0, 'value':0,
                    'metadata':{'modbus':{ 'addr':'40003', 'blockname':'holdingreg',
                                    'blocktype':3, 'datatype':'int'},
                                'dnp3': {} }
            } ],
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
                'baudrate' : 19200,
               }
        ],
        'icsifaces' : []# No ICS interface for this vdev
} #End vdev0

config['vdevs']['slave'] = {
        'name':'slave',
        'id' : 1,
        'points' : [
            {'name':'pump',  'typ':2, 'value':False, 
                    'metadata':{'modbus':{ 'addr':'10', 'blockname':'coil',
                                    'blocktype':1},
                                'dnp3': {} }
            }, {'name':'valve', 'typ':2, 'value':False, 
                    'metadata':{'modbus':{ 'addr':'11', 'blockname':'coil',
                                    'blocktype':1},
                                'dnp3': {} }
            }, {'name':'pressure','typ':1, 'value':17.0, 
                    'metadata':{'modbus':{ 'addr':'30002', 'blockname':'inputreg',
                                    'blocktype':4, 'datatype':'float'},
                                'dnp3': {} }
            }, {'name':'setpoint',  'typ':0, 'value':15.0, 
                    'metadata':{'modbus':{ 'addr':'40003', 'blockname':'holdingreg',
                                    'blocktype':3, 'datatype':'float'},
                                'dnp3': {} }
            } ],
        'timeout' : .1, #timeout for logic loop
        'simiface' : {
            #These values should correspond to those in config['simiface']
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
                'baudrate' : 19200,
                'id' : 1,
               }
       ],
       'clientifaces' : []
}#End vdev2


config.write()


