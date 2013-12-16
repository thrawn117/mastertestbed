#!/usr/bin/env python

"""
@author Brad Reaves
March 2011
@version 0.1
License GPL2
"""

"""This module contains the Point class, some simple and likely common
    callbacks to be used when the point value is set, and unit tests for the 
    point class."""

import logging, unittest

class Point(object):
    """
        The point class maintains process information local to the virtual 
        device in an ICS protocol-independent manner. It maintains names for
        each point for each supported protocol, as well as notes whether a point
        is for internal use, an device input, or a device output.
        
        As an aside, "point" is an ICS term for a variable. Point names are
        protocol specific. Points may be inputs (like an analog or digital 
        port), outputs (also analog or digital), or internal variables used to
        store a state or a calculation. It is a common paradigm for devices to
        poll other devices for other devices' points.
     """


    #Static class constants for defining point types
    INTERNAL, INPUT, OUTPUT = range(3)

    def __init__(self, name, typ=0, value=0, metadata=dict(), **kwds ): 
        """Constructor for the point class
       """
        self.name = name #Internal name of the point as ref'd by the simulator
        self.typ = typ #Point type for simulation use
        self.default = value # Default initial value of the point
        self._value = value # Present value of this point. It will typically be a
                         # boolean or int, but it can be a string, a binary
                         # blob, or a file
        self.metadata = metadata # Dictionary keyed by protocol. 
                                 # Items are also dictionaries
                                 # of {metadata name:value}
        self.protocols = metadata.keys() # List of protocols this point is assigned to
                                        # If this point was used in Modbus and DNP3
                                        # Systems, this would be ['MODBUS', 'DNP3']
        self.set_callbacks = [] # List of functions called before setting the
                                # the new value of the point. Functions have
                                # are of the form f(self, new value) where self
                                # is the point object.

    def add_set_callback(self, f):
        """Adds a function to the list of callbacks run when the value changes.
            Such a call back may be useful for initiating external, logging, or
            debugging or for ensuring that values are maintained in an 
            appropriate range, like ensuring that an integer remains 
            within 16-bits. 

            Developers should be careful if more than one callback is
                registered that modifies the new value that the order of
                callbacks is appropriate and watch for unintended side effects.

            @param f a function of form f(point, newvalue) that returns a value
                to be stored as the value of the point. If a callback intends to
                do nothing to the point value, it should return newvalue.
            """
        self.set_callbacks.append(f)

    def set(self, val):
        """ Used to set the value of the point. Before assigning the new
            value val to the point, all the set callbacks registered with
            the point are called in the order that they are present in 
            the set_callbacks list.

            @param val the new point value
            """

        for f in self.set_callbacks:
            val=f(self, val)
        self._value = val

    def reset(self):
        self.set(self.default)
        pass

    def get(self):
        """This is a get function for the value of this point.
        @returns self.value"""
        return self._value


    def __str__(self):
        """String representation of a point.
            @returns a string giving the type, value, and names of the point"""
        return self.__repr__()
        tojoin= [ ('INTERNAL', 'INPUT', 'OUTPUT')[self.typ],
                    ' Point ', self.name, '. Value: ', str(self._value)]  
        return ''.join(tojoin)
    def __repr__(self):
        """Returns self.__str__()"""
        tojoin= [ '<',('INTERNAL', 'INPUT', 'OUTPUT')[self.typ],
                    ' Point ', self.name, '. Value: ', str(self._value), '>']  
        return ''.join(tojoin)

class PointCallbacks():
    """ This is a class that holds some common callbacks when points are set."""
    @staticmethod
    def printValue(pt, newvalue):
        """This callback prints a message to the console everytime the value 
            changes. 
            
            @returns The new value unchanged
            """
        print "Point %s changing from %d to %d" % (pt.name, pt.get(),pt.newvalue)
        return newvalue

    @staticmethod
    def ensure16Bit(pt, newvalue):
        """This callback ensures that the point value is a 16-bit value
            @returns newvalue and'ed with 0xfff
        """
        newvalue = newvalue & 0xffff
        return newvalue

    @staticmethod
    def double(pt, newvalue):
        """This callback doubles newvalue. This was a useful function for
        testing; it may not be good for much else.
        @returns newvalue*2 """

        newvalue *= 2
        return newvalue

class PointTest(unittest.TestCase):
    """@internal
        Unit tests of the point class"""
    
    def setUp(self):
        """Called at the start of the unittest"""
        self.meta1 = {'modbus': {'address':30000,
                                'type':'hr'
                               },
                     'dnp3' : {'group':1,
                               'variation': 3,
                               'index':1 
                              }
                    }
        self.meta2 = {'modbus': {'address':20000,
                                'type':'coil'
                               },
                     'dnp3' : {'group':2,
                               'variation': 1,
                               'index':1 
                              }
                    }
        self.cfg3 = {'name':'setpoint',  'typ':0, 'value':15, 
                    'metadata':{'modbus':{ 'addr':'30003', 'type':'hreg'},
                            'dnp3': {} } }
        self.pt1 = Point(name = 'pressure', typ = Point.INPUT, value = 10, 
                            metadata=self.meta1)
        self.pt2 = Point(name = 'pump', typ = Point.OUTPUT, value = 1, 
                                metadata=self.meta2)
        self.pt3 = Point(**self.cfg3)


    def testCreation(self):
        pt1 = Point(name = 'pressure', typ = Point.INPUT, value = 10, 
                            metadata=self.meta1)
        pt2 = Point(name = 'pump', typ = Point.OUTPUT, value = 1, 
                                metadata=self.meta2)
        pt3 = Point(**self.cfg3)
        
    def testGet(self):
        v1 = self.pt1.get()
        v2 = self.pt2.get()
        v3 = self.pt3.get()

        self.assertEqual(v1,10)
        self.assertEqual(v2,1)
        self.assertEqual(v3,15)
    
    def testSet(self):
        self.pt1.set(5)
        self.pt2.set(0)
        self.pt3.set(10)
        
        v1 = self.pt1.get()
        v2 = self.pt2.get()
        v3 = self.pt3.get()

        self.assertEqual(v1,5)
        self.assertEqual(v2,0)
        self.assertEqual(v3,10)

    def testReset(self):
        self.pt1.set(5)
        self.pt2.set(0)
        self.pt3.set(10)
        
        self.pt1.reset()
        self.pt2.reset()
        self.pt3.reset()

        self.assertEqual(self.pt1.get(),10)
        self.assertEqual(self.pt2.get(),1)
        self.assertEqual(self.pt3.get(),15)

    def testCallbacks(self):
        self.pt1.add_set_callback(PointCallbacks.double)
        self.pt1.set(0x657f)
        v=self.pt1.get()
        self.assertEqual(v,0xCAFE)

        self.pt1.add_set_callback(PointCallbacks.ensure16Bit)
        self.pt1.set(0xe57f)
        v=self.pt1.get()
        self.assertEqual(v,0xCAFE)

if __name__ == "__main__":
    unittest.main()
