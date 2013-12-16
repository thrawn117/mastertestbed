#!/usr/bin/env python
# vim: set tw=80:inoremap # X#
"""
Brad Reaves
Released under GPL2
April 2011

This module implements PortLogger objects and unit tests. PortLogger objects
create virtual serial port busses where each packet sent is logged to a file.
The idea is that a number of pseudoterminal devices are created. The slave ends
of the pty are provided as external ports for devices to connect to; the master
ends are kept internally and read. Data that is read from the master is logged
and then sent to all other pty devices.
"""

#built-in imports
#import pty
import os
from select import select
from threading import Thread
import unittest
from time import time, sleep
from optparse import OptionParser
from serial import Serial
import sys
from random import randint

#Local library imports

#External library imports

class PortLogger(Thread, object):
    """Port logger objects create two or more connected pseudoterminal devices 
        that are connected together; each write to any of the devices is logged.
        """
    BUF_LEN = 1024
    def __init__(self, number_of_ports=2, logfile=None, symlinks=None,
                    ports=None, baud=9600, force_symlinks=False, emulate=False,
                    rs485 = False):
        """ Creates the portLogger object. 
        self. masters and self.slaves hold file descriptors of corresponding
        master and slave sides of the pseudoterminals.
        @param numberOfPorts Number of pseudoterminals to create. Default is 2.
        @param logfile Name of the logfile. 
        @param symlinks Iterable of filenames to symlink the slaves to
        @param ports List of filenames of physical serial ports to connect&log 
        @param baud Baud rate for the links. If pty is used, a wait is used to
                    simulate transmission times.
        @param emulate Emulate a baud rate delay for communicating between
        @param rs485 RS-485 emulation. If true, the first pty is selected to 
                        broadcast to other
                        ports, and other ports only send responses to the first
                        pty. 
        pseudoterminal devices. Serial ports are unaffected.
        @param force_symlinks If true, if a file name given to
                            be created as a symlink is already a link, a new 
                            link will be forced in its place. If it exists and 
                            is not a link, the program will halt."""
        ##Set up baud rate delay for ptys
        self.baud = baud
        self.emulate = emulate
        self.byte_delay = (8.0+2.0)/baud if emulate else 0
                        #8data + 1startbit + 1stopbit / baud = seconds/byte

        ## Create Pseudoterminals
        self.masters = []
        self.slaves = []
        for _ in xrange(number_of_ports):
            master, slave = os.openpty() #master and slave are file descriptors
            self.masters.append(master)
            self.slaves.append(slave)
        
        ## Create symlinks to the slave ports before adding serial objects
        if symlinks:
            self.make_symlinks(symlinks, force_symlinks)

        ##Create serial objects
        self.serials = []
        for port in ports if ports else []:
            self.serials.append(Serial(port=port, baudrate=baud))
        self.serial_fds = [ser.fileno() for ser in self.serials]
        self.masters.extend(self.serial_fds)
        self.slaves.extend(self.serial_fds)

        #Map masters to slaves
        self.masters_to_slaves = dict(zip(self.masters, self.slaves))

        #Designate leader:
        #Leader and follower are used to distinguish the RS435 master and slave
        #   terms from the master/slave used in pty terminology.
        self.leader = self.masters[0]
        self.followers = [m for m in self.masters if m != self.leader]
        self.rs485_mode = rs485

        #self.done is a flag to stop the run() method 
        self.done = False

        ## Start logging
        if not logfile:
            logfile = '/tmp/'+str(time())+'.serialport.log'
        self.log = open(logfile, 'w+')
        self.start_log()
        
        Thread.__init__(self)

    def make_symlinks(self, symlinks, force_symlinks=False):
        """Creates symlinks from the names of the slave ptys to the targets
            in the iterable symlinks. This is useful to have constant names 
            for the ports created with the port logger. There is no guarantee
            that a given pty will be linked to a specific symlink.
            @param symlinks Iterable of filenames to symlink the slaves to.
            @param force_symlinks If true, if a file name given to
                            be created as a symlink is already a link, a new 
                            link will be forced in its place. If it exists and 
                            is not a link, the program will halt."""
        names_and_links = zip(self.port_names(), symlinks)
        for nm_ln in names_and_links:
            try:
                os.symlink(nm_ln[0], nm_ln[1])
            except OSError as oe:
                #New link name is already in use if errno is 17:
                if (os.path.islink(nm_ln[1]) and force_symlinks and oe.errno==17):
                    os.remove(nm_ln[1]) #delete old symlink
                    os.symlink(nm_ln[0], nm_ln[1]) #make new symlink
                else:
                    raise oe #This was not the error we were looking for

    def start_log(self):    
        """Writes a header to the log file"""
        self.log.write("Port Logger Log: Unix time: " + str(time()) +'\n')
        self.log.write("Ports in use: " + ' '.join(self.port_names()) +'\n' )
        self.log.write("Format : <Timestamp (Unix time)> : <port file name> " +
                        ": <packet> \n\n")
   
    def log_packet(self, port_fd, packet, timestamp = None):
        """Writes a packet entry to the log"""
        timestamp = '%.6f' % (timestamp or time())
        slave_name = os.ttyname(self.masters_to_slaves[port_fd])
        packet_string = '.'.join(["%02.x" % ord(ch) for ch in packet])
        log_string = " : ".join([timestamp, slave_name , packet_string]) 
        self.log.write(log_string + '\n')
        self.log.flush()

    def run(self):
        """ Function that executes when this thread is started.
            run() listens to on all pty objects and echoes incoming data
            to all other ports."""
        while not self.done:
            ports_to_read, _,_  = select(self.masters, [], [], .01)
            #print "BRDEBUG: After select() call: ports to read: ", ports_to_read
            for in_port in ports_to_read:
                #print "BRDEBUG: Port being read:", in_port
                #Read bytes from pty 
                data_in = os.read(in_port, self.BUF_LEN) 
                timestamp = time()
                
                if not self.rs485_mode:
                    out_ports = [m for m in self.masters if m != in_port]
                elif in_port == self.leader:
                    out_ports = self.followers
                elif in_port in self.followers:
                    out_ports = [self.leader]

                #Write bytes to serial ports:
                for out_port in out_ports:
                    if out_port in self.serial_fds:
                        os.write(out_port, data_in)
                #Simulate transmission delay if sender was a pty:
                if in_port not in self.serial_fds:
                    sleep(len(data_in)*self.byte_delay)
                #Write bytes to other ptys
                for out_port in out_ports:
                    if out_port not in self.serial_fds:
                        os.write(out_port, data_in)
                self.log_packet(in_port, data_in, timestamp)

    def stop(self):
        """Stops execution of the logger. The logger is closed and the 
            thread exits"""
        self.done = True
        sleep(.1) #Wait on the latest select() to finish and write out
        self.log.close()
        

    def port_names(self):
        """Returns a list of filenames of ports made available by this 
            object.
            @returns a list of filenames"""
        names = [ os.ttyname(fd) for fd in self.slaves]
        return names

class PortLoggerTest(unittest.TestCase):
    """Unit tests for the port logger class"""
    def testCreation(self):
        """testCreation: Creates several PortLogger classes"""
        l1 = PortLogger()
        self.assertEqual(len(l1.masters), 2)
        self.assertEqual(len(l1.slaves), 2)
        l3 = PortLogger(logfile='/tmp/logfile')
        for i in xrange(2, 10):
            l2 = PortLogger(number_of_ports=i)
            self.assertEqual(len(l2.masters), i)
            self.assertEqual(len(l2.slaves), i)

    def testSendAndReceive2Ports(self):
        """testSendAndReceive2Ports: Creates a PortLogger, serial objects that 
            connect to the PortLogger, and verifies that reads and writes work"""
        plogger= PortLogger()
        serials = []
        for port_name in plogger.port_names():
            new_serial = Serial(port_name)
            new_serial.timeout = 1
            serials.append(new_serial)

        plogger.start()

        message1 = "This is a test message"
        message2 = ''.join([chr(randint(32,127)) for _ in range(24)])
        serials[0].write(message1)
        recvd = serials[1].read(len(message1))
        self.assertEqual(message1, recvd)
        recvd = serials[0].read(len(message1))
        self.assertEqual('', recvd)
        

        serials[1].write(message2)
        recvd = serials[0].read(len(message2))
        self.assertEqual(message2, recvd)
        recvd = serials[1].read(len(message2))
        self.assertEqual('', recvd)
        
        plogger.stop()

    def testSendAndReceive2PortsLeader(self):
        """testSendAndReceive2PortsLeader: Creates a PortLogger, serial objects that 
            connect to the PortLogger, and verifies that reads and writes work.
            The portlogger uses the leader setup"""
        plogger= PortLogger(emulate=True, rs485=True )
        serials = []
        for port_name in plogger.port_names():
            new_serial = Serial(port_name)
            new_serial.timeout = 1
            serials.append(new_serial)

        plogger.start()

        message1 = "This is a test message"
        message2 = ''.join([chr(randint(32,127)) for _ in range(24)])
        serials[0].write(message1)
        recvd = serials[1].read(len(message1))
        self.assertEqual(message1, recvd)
        recvd = serials[0].read(len(message1))
        self.assertEqual('', recvd)
        

        serials[1].write(message2)
        recvd = serials[0].read(len(message2))
        self.assertEqual(message2, recvd)
        recvd = serials[1].read(len(message2))
        self.assertEqual('', recvd)
        
        plogger.stop()

    def testSendAndReceive4Ports(self):
        """testSendAndReceive4Ports: Creates a PortLogger, serial objects that 
            connect to the PortLogger, and verifies that reads and writes work"""
        plogger = PortLogger(number_of_ports=4)
        serials = []
        for port_name in plogger.port_names():
            new_serial = Serial(port_name)
            new_serial.timeout = 1
            serials.append(new_serial)

        plogger.start()
        for port in serials:
            message = ''.join([chr(randint(32,127)) for _ in range(24)])
            port.write(message)
            recvd = port.read(len(message))
            self.assertEqual('', recvd)
            for pt in [s for s in serials if s != port]:
                recvd = pt.read(len(message))
                self.assertEquals(recvd, message)
        plogger.stop()

    def testSendAndReceive4PortsLeader(self):
        """testSendAndReceive4Ports: Creates a PortLogger, serial objects that 
            connect to the PortLogger, and verifies that reads and writes work"""

        plogger = PortLogger(number_of_ports=4, rs485=True)
        serials = []
        for port_name in plogger.port_names():
            new_serial = Serial(port_name)
            new_serial.timeout = 1
            serials.append(new_serial)

        leader = serials[0]
        followers = serials[1:]

        self.assertEquals(len(followers), len(serials)-1)
        self.assertTrue(leader) #Check that leader is not None or []

        plogger.start()
        for port in followers:
            message = ''.join([chr(randint(32,127)) for _ in range(24)])
            port.write(message)
            for port2 in followers:
                recvd = port2.read(len(message))
                self.assertEqual('', recvd)
            recvd = leader.read(len(message))
            self.assertEquals(recvd, message)
        
        message = ''.join([chr(randint(32,127)) for _ in range(24)])
        leader.write(message)
        for port in followers:
            recvd = port.read(len(message))
            self.assertEquals(recvd, message)

        plogger.stop()
    

if __name__ == "__main__":
    programDescription = ( "This program creates virtual connected serial " +
                            "ports. Optional arguments point to symlinks " +
                            "that will be created for ports  if provided." )
    usage = """ %prog [options] /dir/to/symlink1 /dir/to/symlink2 ..."""
    parser = OptionParser(description=programDescription, usage=usage)
    parser.add_option('-t', '--unit_test', help="""Run the unit tests for this
        module""", action='store_true', default=False)
    parser.add_option('-s', '--symlink', dest='symlink', 
        help="""Name of a symlink to connect a pseudoterminal to""", 
        action='append')
    parser.add_option('-p', '--port', dest='port', 
        help="""Filename of a serial port to add to logger. If a port is
        specified, a baudrate must also be specified.""", 
        action='append')
    parser.add_option('-b', '--baud', dest='baud', 
        help="""Baudrate of the logger ports. If not specified,
        9600 is assumed.""", action='store', default =
        9600,type='int')
    parser.add_option('-e', '--emulate', dest='emulate', 
        help="""If specified, a delay is added between receiving and sending
        to/from a pty.""", action='store_true')
    parser.add_option('-r', '--rs485', dest='rs485', 
        help="""If used, the ports are set up in an RS485 master/multislave
        situation.""", action='store_true')
    parser.add_option('-n', '--num_ports', help="""Number of pseudoterminals to create.
        Default is 2.""", action='store', type='int', default = 2)
    parser.add_option('-l', '--logfile', help="""Name of file to write log
        to.""", action='store', default = None)
    parser.add_option('-f', '--force_symlinks', help="""If a file name given to
        be created as a symlink is already a link, a new link will be forced in its
        place. If it exists and is not a link, the program will halt.""", 
        action='store_true', default = False)

    #Get system and vdev name
    (opts, args) = parser.parse_args()
    if opts.unit_test:
        sys.argv = [''] #unittest.main() tries to interpret the cmd line opts
        unittest.main()
    else:
        port_logger = PortLogger(number_of_ports=opts.num_ports, 
                                 logfile=opts.logfile, symlinks=args,
                                 ports=opts.port, baud=opts.baud,
                                 force_symlinks=opts.force_symlinks,
                                 emulate=opts.emulate, rs485=opts.rs485)
        print "Ports created: ", ' '.join(port_logger.port_names())
        if opts.rs485:
            print "Master: ", os.ttyname(port_logger.leader)
        print "Logfile: ", port_logger.log.name
        port_logger.start()
        user_input = ''
        try: 
            while not 'quit' in user_input:
                user_input = raw_input('To close the port logger, type ' +
                                        '"quit<enter>":\n')
        except EOFError: #This happens if user gives <C-d>
            port_logger.stop()
        port_logger.stop()

##---------------Feature Requests --------------------
# -- Instead of just logging, implement a callback scheme so that implementing
#       bump-in-the-wire systems is easy        
# -- Instead of port numbers in the logs, it would be nice to register device 
#       names that are written to the logs
# -- Logging should be some sort of standard -- like Snoop
