# -*- encoding:utf-8 -*-
__author__ = 'Zijie Yang'
__filename__ = 'driver.py'
__copyright__ = 'Copyright 2020, '
__email__ = 'zijiey@student.unimelb.edu.au'

# Modified from
# https://github.com/stevemarple/python-MCP342x/blob/master/MCP342x/examples/convert_and_read_many.py

import glob
import logging
import smbus
from MCP342x import MCP342x

def get_smbus():
    candidates = []
    prefix = '/dev/i2c-'
    for bus in glob.glob(prefix + '*'):
        try:
            n = int(bus.replace(prefix, ''))
            candidates.append(n)
        except:
            pass

    if len(candidates) == 1:
        return smbus.SMBus(candidates[0])
    elif len(candidates) == 0:
        raise Exception("Could not find an I2C bus")
    else:
        raise Exception("Multiple I2C busses found")


logging.basicConfig(level='DEBUG')

logger = logging.getLogger("server.Driver")

bus = get_smbus()

# Create objects for each signal to be sampled
addr68_ch0 = MCP342x(bus, 0x68, channel=0, resolution=18, continuous_mode=True, scale_factor=1.0)
addr68_ch1 = MCP342x(bus, 0x68, channel=1, resolution=18, continuous_mode=True, scale_factor=1.0)
addr68_ch2 = MCP342x(bus, 0x68, channel=2, resolution=18, continuous_mode=True, scale_factor=1.0)
addr68_ch3 = MCP342x(bus, 0x68, channel=3, resolution=18, continuous_mode=True, scale_factor=1.0)

addr69_ch0 = MCP342x(bus, 0x69, channel=0, resolution=18, continuous_mode=True, scale_factor=1.0)
addr69_ch1 = MCP342x(bus, 0x69, channel=1, resolution=18, continuous_mode=True, scale_factor=1.0)
addr69_ch2 = MCP342x(bus, 0x69, channel=2, resolution=18, continuous_mode=True, scale_factor=1.0)

# Create a list of all the objects. They will be sampled in this
# order, unless any later objects can be sampled can be moved earlier
# for simultaneous sampling.
adcs = [addr68_ch0, addr68_ch1, addr68_ch2, addr68_ch3,
        addr69_ch0, addr69_ch1, addr69_ch2]
r = MCP342x.convert_and_read_many(adcs, samples=2)
print('return values: ')
print(r)

# , scale_factor=2.448579823702253
addr68_ch0.convert()
print(addr68_ch3.convert_and_read())
