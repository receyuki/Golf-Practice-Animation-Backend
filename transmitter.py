import bluetooth
from sh import bluetoothctl

# mbp A4:83:E7:E4:45:DE


class Transmitter:

    def __init__(self):
        self.server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.client_sock = None
        self.address = None

    def connect(self):
        bluetoothctl("power", "on")
        bluetoothctl("discoverable", "yes")

        nearby_devices = bluetooth.discover_devices(lookup_names=True)
        print("Found {} devices.".format(len(nearby_devices)))

        for addr, name in nearby_devices:
            print("  {} - {}".format(addr, name))

        port = 1
        self.server_sock.bind(("", port))
        self.server_sock.listen(1)
        print("Waiting for in coming connection...")
        self.client_sock, self.address = self.server_sock.accept()
        print("Accepted connection from ", self.address)

    def send(self, msg):
        try:
            self.client_sock.send(msg.encode("utf-8"))
        except bluetooth.btcommon.BluetoothError as e:
            print(e)
            self.client_sock, self.address = self.server_sock.accept()

    def close(self):
        self.client_sock.close()
        self.server_sock.close()
