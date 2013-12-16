#!/bin/bash

#script to start the tank simulation

term=gnome-terminal
#system=rtupipe
#system=rtuwater
system=tcppipe
logfile=$1

sudo true #Get the user to provide sudo power (necessary to open port 502)
cd ..
#Create ports
symlinks="pty/0 pty/1 pty/2"

#gnome-terminal -x /bin/bash -c "protolibs/portlogger.py -r -n 2 -b 9600 -e --force_symlinks $symlinks -l $logfile; exec bash"
gnome-terminal -x /bin/bash -c "protolibs/portlogger.py -r -n 2 -b 9600 -e --force_symlinks $symlinks -l $logfile; exec bash"
sleep .2

#Start attack scripts (optional)
#gnome-terminal -x /bin/bash -c "attacks/rtu_dos_inject -inport pty/2; exec bash"
gnome-terminal -x /bin/bash -c "watch wc -l $logfile"

#Start simulator 
gnome-terminal -x /bin/bash -c "python simulator.py -s $system; exec bash"

#Start vdevs
gnome-terminal -x /bin/bash -c "python vdev.py -s $system -d slave; exec bash" &
sleep 1
gnome-terminal -x /bin/bash -c "python vdev.py -s $system -d master; exec bash" & 

