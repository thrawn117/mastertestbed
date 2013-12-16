#!/usr/bin/env python


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

import copy
import logging, optparse
import threading, Queue 
import time  
import random

from math import sqrt, log
from configobj import ConfigObj

from protolibs import ifaces
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
        self.config=ConfigObj(infile='sims/rtupipe/config', unrepr=True)#NOTE
        if not self.config:
            raise Exception("Config file empty or non-existent")

    def __init__(self):
        """Constructor for the simulation class. Calls readConfig() and 
        creates an initial simulation state."""
        self.config = None
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
        # This is for variables that we don't want sent to the vdevs, but need 
        #       to remember step to step
        self.simInternals = {'pressurePSI':0} 

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
        simState = self.simState #create a local alias for brevity.
        simInternals = self.simInternals #create a local alias for brevity.

        
        #Pump only:
        # Provides pressure given an amount of time the pump has been running
        pump_t2p = lambda t: 2.00522251015311 * t ** .748304381920375
        # Provides a "time running" value given a pressure
        pump_p2t = lambda p: 0.39464 * p**1.3363545960183984

        #Valve only:
        # Provides pressure given an amount of time the valve has been open
        valve_t2p = lambda t: .098*t**2 -4.439*t+49.83
        # Provides a "time open" value given a pressure
        valve_p2t = lambda p: (4439-sqrt(392000*p + 171361) )/196.0

        #Pump and valve:
        pv_lesser_p2t = lambda p: 18.4324 - .0000106047 * sqrt(3.08507e12 - 4.21714e11*p)
        pv_lesser_t2p = lambda t: t * (.777319 - .0210857 * t) + .151637
        pv_greater_delta = lambda p: -1.10353 * log(0.125097*p)

        #Use a non-linear model for the pump based on measurements
        #of pressure taken per unit time

        if simState['PumpRunCmd'] and not simState['SolOpenCmd']:
            current_t = pump_p2t(simInternals['pressurePSI'])
            simInternals['pressurePSI'] = pump_t2p(current_t + deltaT)
        elif simState['SolOpenCmd'] and not simState['PumpRunCmd']:
            current_t = valve_p2t(simInternals['pressurePSI'])
            simInternals['pressurePSI'] = valve_t2p(current_t + deltaT)
        elif simState['SolOpenCmd'] and simState['PumpRunCmd']:
            ##Use a piecewise model because the pressure will converge
            ## to around 7.8 empirically, and 7.3 mathematically
            if simInternals['pressurePSI'] < 7.31:
                current_t = pv_lesser_p2t(simInternals['pressurePSI'])
                calc_pressure = pv_lesser_t2p(current_t + deltaT)
                #p2t is only defined on (0, 7.315..), so if we
                #are close to this number, we ensure that we stay in the 
                #proper domain while adding some perturbation so we don't
                # get stuck with repeating values
                if calc_pressure > 7.3: 
                    calc_pressure = 7.3 + random.uniform(-.02, .01)
                simInternals['pressurePSI'] = calc_pressure
            else: #We are decreasing to the proper value
                #Instead of the other approaches, here we use an approximated
                #derivative to find the next pressure:
                dPdt = pv_greater_delta(simInternals['pressurePSI'])
                simInternals['pressurePSI'] = (simInternals['pressurePSI']
                        + dPdt * deltaT)

        #Negative pressures are impossible.
        if simInternals['pressurePSI'] < 0: 
            simInternals['pressurePSI'] = 0

        PSItoAnalog = lambda psi: (87 * psi) + 3131 #Obtained from ladder logic
        simState['PressureRawInputReg'] = PSItoAnalog(simInternals['pressurePSI'])

        simState['simtime'] = upto
        self.simState = simState #Put the local variable back, just in case
        self.simInternals = simInternals #Put the local variable back, just in case

