import bluetooth
import sys
import logging
from sh import bluetoothctl


# mbp A4:83:E7:E4:45:DE


class Transmitter:

    def __init__(self):
        self.logger = logging.getLogger("server.Transmitter")
        self.server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.client_sock = None
        self.address = None

    def connect(self):
        # turn on bluetooth
        bluetoothctl("power", "on")
        bluetoothctl("discoverable", "yes")
        self.logger.debug("Bluetooth on")

        # display near by device
        nearby_devices = bluetooth.discover_devices(lookup_names=True)
        self.logger.info("Found {} devices.".format(len(nearby_devices)))

        for addr, name in nearby_devices:
            if "-hidemac" in sys.argv:
                self.logger.info("  {} - {}".format("**:**:**:**:**:**", name))
                self.logger.debug([addr, name])
            else:
                self.logger.info("  {} - {}".format(addr, name))

        port = 1
        # establish connection
        self.server_sock.bind(("", port))
        self.server_sock.listen(1)
        self.logger.debug("Sock listening to port %i", port)
        self.logger.info("Waiting for in coming connection...")
        self.client_sock, self.address = self.server_sock.accept()
        if "-hidemac" in sys.argv:
            self.logger.info("Accepted connection from %s", ["**:**:**:**:**:**", self.address[1]])
            self.logger.debug(self.address)
        else:
            self.logger.info("Accepted connection from %s", self.address)

    def send(self, msg):
        try:
            self.client_sock.send(msg.encode("utf-8"))
            self.logger.debug("Send message [%s]", msg)
        except bluetooth.btcommon.BluetoothError as e:
            self.logger.warning(e)
            self.client_sock, self.address = self.server_sock.accept()

    def close(self):
        self.client_sock.close()
        self.server_sock.close()
        self.logger.info("Socket close")
