#!/usr/bin/env python

"""
Script to generate a plot from a simulator output file of a vdev variable
Brad Reaves
May 2011
"""

from pylab import *
import sys

from IPython.Shell import IPShellEmbed
ipshell = IPShellEmbed()

try:
    filename = sys.argv[1]
except IndexError:
    print "ERROR: No file name\n", "Usage: python level_plotter.py FILENAME"
    sys.exit(-1)

times = []
var_list =[]
with open(filename,'r') as f:
    for line in f:
        time, pressure = line.split(' : ')
        times.append(time)
        var_list.append(pressure)

#normalize times
zero = float(times[0])
times = [float(t) - zero for t in times]
var_list = [float(v) for v in var_list]

#Start plotting
ax = axes()
ax.set_xlabel('Seconds since start of simulation')
ax.set_ylabel('Level (PSI)')

plot(times, var_list)
show()
ipshell()

