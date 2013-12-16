#!/bin/bash

baud=9600
port1=/dev/ttyUSB0
port2=/dev/ttyUSB2
symlink1=./pty/0
symlink2=./pty/1
logfile=$1
#basefile=/home/bgr39/tbcode/analysis/traces/water_lab/

cd ..
gnome-terminal -x /bin/bash -c "protolibs/portlogger.py -n 1 -b $baud -p $port1 --force_symlinks $symlink1 -l $basefile$logfile.master; exec bash"
gnome-terminal -x /bin/bash -c "protolibs/portlogger.py -n 1 -b $baud -p $port2 --force_symlinks $symlink2 -l $basefile$logfile.slave; exec bash"

gnome-terminal -x /bin/bash -c "watch 'wc -l $basefile$logfile.slave; wc -l $basefile$logfile.master';exec bash" 




