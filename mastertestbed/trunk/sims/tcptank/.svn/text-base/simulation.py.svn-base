#!/usr/bin/env python

import copy
import logging, optparse
import threading, Queue 
import time  

from configobj import ConfigObj

from protolibs import ifaces
#import protolibs.ifaces as ifaces #this relies on a symlink back to protolibs

"""
@author Brad Reaves
@version 0.1
February 2011
@license GPL2

This module defines the necessary functions, constants, and variables to
simulate a simple fluid tank consisting of a single output valve and
single input pump governed by a single virtual device and monitored by a second
virtual device.
"""

#--------------- Parse Configuration Options ----------------

#Required Items:
#---Communication interface
    #Type (udp, tcp, pipes, serial)
    #Setup options (ports, filenames, destination addresses, etc)
#---Virtual Device Setup

#Simulation Details (constants, etc)
#   physical constants
#   simulation time
#   variables and default values
class Simulation():
    """This class obtains simulation information from a configuration file,
        sets up a simulation state, provides a method to step the simulation
        forward in time.
     """
    def readConfig(self):
        """Opens and parses the configuration file in the local directory. The
            results are available in self.config ."""
        ##Open ConfigFile
        self.config=ConfigObj(infile='sims/tcptank/config', unrepr=True)#MAKE READ ONLY
        """
        self.config = dict()
        self.config['iface']={
            'typ':'udp', 
            'sport':9912, #9912-9949 are unassigned
            'recipients' : [('127.0.0.1',9913)],
            'timeout' : .1 
        }
        self.config['sim_state']={
            'simtime' : 0, #time in the simulation
            'pump' : True, #Whether pump is on or off
            'valve' : False, #Whether valve is open or not
            'pressure' : 0 #Current pressure in the tank (psi)
        }
        self.config['sim_constants']={
            'valve_rate' : -1 ,#psi/sec
            'pump_rate' : 2 #psi/sec
        }
        """
    def __init__(self):
        """Constructor for the simulation class. Calls readConfig() and 
        creates an initial simulation state."""
        self.readConfig()
        #/define/ comm interface type (based on config)
        ifaceinfo = self.config['simiface']
        ifacetype = getattr(ifaces, ifaceinfo['typ'])
        self.interface=ifacetype(**ifaceinfo)
        self.interface.initialize()

        #initialize variables in the procVarDictionary
        #   use a deep copy so that we can't change the config dictionary
        self.simState = copy.deepcopy(self.config['sim_state'])
        self.simState['simtime'] = time.time()

    def step(self, upto=None):
        """Function that modifies the simulation state from the curent
        simulation state to the time given in parameter upto.
        
        @param upto Time to simulate from simState['simtime'] to upto.
                    upto should be a float in the format of the time.time()
                    call -- i.e. unix time. If upto is None, the current time 
                    will be used.
        """
        if upto is None:
            upto = time.time()
        deltaT = upto - self.simState['simtime'] 
        if deltaT < 0:
            #This happens when we receive an update packet dated from before the
            #   current simulation time. In that case, we return to let the
            #   changes be applied, and then the simulation will step to the
            #   current time, and all will be well. In the worst case, changes
            #   should only be 100 ms old.
            return
        consts = self.config['sim_constants']
        
        #We're doing a simple model that's linear over time. Non-linear models
        #   may require iterating over fractions deltaT to be accurate.
        #   Numerical techniques from Sage or SciPy may be required for advanced
        #   models.

        if self.simState['pump']:
            pumpContribution = deltaT *  consts['pump_rate']
        else:
            pumpContribution = 0

        if self.simState['valve']:
            valveContribution = deltaT *  consts['valve_rate']
        else:
            valveContribution = 0

        self.simState['pressure'] = self.simState['pressure'] +( 
            pumpContribution + valveContribution)

        #Negative pressures are impossible
        if self.simState['pressure'] < 0: self.simState['pressure'] = 0

        self.simState['simtime'] = upto

