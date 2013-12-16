#!/usr/bin/env python
# vim: set tw=80:
"""
analyzer.py
Brad Reaves
May 2011
License: GPL v2

This script is used to analyze and measure similarity between two or more 
packet traces.
"""

import unittest
import math
from modbus_tk import utils as modbus_utils

class Trace(object):
    """Class that reads and stores information from traffic trace files.
    Child classes inherit from Trace and implement their own read_trace methods
    for particular types of trace file, like PCap, Snoop, or custom CSVs"""
    def __init__ (self, filename, name = '', do_not_read=False):
        """Populates a trace object with packets from the trace given in 
            parameter filename.
            @param name Name to use when plotting values from this trace
            @oaram filename Filename of trace to read packets from.
            @param do_not_read Set true to create an instance of a trace object
                                that does not attempt to read itself. Used for 
                                creating new arbitrary Trace objects.
            """
        self.filename = filename
        self.name = name

        self.packets = [] #Holds packet objects; filled by self.read_trace()
        self.header = '' #Holds tracefile header info
        if not do_not_read:
            self.read_trace()

    def print_info(self):
        """Return a tuple of the amount of time the trace covers, number of
        packets, and other interesting information"""
        print "Filename: ", self.filename
        print "Number of packets: ", len(self.packets)
        print "Time covered by trace: ", (self.packets[-1].timestamp
                                            -  self.packets[0].timestamp)


    def read_trace(self):
        """Should be implemented by child classes"""
        raise NotImplementedError("read_trace not implemented in the Trace"
                                  + " base class. Use a child class")
    @staticmethod
    def combine_traces(trace1, trace2, source1, source2):
        """This function takes two traces of the same event from split logs 
            (logs that capture only one side of the traffic) and creates one
            combined trace.
            @param trace1 A trace to combine
            @param trace2 A trace to combine 
            @param source1 The source in trace1 to copy packets from
            @param source1 The source in trace2 to copy packets from
            @returns A new trace object of the same type as trace1
        """
        trace1pkts = [pkt for pkt in trace1.packets if pkt.source == source1]
        trace2pkts = [pkt for pkt in trace2.packets if pkt.source == source2]
        trace_pkts = sorted(trace1pkts+ trace2pkts, 
                                key = lambda p: p.timestamp)
        
        header = trace1.header or trace2.header
        t = trace1.__class__('', do_not_read=True)
        t.header = header
        t.packets = trace_pkts
        return t

class MSU_CSV_Trace(Trace):
    """Reads and stores serial capture traces in Mississippi State University's 
        custom CSV format."""
    separator = ' : '
    def read_trace(self):
        with open(self.filename, 'r') as trace_file:
            self.header = ''.join([trace_file.readline() for i in range(4)])
            for line in trace_file:
                timestamp, source, data = line.split(self.separator)
                data = self.convert_data(data)
                pkt = Packet(source, None, float(timestamp), data, line)
                self.packets.append(pkt)

    def convert_data(self, data):
        """Used to covert the dot-separated ASCII-encoded packets into a 
            binary format
        @param data Original data string from the record
        @returns A new string of the original data converted into binary form"""
        byte_separator = '.'
        #Use strip() to remove newline, split to separate into byte strings
        data_bytes = data.strip().split(byte_separator)
        new_data = ''.join([chr(int(byte,16)) for byte in data_bytes])
        return new_data
    
    def write_trace(self, filename = None):
        filename = filename or self.filename
        if not filename:
            raise Exception('No filename available for trace')
        with open(filename, 'w') as f:
            f.write(self.header)
            for pkt in sorted(self.packets, key = lambda p: p.timestamp):
                f.write(pkt.record)

class PCAP_Trace(Trace):
    def read_trace(self):
        raise NotImplementedError("PCAP Traces not supported yet") #TODO
        
class Packet(object):
    """Holds individual packet data read from traces. May be subclassed to 
       parse protocol-level data"""
    def __init__(self, source, destination, timestamp, data, record):
        """Initializes a packet object.
        @param source String representing the source of the packet
        @param destination String representing the destination of the packet
        @param timestamp Timestamp of this packet
        @param data The contents of the packet as recorded in the trace (string)
        @param record String representing the complete, encoded representation
                        of the packet from the trace file
        """
        self.source = source
        self.destination = destination
        self.timestamp = timestamp
        self.data = data
        self.record = record
        self.parse_data()

    def parse_data(self):
        """Used to parse data strings into fields or convert data.
            Examples include extracting
            flags or checksums. Should be defined in subclasses"""
        pass

    def __repr__(self):
        return '<Packet: {%s}>' % self.record

class Metric(object):
    """Base class for implementing similarity metrics based on comparing two
        traces. Child classes implement the "compute_similarity" method.
        Child classes may override the constructor and delay calling compute
        similarity and compute_error by setting calc_similarity to False"""
    name = 'Base Metric' #Used for pretty printing and report generation
    def __init__(self, trace1, trace2, calc_similarity = True):
        self.trace1 = trace1
        self.trace2 = trace2
        self.score1 = None
        self.score2 = None
        self.xlabel = 'Normalized measurement number'
        self.similarity = self.compute_similarity() if calc_similarity else None
        self.compute_error() if calc_similarity else None

    def compute_error(self):
        """Computes error statistics between the two metrics
            Note: Assumes Trace1 is the canonical trace!
        """
        if not self.score1 or not self.score2:
            self.error = None
            self.percent_error = None
            self.average_error = None
            return
        error = self.diff_lists(self.score1, self.score2)
        if hasattr(error, '__iter__'):
            avg_err = sum(error)/float(len(error))
        else:
            avg_err = error
        if hasattr(self.score1, '__iter__'):
            avg_val = sum(self.score1)/float(len(self.score1))
            avg_val2 = sum(self.score2)/float(len(self.score2))
        else:
            avg_val = self.score1
            avg_val2 = self.score2
        p_err = (avg_val2-avg_val)/avg_val if avg_val else float('nan')
        self.average_error = avg_err
        self.percent_error = p_err 
        self.error = error
        
    def compute_similarity(self):
        """Method called to provide a single floating-point similarity index
            on [0,1] of the two traces based upon some characteristic of the
            traces.
            @returns A float on [0,1] indicating the degree of similarity of the
                    two traces.
        """
        raise NotImplementedError("Use a child class of the Metric object")
    def compute_metric(self, trace):
        """Method to compute a metric for a given trace. The result of this may
        be a scalar, a discrete set, or a continuous set of data derived from
        the trace."""
        raise NotImplementedError("Use a child class of the Metric object")
    @staticmethod
    def scalar_similarity(score1, score2):
        """Static method used to compute the similarity of two traces
        from scalar scores computed on each one independently.
        @returns A floating point similarity score on [0,1]
        """
        if score1 or score2: #Make sure we aren't about to div by 0
            similarity = 1 - math.fabs(score1 - score2)/(score1+score2)
        else:
            similarity = 1 #If both values are zero, the similarity is 1
        return similarity

    @staticmethod
    def discrete_similarity(list1, list2):
        """Static method used to compute the similarity of two traces from 
            lists of characteristics compiled from each trace. This method does
            no scaling on the data, so scaling or interpolation must be done on
            the lists before calling this funtion. Uses zip on both lists, so
            truncation of lists may occur.
        @returns A floating point similarity score on [0,1]"""
        summand = lambda x1, x2: math.fabs(x1-x2)/(x1+x2) if x1 or x2 else 0
        pairs = zip(list1, list2)
        sigma = sum([summand(*pair) for pair in pairs])
        similarity = 1 - sigma/len(pairs)
        return similarity

    @staticmethod
    def ordered_continuous_similarity():
        raise NotImplementedError()

    @staticmethod
    def compress_list(large_array, small_array):
        """Makes two lists the same size by sampling the larger at intervals
        defined by the smaller. This is the same algorithm used by sorted
        continuous similarity below"""
        ## Determine which is the larger and smaller lists
        #large_array = list1 if len(list1)>=len(list2) else list2
        #small_array = list1 if len(list1)<len(list2) else list2
        #large_array = sorted(large_array)
        #small_array = sorted(small_array)

        sampled_array = []
        for small_ary_cnt, small_ary_item in enumerate(small_array):
            if len(small_array)>1:
                small_ary_rel_cnt = (small_ary_cnt * 1.0/(len(small_array) - 1))
            else: 
                small_ary_rel_cnt = 0
            # Compute larger array from the smaller array
            large_ary_cnt = round(small_ary_rel_cnt*(len(large_array)-1), 5)
            large_ary_cnt = round(large_ary_cnt, 5) #Truncate to 5 decimals

            #If the index is an int, only one value is provided, otherwise 2
            large_ary_item = large_array[int(math.floor(large_ary_cnt)) :
                                           int(math.ceil(large_ary_cnt)+1)]
            #Compute the average of the values
            large_ary_item = math.fsum(large_ary_item) / len(large_ary_item)
            sampled_array.append(large_ary_item)
        return sampled_array


    @staticmethod
    def sorted_continuous_similarity(list1, list2):
        """This test is useful for comparing data that isn't ordered (i.e. not 
        (x,y)
        pairs. This method is taken from nonkeyedCompare.c, provided by Terry
        Brugger."""
        scalar_similarity = lambda x1, x2: 1 - math.fabs(x1-x2)/(x1+x2)
        ## Determine which is the larger and smaller lists
        large_array = list1 if len(list1)>=len(list2) else list2
        small_array = list1 if len(list1)<len(list2) else list2
        large_array = sorted(large_array)
        small_array = sorted(small_array)

        ## Iterate over smaller array. Find the corresponding element in the
        ## larger array, and compute a similarity score for the numbers. If the
        ## corresponding scaled index is not an integer, take the average of the
        ## two elements. Add the calculated similarity to the total similarity
        total_similarity = 0
        for small_ary_cnt, small_ary_item in enumerate(small_array):
            if len(small_array)>1:
                small_ary_rel_cnt = (small_ary_cnt * 1.0/(len(small_array) - 1))
            else: 
                small_ary_rel_cnt = 0
            # Compute larger array from the smaller array
            large_ary_cnt = round(small_ary_rel_cnt*(len(large_array)-1), 5)
            large_ary_cnt = round(large_ary_cnt, 5) #Truncate to 5 decimals

            #If the index is an int, only one value is provided, otherwise 2
            large_ary_item = large_array[int(math.floor(large_ary_cnt)) :
                                           int(math.ceil(large_ary_cnt)+1)]
            #Compute the average of the values
            large_ary_item = math.fsum(large_ary_item) / len(large_ary_item)
            if small_ary_item and large_ary_item:
                sim = scalar_similarity(small_ary_item, large_ary_item)
            else:
                sim = 1
            total_similarity += sim
        return total_similarity/len(small_array)
                
    @staticmethod
    def chi_square_confidence(list1, list2):
        """Static method used to compute the chi-square fit of one distribution
        to another. This method returns a p-value, which indicates the
        probability that the results in list2 could have been sampled from 
        list1.
        @param list1 Base distribution
        @param list2 Empirical distribution
        @returns A floating point p-value on [0,1]"""
        from scipy.stats import chisquare
        from numpy import array
        x2, p = chisquare(array(list2), array(list1))
        return p

    @staticmethod
    def diff_lists(list1, list2):
        """Takes two lists, samples the larger to be the same size as the smaller,
           sorts, then produces a list of the differences of each list element."""
        from random import sample
        from math import fabs

        if not hasattr(list1, '__iter__') and not hasattr(list2,'__iter__'):
            return list1-list2 #We've got scalar values

        longer = list1 if len(list1) >= len(list2) else list2
        shorter = list1 if len(list1) < len(list2) else list2

        #sampled = sorted(sample(longer, len(shorter))) #Sampling > interpolating
        sampled = Metric.compress_list(longer, shorter)

        diff = []
        for t in zip(sampled, shorter):
            #diff.append(fabs(t[1]-t[0]))
            diff.append(t[0]-t[1])
        return diff

    def __str__(self):
        return str(self.similarity)

    def __repr__(self):
        return '<%s : similarity: %f>' % (self.__class__.__name__,
                                            self.similarity)

    def plot(self, error=False, _xlabel='', _ylabel='', _title=''):
        """Code from http://matplotlib.sourceforge.net/examples
            /pylab_examples/axes_demo.html"""
        from pylab import plot, xlabel, ylabel, title, show, legend
        makex = lambda y: [i*1.0/len(y) for i in range(len(y))]
        x1 = [i*1.0/len(self.score1) for i in range(len(self.score1))]
        y1 = sorted(self.score1)
        #y1 = self.score1
        plot(x1 ,y1, 'r', label=self.trace1.name or 'Trace1')
        x2 = [i*1.0/len(self.score2) for i in range(len(self.score2))]
        y2 = sorted(self.score2)
        #y2 = self.score2
        plot(x2 ,y2, 'b', label=self.trace2.name or 'Trace2')
        if error:
            plot(makex(self.error), self.error, 'g', label='Error')
        xlabel(_xlabel or self.xlabel)
        ylabel(_ylabel or self.ylabel)
        title(_title)
        legend(loc='upper left')
        show()

    def histogram(self, _xlabel='', _ylabel='', _title=''):
        #from pylab import plot, xlabel, ylabel, title, show
        import numpy as np
        import matplotlib.mlab as mlab
        import matplotlib.pyplot as plt

        y1 = self.score1
        y2 = self.score2
        n1, bins1, patches1 = plt.hist(np.array(y1), 50, normed=1,
            histtype='step', color='r')
        n2, bins2, patches2 = plt.hist(np.array(y2), 50, normed=1,
            histtype='step', color='b')
        #l = plt.plot(bins1)
        #l = plt.plot(bins2)
        plt.xlabel(_xlabel)
        plt.ylabel(_ylabel)
        plt.title(_title)
        plt.show()
    def print_statistics(self):
        from scipy import stats
        sz, (mn, mx), avg, var,skew, kurt = stats.describe(self.score1)
        s1_stats =  (sz, mn, mx, avg, var,skew, kurt)[:5]
        sz, (mn, mx), avg, var,skew, kurt = stats.describe(self.score2)
        s2_stats =  (sz, mn, mx, avg, var,skew, kurt)[:5]
        stat_string = ("\n\tTrace 1 \t Trace2\n" + '-'*40 + '\n' +
                       "Length \t %d \t\t %d \n" % (s1_stats[0], s2_stats[0]) +
                       "Min \t %f \t %f \n" % (s1_stats[1], s2_stats[1]) +
                       "Max \t %f \t %f \n" % (s1_stats[2], s2_stats[2]) +
                       "Average  %f \t %f \n" % (s1_stats[3], s2_stats[3]) +
                       "Variance %f \t %f \n" % (s1_stats[4], s2_stats[4]) )
        print stat_string

    def latex_row(self):
        """Creates a string formated as a LaTeX table row of relevant
        statistics. Called by dict_to_latex2"""
        sim = '%0.5f' % self.similarity
        if hasattr(self.error,'__iter__') :
            mx = max(self.error)
        else:
            mx = self.error

        avg_err = '%0.5f' % self.average_error if self.average_error!=None else '-'
        max_err = '%0.5f' % mx if mx != None else '-'
        p_err =  '%0.3f\%%' % (self.percent_error*100) if self.percent_error!=None else '-'

        
        s = (self.name + ' & ' + sim + ' & ' +  avg_err + ' & ' + max_err 
                + ' & ' + p_err + r' \\'+'\n'+r'\hline')
        return s

## Subclassed Metrics ----------------------------------------------------

class ByteThroughputMetric(Metric):
    name = "Byte Throughput"
    def compute_metric(self, trace):
        if len(trace.packets) > 1:
            total_byte_count = sum([len(pkt.data) for pkt in trace.packets])
            time = trace.packets[-1].timestamp -trace.packets[0].timestamp
            return total_byte_count / float(time)
        else:
            return 0 # There's not enough data to determine throughput for
                     # 0 or 1 packet.
    def compute_similarity(self):
        self.score1 = self.compute_metric(self.trace1)
        self.score2 = self.compute_metric(self.trace2)
        return self.scalar_similarity(self.score1, self.score2)

class PacketThroughputMetric(Metric):
    name = 'Packet Throughput'
    def compute_metric(self, trace):
        if len(trace.packets) > 1:
            time = trace.packets[-1].timestamp -trace.packets[0].timestamp
            return len(trace.packets) / float(time)
        else:
            return 0 # There's not enough data to determine throughput for
                     # 0 or 1 packets.
    def compute_similarity(self):
        self.score1 = self.compute_metric(self.trace1)
        self.score2 = self.compute_metric(self.trace2)
        return self.scalar_similarity(self.score1, self.score2)

class InterarrivalMetric(Metric):
    name = 'Interarrival Time'
    ylabel = 'Time (s)'
    def compute_metric(self, trace):
        delta_list = []
        for i in xrange(1,len(trace.packets)):
            delta = trace.packets[i].timestamp - trace.packets[i-1].timestamp
            delta_list.append(delta)
        return sorted(delta_list)
    def compute_similarity(self):
        self.score1 = self.compute_metric(self.trace1)
        self.score2 = self.compute_metric(self.trace2)
        self.error = self.diff_lists(self.score1, self.score2)
        return self.sorted_continuous_similarity(self.score1,self.score2)


class InterarrivalMetricMS(Metric):
    """Measures the time from Master sending a message to a slave responding.
       NOTE: Assumes Master request is the first packet of the trace.
       NOTE: Ignores sources, so this is not a per-source metric"""
    name = 'Master-Slave Interarrival Time'
    ylabel = 'Time (s)'
    def __init__(self, trace1, trace2, master1=None, master2=None):
        super( InterarrivalMetricMS, self).__init__(trace1, trace2,
            calc_similarity=False)
        self.master1 = master1 or trace1.packets[0].source
        self.master2 = master2 or trace2.packets[0].source
        self.similarity = self.compute_similarity()
        self.compute_error()
        self.xlabel = 'Normalized measurement number'

    def compute_metric(self, trace, master):
        delta_list = []
        i = 1 #points to a slave response record
        while i < len(trace.packets):
            #In the if statement, we make sure that packet @ i is a slave
            # and that packet at i-1 is also not a slave, otherwise we skip
            # ahead and try again
            if (trace.packets[i].source == master 
                or trace.packets[i-1].source != master):
                i += 1
            else:
                delta = trace.packets[i].timestamp - trace.packets[i-1].timestamp
                delta_list.append(delta)
                i += 2
        return sorted(delta_list)
    def compute_similarity(self):
        self.score1 = self.compute_metric(self.trace1, self.master1)
        self.score2 = self.compute_metric(self.trace2, self.master2)
        return self.sorted_continuous_similarity(self.score1,self.score2)

class InterarrivalMetricMSFC(Metric):
    """Measures the time from Master sending a message to a slave responding.
       NOTE: Assumes Master request is the first packet of the trace.
       NOTE: Ignores sources, so this is not a per-source metric"""
    ylabel = 'Time (s)'
    def __init__(self, trace1, trace2, master1=None, master2=None, fc = 0):
        super( InterarrivalMetricMSFC, self).__init__( trace1, trace2,
                calc_similarity=False)
        self.master1 = master1 or trace1.packets[0].source
        self.master2 = master2 or trace2.packets[0].source
        self.fc = fc
        self.similarity = self.compute_similarity()
        self.compute_error()
        self.xlabel = 'Normalized measurement number'

    def compute_metric(self, trace, master):
        packet_list = [pkt for pkt in trace.packets 
                            if pkt.data[1] == chr(self.fc)]
        delta_list = []
        delta_pairs = []
        i = 1 #points to a slave response record
        while i < len(packet_list):
            #In the if statement, we make sure that packet @ i is a slave
            # and that packet at i-1 is also not a slave, otherwise we skip
            # ahead and try again
            if (packet_list[i].source == master 
                or packet_list[i-1].source != master):
                i += 1
            else:
                delta = packet_list[i].timestamp - packet_list[i-1].timestamp
                delta_list.append(delta)
                delta_pairs.append((packet_list[i-1], packet_list[i]))
                i += 2
        return (delta_list)
    def compute_similarity(self):
        self.score1 = self.compute_metric(self.trace1, self.master1)
        self.score2 = self.compute_metric(self.trace2, self.master2)
        return self.sorted_continuous_similarity(self.score1,self.score2)

class InterarrivalMetricSM(Metric):
    """Measures the time from Slave sending a response to the next request.
       NOTE: Ignores sources, so this is not a per-source metric"""
    name = 'Slave-Master Interarrival Metric'
    ylabel = 'Time (s)'
    def __init__(self, trace1, trace2, master1=None, master2=None):
        super( InterarrivalMetricSM, self).__init__(trace1, trace2,
                calc_similarity=False)
        self.master1 = master1 or trace1.packets[0].source
        self.master2 = master2 or trace2.packets[0].source
        self.similarity = self.compute_similarity()
        self.compute_error()

    def compute_metric(self, trace, master):
        delta_list = []
        i = 1 #points to a slave response record
        while i+1 < len(trace.packets):
            #In the if statement, we make sure that packet @ i is a slave
            # and that packet at i+1 is also not a slave, otherwise we skip
            # ahead and try again
            if (trace.packets[i].source == master 
                or trace.packets[i+1].source != master):
                i += 1 #Try the next record
                continue
            else:
                delta = trace.packets[i+1].timestamp - trace.packets[i].timestamp 
                delta_list.append(delta)
                i += 2
        return sorted(delta_list)
    def compute_similarity(self):
        self.score1 = self.compute_metric(self.trace1, self.master1)
        self.score2 = self.compute_metric(self.trace2, self.master2)
        return self.sorted_continuous_similarity(self.score1,self.score2)

class InterarrivalMetricBySource(Metric):
    ylabel = 'Time (s)'
    def __init__(self, trace1, trace2, source1=None, source2=None, filter=None):
        """Creates an interarrival metric by source; 
            @param filter is an optional callable that takes a trace as an argument and
            returns a modified trace."""
        self.trace1 = filter(trace1) if filter else trace1
        self.trace2 = filter(trace2) if filter else trace2
        self.source1 = source1 or trace1.packets[0].source
        self.source2 = source2 or trace2.packets[0].source
        self.similarity = self.compute_similarity()
        self.compute_error() 
        self.xlabel = 'Normalized measurement number'

    def compute_metric(self, trace, source=None):
        packet_list = [pkt for pkt in trace.packets if pkt.source == source]
        delta_list = []
        for i in xrange(1,len(packet_list)):
            delta = packet_list[i].timestamp - packet_list[i-1].timestamp
            delta_list.append(delta)
        return sorted(delta_list)
    def compute_similarity(self):
        self.score1 = self.compute_metric(self.trace1,self.source1)
        self.score2 = self.compute_metric(self.trace2, self.source2)
        return self.sorted_continuous_similarity(self.score1,self.score2)

class PacketSizeMetric(Metric):
    name = 'Packet Size'
    def compute_metric(self, trace):
        length_list = []
        for pkt in trace.packets:
            length_list.append(len(pkt.data))
        return sorted(length_list)
    def compute_similarity(self):
        self.score1 = self.compute_metric(self.trace1)
        self.score2 = self.compute_metric(self.trace2)
        return self.sorted_continuous_similarity(self.score1,self.score2)

class FunctionCodeCountMetric(Metric):
    name = 'Function Code Count'
    def compute_metric(self, trace):
        fc_list = []
        #Extract all function codes (second data byte) from trace
        for pkt in trace.packets:
            fc_list.append(ord(pkt.data[1]))
        #Create histogram list of function codes
        fc_counts = [0]* (max(fc_list)+1) #list of fc counts indexed by fc
        for fc in fc_list:
            fc_counts[fc] += 1
        #Scale counts by total packet count
        for i, cnt in enumerate(fc_counts):
            fc_counts[i] = float(fc_counts[i])/len(trace.packets)
        return fc_counts
    def compute_similarity(self):
        self.score1 = self.compute_metric(self.trace1)
        self.score2 = self.compute_metric(self.trace2)
        #Make score lists the same size
        if len(self.score1) < len(self.score2):
            self.score1 += [0]*(len(self.score2) - len(self.score1))
        if len(self.score2) < len(self.score1):
            self.score2 += [0]*(len(self.score1) - len(self.score2))
        return self.discrete_similarity(self.score1,self.score2)

class ByteFrequencyMetric(Metric):
    name = 'Byte Frequency'
    ylabel = 'Normalized Count of Occurrences'
    xlabel = 'Byte value'
    def compute_metric(self, trace):
        byte_counts = [0]*(2**8)
        #Extract all bytes from trace and append to count
        for pkt in trace.packets:
            for byte in pkt.data:
                byte_num = ord(byte)
                byte_counts[byte_num] += 1
        #Scale counts by total number of bytes
        unscaled = byte_counts[:]
        byte_sum = float(sum(byte_counts))
        for i in range(2**8):
            byte_counts[i] = byte_counts[i]/byte_sum
        return byte_counts, unscaled
    def compute_similarity(self):
        self.score1, self.score1_unscaled = self.compute_metric(self.trace1)
        self.score2, self.score2_unscaled  = self.compute_metric(self.trace2)
        return self.discrete_similarity(self.score1,self.score2)
    def plot(self, _xlabel='', _ylabel='', _title=''):
        """Code from http://matplotlib.sourceforge.net/examples
            /pylab_examples/axes_demo.html"""
        from pylab import plot, xlabel, ylabel, title, show, legend
        x1 = range(len(self.score1))
        y1 = self.score1
        plot(x1 ,y1, 'r', label=self.trace1.name or 'Trace1')
        x2 = range(len(self.score1))
        y2 = self.score2
        plot(x2 ,y2, 'b', label=self.trace2.name or 'Trace2')
        xlabel(_xlabel or self.xlabel)
        ylabel(_ylabel or self.ylabel)
        title(_title)
        legend()
        show()

class InvalidCRCMetric(Metric):
    """Computes a similarity metric based on the number of incorrect CRCs are
        present in the data.
        NOTE: Assumes ModbusRTU; ASCII data uses an LRC, not a CRC."""
    name = 'Invalid CRC'
    def compute_metric(self, trace):
        import struct
        incorrect_crc_count = 0
        for pkt in trace.packets:
            pkt_crc, = struct.unpack('>H',pkt.data[-2:])
            correct_crc = modbus_utils.calculate_crc(pkt.data[:-2])
            if pkt_crc != correct_crc:
                incorrect_crc_count += 1
        percent_incorrect = incorrect_crc_count/float(len(trace.packets))
        return percent_incorrect
    
    def compute_similarity(self):
        self.score1 = self.compute_metric(self.trace1)
        self.score2 = self.compute_metric(self.trace2)
        return self.scalar_similarity(self.score1, self.score2)

class ErrorCountMetric(Metric):
    """Computes a similarity metric based on the number of Modbus error packets
    in a trace. """
    name = 'Error Count'
    def compute_metric(self, trace):
        import struct
        get_fc = lambda p: ord(p.data[1])
        error_count = 0
        for pkt in trace.packets:
            if get_fc(pkt) & 0x80:
                error_count += 1
        percent_error = error_count/float(len(trace.packets))
        return percent_error
    
    def compute_similarity(self):
        self.score1 = self.compute_metric(self.trace1)
        self.score2 = self.compute_metric(self.trace2)
        return self.scalar_similarity(self.score1, self.score2)

class DirectSequenceMetric(Metric):
    """Compute a similarity metric based on which function codes follow 
    other function codes.
    The algorithm is to create a dictionary with keys corresponding to all the 
    function codes in the trace, with the items being dictionaries. These
    second-order dictionaries are keyed by function code and the values are the
    counts of times the function code appeared after the first order key in the
    trace.
    As an example, the table {1:{1:0, 2:10, 3:5}, 2: {1:5, 2:0, 3:10},
    3:{1:0,2:10,3:5}} encodes that a packet with fc 1 is never followed by a
    packet with fc 1, but was followed 10 times by a packet with fc2 and 5 times
    with a packet with fc3.
    """
    def __init__(self, trace1, trace2, op=None):
        """Creates an interarrival metric by source; 
            @param op is a function that is run on each packet to produce a
            value, like a source or a function code"""
        
        super( DirectSequenceMetric, self).__init__(trace1, trace2,
                calc_similarity=False)
        self.op = op or (lambda p: p.data[1]) #get functioncode
        self.table1 = None
        self.table2 = None
        self.similarity = self.compute_similarity()
        self.compute_error()

    def compile_table(self, trace):
        ##Collect function codes and initialize the table
        function_code_set = set([self.op(pkt) for pkt in trace.packets])
        sequence_table = {}
        for fc in function_code_set:
            sequence_table[fc]=dict((fc2, 0) for fc2 in function_code_set)
            
        ## Populate the table
        index=0
        for index in range(len(trace.packets)-1):
            this_pkt = trace.packets[index]
            next_pkt = trace.packets[index+1]
            sequence_table[self.op(this_pkt)][self.op(next_pkt)] += 1

        ##Scale by number of packets:
        for d1 in sequence_table.values():
            for k,v in d1.items():
                d1[k] = float(v) / len(trace.packets)
        return sequence_table
                    
    def compute_similarity(self):
        self.table1 = self.compile_table(self.trace1)
        self.table2 = self.compile_table(self.trace2)
        
        fc_set =  sorted(set(self.table1.keys() + self.table2.keys()))

        self.scores_dict = {}
        for fc in fc_set: 
            list1 = [self.table1.get(fc,{}).get(fc2, 0) for fc2 in fc_set]
            list2 = [self.table2.get(fc,{}).get(fc2, 0)  for fc2 in fc_set]
            self.scores_dict[fc] = self.discrete_similarity(list1,list2)
        average = sum(self.scores_dict.values())/float(len(self.scores_dict))
        return average
        
class AnalyzerTest(unittest.TestCase):
    """NOTE: These unit tests are incomplete and unreliable"""
    def setUp(self):
        pass
    
    def testMSUCreation(self):
        trace = MSU_CSV_Trace('./test_trace.csv')
        self.assertTrue(len(trace.packets) == 2354)
        self.assertTrue(len(trace.header) == 143)

def dict_to_latex(dictionary):
    """ Helper method for report generation.
    @param Dictionary a dictionary of key:value pairs
    @returns A string containing LaTeX code for a table based on dictionary"""
    full = """\begin{tabular}{|r|l|}
  \hline
  7C0 & hexadecimal \\
  3700 & octal \\ \cline{2-2}
  11111000000 & binary \\
  \hline \hline
  1984 & decimal \\
  \hline
\end{tabular}
"""
     
    begin = [r'\begin{tabular}{|r|l|}',r'\hline']
    heading = 'Name & Similarity & Average Error & Maximum Error'
    end = [r'\end{tabular}']
    sorted_keys = sorted(dictionary.keys())
    middle = [ str(k) + ' & ' + str(dictionary[k]) + r' \\'+'\n' + r'\hline' 
                for k in sorted_keys]
    l = begin + middle +end
    table = '\n'.join(l)
    return table

def dict_to_latex2(metric_list):
    """Used for report generation"""
    begin = [r'\begin{tabular}{|r|l|l|l|l|}',r'\hline ']
    heading = ['Name & Similarity & Average Error & Maximum Error & ' +
                'Percent Error',r'\\ \hline']
    end = [r'\end{tabular}']
    metric_list = sorted(metric_list, key=lambda m: m.name)
    middle = [ m.latex_row() for m in metric_list ]
    table = '\n'.join(begin+heading+middle+end)
    return table

def main():
    def read_filter(trace):
        import copy
        trace = copy.deepcopy(trace)
        packet_list = trace.packets
        trace.packets = [pkt for pkt in trace.packets 
                            if pkt.data[1] == chr(03)]
        return trace
    def write_filter(trace):
        import copy
        trace = copy.deepcopy(trace)
        packet_list = trace.packets
        trace.packets = [pkt for pkt in trace.packets 
                            if pkt.data[1] == chr(0x10)]
        return trace

    from pprint import pprint
    #trace1 = MSU_CSV_Trace('traces/test_trace1.csv')
    #trace2 = MSU_CSV_Trace('traces/test_trace2.csv')
    #trace2 = MSU_CSV_Trace('traces/test_trace.csv')

    ##Latest vanilla traces
    #trace1 = MSU_CSV_Trace('traces/pipeline_lab/off.csv')
    #trace1 = MSU_CSV_Trace('traces/pipeline_lab/auto.csv')
    #trace2 = MSU_CSV_Trace('traces/pipeline_sim/off.csv')
    #trace2 = MSU_CSV_Trace('traces/pipeline_sim/auto.csv')
    #trace1 = MSU_CSV_Trace('traces/water_lab/off.csv', name='Laboratory System')
    trace1 = MSU_CSV_Trace('traces/water_lab/auto.csv', name='Laboratory System')
    #trace2 = MSU_CSV_Trace('traces/water_sim/off.nodelay.csv', 'Virtual System')
    #trace2 = MSU_CSV_Trace('traces/water_sim/baud_delay.off.csv', 'Virtual System')
    #trace2 = MSU_CSV_Trace('traces/water_sim/msdelay.off.csv', 'Virtual System')
    #trace2 = MSU_CSV_Trace('traces/water_sim/final.off.csv', 'Virtual System')
    trace2 = MSU_CSV_Trace('/tmp/auto', 'Virtual System')
    #trace2 = MSU_CSV_Trace('/tmp/off2')
    #trace2 = MSU_CSV_Trace('traces/water_sim/auto.csv', 'Virtual System')
    #trace2 = MSU_CSV_Trace('/tmp/off2', 'Virtual System')

    ##Radio Traces
    #trace1 =  MSU_CSV_Trace('traces/water_lab/radio/off.csv')
    #trace2 =  MSU_CSV_Trace('traces/water_sim/radio/off.combined')
    #trace1 =  MSU_CSV_Trace('traces/water_lab/radio/auto.csv')
    #trace2 =  MSU_CSV_Trace('traces/water_sim/radio/auto.combined')
    #trace1 =  MSU_CSV_Trace('traces/pipeline_lab/radio/auto.radio.csv')

    ##Mixed system traces
    #trace2 =  MSU_CSV_Trace('traces/pipeline_sim/lab_master_sim_slave_auto.csv')

    ##Attack Traces
    #trace1 = MSU_CSV_Trace('traces/water_lab/attacks/atk3.combined')
    #trace2 = MSU_CSV_Trace('traces/water_sim/attacks/atk3.combined')

    #tracea = MSU_CSV_Trace('traces/water_lab/attacks/atk3.master')
    #traceb = MSU_CSV_Trace('traces/water_lab/attacks/atk3.slave')
    #tracec = MSU_CSV_Trace('traces/water_sim/attacks/atk3.master')
    #traced = MSU_CSV_Trace('traces/water_sim/attacks/atk3.slave')
    #trace1 = Trace.combine_traces(tracea,traceb, '/dev/pts/6', '/dev/pts/11')
    #trace2 = Trace.combine_traces(tracec,traced, '/dev/pts/6', '/dev/pts/11')

    interarrival_metric = InterarrivalMetric(trace1, trace2)
    interarrival_metric_ms = InterarrivalMetricMS(trace1, trace2)
    interarrival_metric_sm = InterarrivalMetricSM(trace1, trace2)
    interarrival_metric_m = InterarrivalMetricBySource(trace1, trace2)
    interarrival_metric_m.name = 'Master-Master Interarrival Time'
    interarrival_metric_m_read = InterarrivalMetricBySource(trace1, trace2,
                                    filter=read_filter)
    interarrival_metric_m_read.name = 'Master-Master Interarrival Time (Read)'
    interarrival_metric_m_write = InterarrivalMetricBySource(trace1, trace2,
                                    filter=write_filter)
    interarrival_metric_m_write.name = 'Master-Master Interarrival Time (Write)'
    interarrival_metric_s = InterarrivalMetricBySource(trace1, trace2,
                            trace1.packets[1].source, trace2.packets[1].source)
    interarrival_metric_s.name = 'Slave-Slave Interarrival Time'
    byte_throughput_metric = ByteThroughputMetric(trace1, trace2)
    packet_throughput_metric = PacketThroughputMetric(trace1, trace2)
    packet_size_metric = PacketSizeMetric(trace1,trace2)
    fc_count_metric = FunctionCodeCountMetric(trace1,trace2)
    byte_frequency_metric = ByteFrequencyMetric(trace1, trace2)
    interarrival_metric_ms_read = InterarrivalMetricMSFC(trace1, trace2, fc=3)
    interarrival_metric_ms_read.name = 'Master-Slave Interarrival Metric (Read)'
    interarrival_metric_ms_write = InterarrivalMetricMSFC(trace1, trace2, fc= 0x10)
    interarrival_metric_ms_write.name = 'Master-Slave Interarrival Metric (Write)'
    invalid_crc_metric = InvalidCRCMetric(trace1, trace2)
    error_count_metric = ErrorCountMetric(trace1, trace2)
    fc_sequence_metric = DirectSequenceMetric(trace1, trace2)
    fc_sequence_metric.name = "Function Code Sequence (Length=2)"
    source_sequence_metric = DirectSequenceMetric(trace1, trace2, 
                                    op=lambda p: p.data[0])
    source_sequence_metric.name = "ID Sequence (Length=2)"

    #Interface stuff
    i = None
    m_list = [locals()[i] for i in locals() if 'metric' in i]
    metrics_dict = dict([(i,locals()[i].similarity) for i in locals()
                           if  'metric' in i])
    metrics_table = dict_to_latex(dict((v.name, v) for v in m_list))
    from numpy import array
    from pylab import plot, show, histogram

    print "Trace 1(red): \t", trace1.filename
    print "Trace 2(blue): \t", trace2.filename
    pprint(metrics_dict)
    from IPython.Shell import IPShellEmbed
    ipshell = IPShellEmbed( banner = """metrics available in metrics_dict""")
    ipshell() 

if __name__ == '__main__':
    main()
    #unittest.main()
