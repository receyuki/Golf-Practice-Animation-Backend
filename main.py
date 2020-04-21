import sys
import ascii
from transmitter import Transmitter

if "-doge" in sys.argv:
    print(ascii.ASCII_DOGE)
else:
    print(ascii.ASCII_TITLE)

link = Transmitter()

link.connect()

while True:
    msg = input("input message: ")
    link.send(msg)

link.close()
