#!/bin/bash

baud=9600
port1=/dev/ttyUSB0
port2=/dev/ttyUSB2
symlink1=./pty/0
symlink2=./pty/0sf
symlink3=./pty/1
symlink4=./pty/1sf
logfile=$1
#basefile=/home/bgr39/tbcode/analysis/traces/water_lab/

cd ..
gnome-terminal -x /bin/bash -c "protolibs/portlogger.py -n 2 -b $baud -e  --force_symlinks $symlink1 $symlink2 -l $basefile$logfile.master; exec /bin/bash"
gnome-terminal -x /bin/bash -c "protolibs/portlogger.py -n 2 -b $baud -e  --force_symlinks $symlink3 $symlink4 -l $basefile$logfile.slave; exec /bin/bash"

#Storeforward
#gnome-terminal -x /bin/bash -c "protolibs/portlogger.py -n 0 -p $symlink2 -p $symlink4 -b $baud; exec /bin/bash"




