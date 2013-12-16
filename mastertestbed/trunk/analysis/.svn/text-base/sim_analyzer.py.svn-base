#!/usr/bin/env python
# vim: set tw=80:
"""
sim_analyzer.py
Brad Reaves
June 2011

This script extracts process information from packet traces to compare the 
effectiveness of virtual testbed process simulations to their lab counterparts.
"""

from analyzer import Trace, MSU_CSV_Trace, Packet
import struct
from pprint import pprint
import numpy


class ProcessValues(object):
    """Creates a list of values based on packets in a trace; values are
    obtained by running op on the packet list."""
    def __init__(self, trace, op, name=None):
        self.trace = trace
        self.op = op 
        self.name = name 
        self.times, self.values  = self.op(self.trace.packets) 
        self.net_times = [t-self.times[0] for t in self.times]

    def linear_fit(self, start_index=0, stop_index=-1):
        """Performs a linear fit of the data from start_index to stop_index.
        @returns a tuple (slope, y-intercept) for slope-intercept equation of a
        line
        """
        dx = self.times[stop_index] - self.times[start_index]
        dy = self.values[stop_index] - self.values[start_index]
        m = float(dy)/dx
        b = self.values[start_index] - m * self.times[start_index]
        return m, b

    def write_csv(self, filename):
        """Writes a file of time, value lines in csv format for external
        editing"""
        with open(filename, 'w') as f:
            for time, value in zip(self.net_times,self.values):
                s = '%0.6f,%0.6f' % (time, value) + '\n'
                f.write(s)

    @staticmethod
    def polyfit(x, y, degree):
        #Borrowed and extended from http://stackoverflow.com/questions/893657/
        results = {}
        coeffs = numpy.polyfit(x, y, degree)

        # Polynomial Coefficients
        results['polynomial'] = numpy.poly1d(coeffs)
        results['derivative'] = results['polynomial'].deriv()

        # r-squared
        p = numpy.poly1d(coeffs)
        # fit values, and mean
        yhat = [p(z) for z in x]
        ybar = sum(y)/len(y)
        ssreg = sum([ (yihat - ybar)**2 for yihat in yhat])
        sstot = sum([ (yi - ybar)**2 for yi in y])
        results['determination'] = ssreg / sstot
        return results

class Comparison(object):
    """Comparison objects take two process values and provides tools for
    comparing the differences"""
    
    def __init__(self, trace1, trace2, xlabel='', ylabel=''):
        self.trace1 = trace1
        self.trace2 = trace2
        self.proc_val1 = ProcessValues(trace1, self.op)
        self.proc_val2 = ProcessValues(trace2, self.op)
        self.xlabel = xlabel 
        self.ylabel = ylabel

    def plot(self, _xlabel='', _ylabel='',_title=''):
        """Creates a plot of the process values"""
        from pylab import plot, xlabel, ylabel, title, show, legend

        #First plot
        plot(self.proc_val1.net_times, self.proc_val1.values, 'r', 
              label=self.trace1.name or 'Trace1')
        plot(self.proc_val2.net_times, self.proc_val2.values, 'b', 
              label=self.trace2.name or 'Trace2')
        xlabel(_xlabel or self.xlabel)
        ylabel(_ylabel or self.ylabel)
        title(_title)
        #legend(loc='upper left')
        legend(loc='lower center')
        show()

class GroundTankLevelComparison(Comparison):
    def __init__(self, *args, **kwds):
        self.op = self.GroundTankLevel
        super(GroundTankLevelComparison, self).__init__(*args, **kwds)
        self.xlabel = 'Time (s)'
        self.ylabel = 'Percent Full'

    @staticmethod
    def GroundTankLevel(packets):
        check = lambda d: ord(d[1]) == 03 and len(d)==25
        get_value = lambda d: struct.unpack('>f',d[17:21])[0]
        values = []  
        times = []
        for time, data in [(p.timestamp, p.data) for p in packets]:
            if check(data):
                values.append(get_value(data))
                times.append(time)
        return times, values

class PipelinePressureComparison(Comparison):
    def __init__(self, *args, **kwds):
        self.op = self.PipePressure
        super(PipelinePressureComparison, self).__init__(*args, **kwds)
        self.xlabel = 'Time (s)'
        self.ylabel = 'Pressure (PSI)'

    @staticmethod
    def PipePressure(packets):
        check = lambda d: ord(d[1]) == 03 and len(d)==23
        get_value = lambda d: struct.unpack('>f',d[17:21])[0]
        values = []
        times = []
        for time, data in [(p.timestamp, p.data) for p in packets]:
            if check(data):
                values.append(get_value(data))
                times.append(time)
        return times, values

def main():
    #trace1 = MSU_CSV_Trace('traces/water_lab/process/water_f_to_e', name='Laboratory System')
    #trace2 = MSU_CSV_Trace('/tmp/water_efe', 'Virtual System')
    #comparison = GroundTankLevelComparison(trace1, trace2)
    #trace1 = MSU_CSV_Trace('traces/pipeline_lab/process/pipe_man_top_pressure', name='Laboratory System')
    trace1 = MSU_CSV_Trace('traces/pipeline_lab/process/pipe_off_to_auto', name='Laboratory System')
    trace1 = MSU_CSV_Trace('traces/pipeline_lab/process/pipe_man_0_to_equib', name='Laboratory System')
    trace2 = MSU_CSV_Trace('traces/pipeline_sim/process/man_0_to_equib', 'Virtual System')
    comparison = PipelinePressureComparison(trace1, trace2)

    ##Interface
    comparison_list =[i for i in locals() if  'comparison' in i]
    print "Trace 1(red): \t", trace1.filename
    print "Trace 2(blue): \t", trace2.filename
    pprint(comparison_list)
    from pylab import *
    import numpy as np
    from IPython.Shell import IPShellEmbed
    ipshell = IPShellEmbed( banner = """Comparisons available in comparison_list""")
    ipshell() 

if __name__ == '__main__':
    main()
