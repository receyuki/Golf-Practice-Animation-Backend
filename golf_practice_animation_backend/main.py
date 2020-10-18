# -*- encoding:utf-8 -*-
__author__ = 'Zijie Yang'
__filename__ = 'main.py'
__copyright__ = 'Copyright 2020, '
__email__ = 'zijiey@student.unimelb.edu.au'

import sys
import ascii
import logging
import time
import dbus.mainloop.glib
import ctypes
import numpy as np

from gi.repository import GLib
from transmitter import Transmitter
from data import Data
from trajectorySimulation import Trajectory
from adcConverter import ADC
from gpiozero import MCP3204

# create logger
logger = logging.getLogger("server")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# create file handler
fh = logging.FileHandler("server.log")
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)

# create console handler
ch = logging.StreamHandler()

# parameters
if "-debug" in sys.argv:
    ch.setLevel(logging.DEBUG)
else:
    ch.setLevel(logging.INFO)

if "-nolog" not in sys.argv:
    logger.addHandler(fh)
logger.addHandler(ch)

logger.debug("Server running")
logger.debug("The arguments are: %s", sys.argv[1:])

if "-doge" in sys.argv:
    print(ascii.ASCII_DOGE)
else:
    # print(ascii.ASCII_TITLE)
    pass

# # initialize ctype
# dataReader = ctypes.CDLL('./dataReader.so')
# dataReader.detect.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.c_double, ctypes.c_double, ctypes.c_int]
# channel = 4
# size = 100
# dataType = ((ctypes.c_double * size) * channel)
# dataSet = np.zeros((100,4), dtype='double')
# dataSetC = dataSet.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
#
# # sampling
# if dataReader.detect(dataSetC, ctypes.c_double(100), ctypes.c_double(100), ctypes.c_int(size)) == 1:
#     print("Sampling success")
#
#
# print(dataSet)
#
# exit()

a1 = [1, 3, 2, 4, 5, 6, 8, 7]
a2 = [4, 5, 6, 8, 7, 9, 11, 10]
a3 = [1, 3, 2, 4, 5, 6, 8, 7]
a4 = [4, 5, 6, 8, 7, 9, 11, 10]
a1 = [element * 10 for element in a1]
a1 = [element * 10 for element in a1]
a1 = [element * 10 for element in a1]
a1 = [element * 10 for element in a1]

dataSet = np.random.randint(1024, size=(10, 4))

test = ADC(dataSet)
#[velocity, azimuthin, elevation] = test.convert()
(velocity, azimuthin, elevation) = test.convert()
exit()

data = Data()
# data.encode(10, 20, 30, 40, 50, [1, 2, 3], [4, 5, 6], [7, 8, 9])
# ts = data.fragment(data.testData())

speed = 111.7 * 1.609 * 0.278
sideAngle = -1.9
launchAngle = 19.4
verticalScale = 2

tra = Trajectory(speed, sideAngle, launchAngle)
(carry, peak, x, y, z) = tra.trajectoryPrediction(verticalScale)
traj = data.encode(speed, launchAngle, sideAngle, carry, peak, x, y, z)
trajt = data.fragment(data.compress(traj))

# print(ts)

mainloop = GLib.MainLoop()

link = Transmitter(mainloop)


def test():
    for e in trajt:
        print(e)
        link.send(e)
    return True


GLib.timeout_add(13000, test)

try:
    mainloop.run()
except KeyboardInterrupt:
    mainloop.quit()
