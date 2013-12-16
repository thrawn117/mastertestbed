#!/usr/bin/env python
# vim: set tw=80:
"""
ascii2rtu.py
Brad Reaves
May 2011
License: GPLv2

This script reads a BR_MSU formated serial packet capture and can convert Modbus
ASCII data to Modbus RTU format. 

Import this file into an interpreter and use that way
"""

def ASCII2RTU(filename):
    separator = ' : '
    with open(filename+'.rtu','w+') as write_file:
        with open(filename, 'r') as read_file:
            header = ''.join([read_file.readline() for i in range(4)])
            for line in read_file:
                timestamp, source, data = line.split(separator)
                data = data.strip().split('.') #Remove newlines and split on bytes
                data = [chr(int(byte,16)) for byte in data]
                import string
                data = [i for i in data if i in string.hexdigits]
                data = '.'.join([data[i]+data[i+1] for i in range(0,len(data),2)])
                write_file.write(' : '.join([timestamp, source, data,])+'\n')

