# -*- encoding:utf-8 -*-
import sys
import ascii
import logging
from transmitter import Transmitter

# create logger
logger = logging.getLogger("server")
logger.setLevel(logging.DEBUG)

formatter =logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# create file handler
fh = logging.FileHandler("server.log")
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)

# create console handler
ch = logging.StreamHandler()
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

link = Transmitter()

link.connect()

try:
    while True:
        msg = input("input message: ")
        link.send(msg)
except EOFError:
    pass

link.close()
