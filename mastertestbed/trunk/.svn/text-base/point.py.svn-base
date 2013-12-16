#!/usr/bin/env python
# vim:tw=80
"""
@author Brad Reaves
March 2011
@version 0.1
License GPL2


This module contains the Point class, some simple and likely common
callbacks to be used when the point value is set, and unit tests for the 
point class."""

import logging, unittest, struct, types

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
        self._value = value # Present value of this point. It will typically be 
                         # a boolean or int, but it can be a string, a binary
                         # blob, or a file
        self.metadata = metadata # Dictionary keyed by protocol. 
                                 # Items are also dictionaries
                                 # of {metadata name:value}
        self.protocols = metadata.keys() # List of protocols this point is 
                                        # assigned to. If this point was used 
                                        # in Modbus and DNP3
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
        """Returns the point value to the default"""
        self.set(self.default)

    def get(self):
        """This is a get function for the value of this point.
        @returns self.value"""
        return self._value

    def __str__(self):
        """String representation of a point.
            @returns a string giving the type, value, and names of the point"""
        return self.__repr__()
    def __repr__(self):
        """Returns self.__str__()"""
        tojoin= [ '<',('INTERNAL', 'INPUT', 'OUTPUT')[self.typ],
                    ' Point ', self.name, '. Value: ', str(self._value), '>']  
        return ''.join(tojoin)

class PointView(object):
    """PointView objects are used when speciallized access to a point is needed.
        They were initially created to be contained in the slave registers of 
        the modbus interface."""
    def __init__(self, point, behavior='default'):
        """Constructor for the PointView class. Each point view can have a
        specified get/set behavior for implementing protocol-specific
        interfactes. For example, the behavior for a PointView  may be set to
        'lower_16bit' , which for float value types in points would treat this
        PointView as the bottom half of the point value; this would fit into a
        single 16-bit Modbus register.

        @param point The point that this view refers to.
        @oaran behavior The type of get and set methods to use.
        """        
        self._point = point
        self.behavior = behavior

    def get(self,*args, **kwds):
        return getattr(PointView, self.behavior+'_get')(self,*args, **kwds)

    def set(self,*args, **kwds):
        return getattr(PointView, self.behavior+'_set')(self,*args, **kwds)
    
    
    def reset(self):
        """Returns the point value to the default"""
        self._point.reset()

    def __str__(self):
        """String representation of a point.
            @returns repr(self)"""
        return self.__repr__()

    def __repr__(self):
        """String representation of a point.
            @returns a string giving the type, value, and names of the point"""
        tojoin= [ '<', 'PointView: ',('INTERNAL', 'INPUT',
            'OUTPUT')[self._point.typ], ' Point ', self._point.name, '. Value: ',
             str(self._point.get()), '>']  
        return ''.join(tojoin)

    def default_get(self):
        return self._point.get()

    def default_set(self,val):
        return self._point.set(val)

    def lower16bit_get(self):
        val = self._point.get()
        if isinstance(val, types.FloatType):
            upper_bytes = struct.pack('>f',val)
        else:
            upper_bytes = struct.pack('>i',val)#Assume some sort of int
        int_val = struct.unpack('>HH',upper_bytes)[1]
        return int_val
           
    def lower16bit_set(self, new_val):
        #Grab the bottom 16 bits of the new value
        if isinstance(new_val, types.FloatType):
            data_bytes = struct.pack('>f',new_val)
        else:
            data_bytes = struct.pack('>I',new_val) #Assume some sort of int
        new_bytes  = data_bytes[2:]

        #Get the upper bits of the old values
        old_val = self._point.get()
        if isinstance(old_val, types.FloatType):
            old_bytes = struct.pack('>f',old_val)[:2]
        else:
            old_bytes = struct.pack('>I',old_val)[:2] #Assume some sort of int

        final_format = '>f' if self.is_float(self._point) else '>I'
        val = struct.unpack(final_format,old_bytes+new_bytes)[0]
            
        #Set point to modified value        
        return self._point.set(val)

    def upper16bit_get(self):
        val = self._point.get()
        if isinstance(val, types.FloatType):
            upper_bytes = struct.pack('>f',val) 
        else:
            upper_bytes = struct.pack('>i',val) #Assume some sort of int
        int_val = struct.unpack('>HH',upper_bytes)[0]
        return int_val

    def upper16bit_set(self,new_val):
        """Used as an interface to the upper 16 bits of the point value.
        @param new_value Value to obtain the upper 16 bits of the point value
        from. If new_value is a float, the upper 16 bits of the float are used.
        If new_value is an integer, the LOWER 16 bits of the integer become the
        UPPER 16 bits of the point value. While counter-intuitive, this is to
        optimize the common case."""
        #Grab the top 16 bits of the new value (if float)
        if isinstance(new_val, types.FloatType):
            data_bytes = struct.pack('>f',new_val)
            new_bytes  = data_bytes[:2]
        else: #Assume some sort of int
            data_bytes = struct.pack('>I',new_val) 
            new_bytes = data_bytes[2:]

        #Get the lower bits of the old values
        old_val = self._point.get()
        if isinstance(old_val, types.FloatType):
            old_bytes = struct.pack('>f',old_val)[2:]
        else:
            old_bytes = struct.pack('>I',old_val)[2:] #Assume some sort of int

        final_format = '>f' if self.is_float(self._point) else '>I'
        val = struct.unpack(final_format, new_bytes + old_bytes)[0]
            
        #Set point to modified value        
        return self._point.set(val)
    
    @staticmethod
    def is_float(point):
        """ Used to determine if a point's datatype is a float or not
        @param point Point object to check
        @returns True if the parameter point has a datatype set
        """
        #@BUG: This breaks protocol independence!
        return ('datatype' in point.metadata['modbus'] 
            and point.metadata['modbus']['datatype'] == 'float')

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

class PointViewTest(unittest.TestCase):
    """@internal
        Unit tests of the PointView class"""
    
    def setUp(self):
        """Called at the start of the unittest"""
        self.meta1 = {'modbus': {'address':30000,
                                'type':'hr',
                                'datatype':'float'
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
        self.cfg3 = {'name':'setpoint',  'typ':0, 'value':15.0, 
                    'metadata':{'modbus':{ 'addr':'30003', 'type':'hreg'},
                            'dnp3': {} } }
        self.pt1 = Point(name = 'pressure', typ = Point.INPUT, value = 10.0, 
                            metadata=self.meta1)
        self.pt2 = Point(name = 'pump', typ = Point.OUTPUT, value = 1, 
                                metadata=self.meta2)
        self.pt3 = Point(**self.cfg3)
        
        self.pv1 = PointView(self.pt1) 
        self.pv1a = PointView(self.pt1, behavior='upper16bit') 
        self.pv1b = PointView(self.pt1, behavior='lower16bit') 
        self.pv2 = PointView(self.pt2) 
        self.pv3 = PointView(self.pt3) 

    def testCreation(self):
       pv1 = PointView(self.pt1) 
       pv1a = PointView(self.pt1, behavior='upper16bit') 
       pv1b = PointView(self.pt1, behavior='lower16bit') 
       pv2 = PointView(self.pt2) 
       pv3 = PointView(self.pt3) 
        
    def testGet(self):
        v1 = self.pv1.get()
        v1a = self.pv1a.get()
        v1b = self.pv1b.get()

        v2 = self.pv2.get()
        v3 = self.pv3.get()

        self.assertEqual(v1,10.0)
        self.assertEqual(v1a,0x4120)
        self.assertEqual(v1b,0)
        self.assertEqual(v2,1)
        self.assertEqual(v3,15.0)
    
    def testSimpleSet(self):
        self.pv1.set(243.33)
        self.pv2.set(0xcafe) 

        v1 = self.pv1.get()
        v1a = self.pv1a.get()
        v1b = self.pv1b.get()
        v2 = self.pv2.get()
        self.assertEqual(v1,243.33)
        self.assertEqual(v1a,0x4373)
        self.assertEqual(v1b,0x547B)
        self.assertEqual(v2,0xcafe)
        self.assertEqual(self.pt1.get(),243.33) 
        self.assertEqual(self.pv2.get(),0xcafe)
        
        self.testReset()

        pass
    def testSetPartialFloat(self):
        self.pv1.set(24.0)
        self.assertEqual(self.pt1.get(), 24.0)
        self.assertEqual(self.pv1.get(), 24.0)
        
        import pdb; pdb.set_trace()
        self.pv1b.set(0xa3d7)
        self.assertEqual(self.pt1.get(), 24.079999923706055)
        self.assertEqual(self.pv1.get(), 24.079999923706055)
        self.pv1a.set(0xcafe)
        self.assertEqual(self.pv1.get(), -8344043.5)
        self.assertEqual(self.pt1.get(), -8344043.5)

        self.testReset()

        self.pv1a.set(0xcafe)
        self.assertEqual(self.pt1.get(), -8323072.0) #Should be 0xcafe0000
        self.assertEqual(self.pv1.get(), -8323072.0)
        self.testReset()

        self.pv1b.set(0xcafe)
        self.assertEqual(self.pt1.get(), 10.049558639526367)#should be 0x4120CAFE
        self.assertEqual(self.pv1.get(), 10.049558639526367)
        self.testReset()

    def testSetPartialInt(self):
        self.pv1.set(0xdeadbeef)
        self.assertEqual(self.pt1.get(), 0xdeadbeef)
        self.assertEqual(self.pv1.get(), 0xdeadbeef)

        self.pv1a.set(0x1337cafe)
        self.assertEqual(self.pv1.get(),
                        struct.unpack('>f','\xca\xfe\xbe\xef')[0])
        self.assertEqual(self.pt1.get(),
                        struct.unpack('>f','\xca\xfe\xbe\xef')[0])

        self.pv1.set(0xdeadbeef)
        self.assertEqual(self.pt1.get(), 0xdeadbeef)
        self.assertEqual(self.pv1.get(), 0xdeadbeef)

        self.pv1b.set(0x1337cafe)
        self.assertEqual(self.pt1.get(), struct.unpack('>f','\xde\xad\xca\xfe')[0])
        self.assertEqual(self.pv1.get(), struct.unpack('>f','\xde\xad\xca\xfe')[0])
        self.testReset()

    def testChangePoint(self):
        self.pt1.set(17)
        self.assertEqual(self.pv1.get(), 17)
        self.assertEqual(self.pv1a.get(), 0)
        self.assertEqual(self.pv1b.get(), 17)
        
        self.pt1.set(10.049558639526367)
        self.assertEqual(self.pv1.get(), 10.049558639526367)
        self.assertEqual(self.pv1a.get(), 0x4120)
        self.assertEqual(self.pv1b.get(), 0xcafe)

    def testReset(self):
        self.pv1.reset()
        self.pv1a.reset()
        self.pv1b.reset()
        self.pv2.reset()
        self.pv3.reset()

        self.assertEqual(self.pv1.get(),10.0)
        self.assertEqual(self.pv1a.get(),0x4120)
        self.assertEqual(self.pv1b.get(),0)
        self.assertEqual(self.pv2.get(),1)
        self.assertEqual(self.pv3.get(),15.0)
        
    def testLargeValues(self):
        pass

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
                    'metadata':{'modbus':{ 'addr':'30003', 'type':'hreg',
                    'datatype':'float'},
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

