# -*- encoding:utf-8 -*-
__author__ = 'Zijie Yang'
__filename__ = 'main.py'
__copyright__ = 'Copyright 2020, '
__email__ = 'zijiey@student.unimelb.edu.au'

import sys
from golf_practice_animation_backend import ascii
import logging
from golf_practice_animation_backend.transmitter import Transmitter
from golf_practice_animation_backend.data import Data
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
    print(ascii.ASCII_TITLE)

# ADC driver
# class gpiozero.MCP3204(channel=0, differential=False, max_voltage=3.3, **spi_args)
#radar0 = MCP3204(channel=0, differential=False, max_voltage=3.3)
#radar1 = MCP3204(channel=1, differential=False, max_voltage=3.3)
#radar2 = MCP3204(channel=2, differential=False, max_voltage=3.3)
#radar3 = MCP3204(channel=3, differential=False, max_voltage=3.3)

#TODO test driver

link = Transmitter()

link.connect()

testdata = Data.encode(10,20,30,40,50,[1,2,3],[4,5,6],[7,8,9])

while True:
    msg = link.recv()
    print("received [%s]" % msg.decode('utf-8'))

#TODO bluetooth

"""
try:
    while True:
        msg = input("input message: ")
        link.send(msg)
except EOFError:
    pass

link.close()
"""
