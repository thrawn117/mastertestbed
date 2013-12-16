#!/usr/bin/env python

"""
@author Brad Reaves
@version 0.1
February 2011
License: GPL2

This module defines functions containing the control logic for the tank
virtual logic.
"""

def slave(points, *args, **kwds):
    if points['pressure'].get() > points['setpoint'].get() + 10:
        points['valve'].set(True)
        points['pump'].set(False)
    if points['pressure'].get() > points['setpoint'].get() + 1:
        points['valve'].set(True)
        points['pump'].set(True)
    if points['pressure'].get() < points['setpoint'].get() - 1:
        points['valve'].set(False)
        points['pump'].set(True)

def master(points, clients, *args,**kwds):
    """ Code for the master device in this system. 
    @param clients dictionary of ICS client objects indexed by device"""
    from random import randint
    #from ..protolibs import ics_clients #This doesn't do anything

    #Static function variable "read" used to determine if we are reading or 
    #writing points this call. If this is the first time the master code is run
    #we read
    master.read = True
    #master.read = getattr(master, "read", True)

    client = clients['slave']
    if master.read:
        ##Read points
        reply = client.readPoints(['pressure', 'setpoint', 'valve', 
                                                'pump'])
        
        ##Process points
        points['pressure'].set(reply[0])
        points['setpoint'].set(reply[1])
        points['valve'].set(reply[2])
        points['pump'].set(reply[3])
        
        master.read = False
    else: #We write something
        #client.writePoints(('setpoint', randint(5,15)))
        master.read = True
