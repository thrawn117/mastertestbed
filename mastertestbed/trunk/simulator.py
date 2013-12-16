#!/usr/bin/env python

import logging, ConfigParser, optparse
import threading, Queue, time, socket, errno, os
from sys import stdin
from select import select

import protolibs.ifaces as ifaces
import simplejson as json
from optparse import OptionParser

"""
@author Brad Reaves
February 2011
@version 0.1
@license GPL2
"""


#---------------- Parse Command Line Options ----------------

#--------------- Set up logging ---------------------------



#--------------- Class definitions -------------------------
class procvar():
    """@brief This class is used to maintain process variables during the simulation
       @deprecated Using a simpler simulator design
    """
    INTERNAL = 'INTERNAL'
    OUTPUT = 'OUTPUT'
    INPUT = 'INPUT'
    def  __init__(self, currentValue = None, nextValue = None, 
                        whenToUpdate=None, updated=False, varType = 'INTERNAL'):
        """Declares and initializes variables for the procvar object
           @deprecated
           @param currentValue The present value in the simulation.
           @param nextValue If an update needs to be simulated, this
                    is the value the process variable will become at time
                    <code>updateTime</code>
           @param whenToUpdate If the value of this variable will change due to 
                    an outside update, this is the simulation time when the 
                    update should occur.
           @param varType Should be a string indicating if the type is INTERNAL,
                    an INPUT, or an OUTPUT. Internal variables are only used by
                    the simulator. Inputs are set by the virtual devices.
                    Outputs are set by the simulator and read by the virtual 
                    devices. If a variable type is an OUTPUT,
                    and if the value changes during a simulation step 
                    (updated == True), the value
                    will be sent to all virtual devices at the end of the 
                    simulation step. Acceptible values are procvar.INTERNAL,
                    procvar.OUTPUT, and procvar.INPUT .
           @param updated Set True if an output value changed during the
                            simulation.

        """
        self.currentValue = currentValue
        self.nextValue = nextValue
        self.whenToUpdate = whenToUpdate
        self.varType = varType
        self.updated = updated

    



#--------------- Function Definitions ---------------------

def processUpdate(update):
    """This function takes an update packet, converts JSON into Python data,
    and then applies all of the listed changes to the process variables.
    
    @param update This parameter is a JSON message received from the interface
    @returns A dictionary of the message contents
    """
    update = json.loads(update)
    #TODO: Handle case where there's no updatetime
    return update

def applyUpdate(update, state):
    """This function takes a dictionary corresponding to an update and 
       if the key corresponds to a state variable, the state variable is set to
       the value in the update.

       @param update Dictionary derived from an update message.
       @param state The state dictionary for the process simulation
       """
    for var in update.keys():
        if var in state.keys():
            state[var] = update[var]
        elif var == "updatetime":
            continue
        else:
            #log the error
            print "Unknown process variable in update:: %s : %s" % \
                  ( str(var), str(update[var]) )
       

def compileUpdate(state):
    """This function creates a JSON string of all state variables.

       @param state The dictionary of process state variables.
       @returns A string containing the JSON representation of the
                    state variables.
       """
    update = json.dumps(state) 
    return update


#------------- "Main" code --------------------------------
def main(system, sim_output_filename ):
    """This function contains the main logic of the simulator"""
    ##Import the simulation given in the commandline option:
    exec 'import sims.'+system+'.simulation as simmodule'
    procsim = simmodule.Simulation()

    #Open and Write header to simulation output file
    simOutputFile = open(sim_output_filename, 'w', 1)
    simOutputFile.write(','.join( sorted(procsim.simState.keys()) ) + '\n' )

    #Initialize comm medium (socket, pipe, etc)
    #interface = ifaces.virtual()
    interface = procsim.interface

    print "Running simulation [%s]. Type 'quit' to stop" % system
    
    loop = True
    while loop:
        ##Blocking receive. The timeout on the iface basically sets the
        ##  simulation maximum wait between simulation runs.
        updateMsg = interface.getMessage(block=True)

        while updateMsg is not None:
            ##Process Update 
            try:
                update=processUpdate(updateMsg)
            except Exception: #Exceptions are thrown if the msg was not valid
                #TODO: Be more explicit about which exceptions are caught
                #TODO: Log here
                updateMsg=interface.getMessage(block=False)
                continue
            ##Simulate up to time in update
            procsim.step(update['updatetime'])
            ##Apply update to input variables
            applyUpdate(update, procsim.simState)
            ##Check for new update (non-blocking)
            updateMsg=interface.getMessage(block=False)

        ##Simulate until present time
        procsim.step()
        #procsim.step(time.time())

        ##Compile update to go out
        update=compileUpdate(procsim.simState)
        ##Push out update
        interface.sendMessage(update)

        ##Log the update
        outputfileline = ','.join( [str(procsim.simState[k] )
                                for k in sorted(procsim.simState.keys()) ] )
        simOutputFile.write( outputfileline + '\n' )
        
        #Wait a fraction of time so the sim isn't constantly looping
        #TODO: Parameterize this wait
        time.sleep(.05)

        ##User interface:
        #check if user typed something:
        rd, wt, ex = select([stdin], [],[], 0) #Nonblocking
        if rd: #User typed something
            user_input = stdin.readline()
            if 'quit' in user_input:
                loop = False
    
    #While is done
    simOutputFile.close()


    
if __name__ == "__main__":
    ##Obtain simulation name as command line option
    programDescription = """This program implements an ICS simulation."""
    parser = OptionParser(description=programDescription)
    parser.add_option('-s', '--system', help="""Name of the system being simulated.\
            This name determines which configuration file is used.""", 
             action='store', default = 'tcptank')
    parser.add_option('-l', '--logfile', help="Name of the logfile where """ +
             "simulation variables are written. ", 
             action='store', default = '/tmp/simulation.csv')
    (opts, args) = parser.parse_args()
    system = opts.system
    ##Create a CSV file to record the sim state after each update. This is mostly
    ##      for debugging. The bufsize=1 indicates the file should be line buffered
    logfile_name = opts.logfile
    main(system, logfile_name)
