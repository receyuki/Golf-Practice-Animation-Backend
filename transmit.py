import sys

import bluetooth

#from bluetooth.ble import DiscoveryService

nearby_devices = bluetooth.discover_devices(lookup_names=True)
print("Found {} devices.".format(len(nearby_devices)))

for addr, name in nearby_devices:
    print("  {} - {}".format(addr, name))

# mbp A4:83:E7:E4:45:DE

bd_addr = "A4:83:E7:E4:45:DE"

port = 1

sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
sock.connect((bd_addr, port))

sock.send("hello!!")

sock.close()