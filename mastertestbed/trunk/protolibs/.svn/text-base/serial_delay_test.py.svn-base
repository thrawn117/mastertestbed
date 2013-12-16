#!/usr/bin/env python
# vim: tw=80:
"""
Brad Reaves
serial_delay_test.py
May 2011
GPL v2

This code tests the one-way delay time for a serial port transmission.
Processes are used instead of threads so that they will run in parallel and
not be subject to Python's GIL limitations.
"""

import os, time,struct
from serial import Serial 

SAMPLES = 100

def receiver(slave):
    records = []
    while len(records) < SAMPLES:
        data = slave.read(8)
        records.append( (time.time(), data) )

    deltas = []
    for rec in records:
        sent_time = struct.unpack('>d',rec[1])[0]
        delta = rec[0] - sent_time 
        deltas.append(delta)
    
    average = sum(deltas)/float(len(deltas))
    #print "Output: ", ','.join([str(d) for d in deltas])
    print "Average delay: ", average
    print "Minimum delay: ", min(deltas)
    print "Maximum delay: ", max(deltas)

def sender(port1, port2):
    master = Serial(port1, baudrate=9600)
    slave = Serial(port2, baudrate=9600)

    deltas = None
    pid = os.fork() 
    if pid == 0:
        deltas = receiver(slave)
    else: 
        time.sleep(.1)
        for i in range(SAMPLES):
            master.write(struct.pack('>d',time.time()))
            time.sleep(.1)
    os.waitpid(pid,0) #wait on children to complete

    return 0

if __name__ == '__main__':
    sender('../pty/0', '../pty/1')
    #sender('/dev/ttyUSB0', '/dev/ttyUSB2')
    #sender('/dev/ttyUSB0', '../pty/1')
    
