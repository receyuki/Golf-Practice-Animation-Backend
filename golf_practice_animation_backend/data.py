# -*- encoding:utf-8 -*-
__author__ = 'Zijie Yang'
__filename__ = 'data.py'
__copyright__ = 'Copyright 2020, '
__email__ = 'zijiey@student.unimelb.edu.au'

import gzip
import json
import logging


class Data:

    def __init__(self):
        self.logger = logging.getLogger("server.Data")

    # encode with json format
    def encode(self, speed, launchAngle, sideAngle, carry, peak, x, y, z):
        trajectory = []
        self.logger.info("speed: " + str(speed))
        self.logger.info("launchAngle: " + str(launchAngle))
        self.logger.info("sideAngle: " + str(sideAngle))
        self.logger.info("carry: " + str(carry))
        self.logger.info("peak: " + str(peak))
        self.logger.info("trajectory: " + str(trajectory))

        for i in range(len(x)):
            trajectory.append({"x": x[i], "y": y[i], "z": z[i]})

        data = {"speed": speed,
                "launchAngle": launchAngle,
                "sideAngle": sideAngle,
                "carry": carry,
                "peak": peak,
                "trajectory": trajectory}

        self.logger.info("data: " + str(data))

        return json.dumps(data)

    # fragment data packet with 500 mtu
    def fragment(self, b, mtu=500):
        n = 0
        i = 0
        subString = bytearray()
        fragmented = []
        for c in b:
            subString.append(c)
            n += 1
            # fragmenting
            if n == mtu:
                header = bytearray("{0:03}".format(i).encode())
                header.extend(subString)
                fragmented.append(header)
                # print(bytearray("{0:03}".format(i).encode()))

                n = 0
                subString = bytearray()
                i += 1
        if subString:
            header = bytearray("{0:03}".format(i).encode())
            header.extend(subString)
            fragmented.append(header)

        # adding header to each fragment
        header = bytearray("{0:03}".format(i + 1).encode())
        # adding EOF to the last fragment
        header.extend("EOF".encode())
        fragmented.append(header)
        return fragmented

    # compression with gzip
    def compress(self, str):
        return gzip.compress(str.encode())
        # return str.encode()

    # test data reader
    def testData(self):
        with open('testData.json') as f:
            data = gzip.compress(str(json.load(f)).encode())
            # data = str(json.load(f)).encode()
        return data
