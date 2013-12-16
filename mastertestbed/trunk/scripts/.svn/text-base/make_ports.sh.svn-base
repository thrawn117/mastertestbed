#!/bin/bash

#This file creates the necessary logged serial ports for the simulation to run.
cd ..
#For normal use
symlinks="./pty/0 ./pty/1"
protolibs/portlogger.py -n 2 --force_symlinks $symlinks

#For radio use
#protolibs/portlogger.py -n 1 -p /dev/ttyUSB0 -b 9600 --force_symlinks ./pty/0 &
#protolibs/portlogger.py -n 1 -p /dev/ttyUSB2 -b 9600 --force_symlinks ./pty/1 &
