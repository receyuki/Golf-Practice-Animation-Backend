# -*- encoding:utf-8 -*-
__author__ = 'Zijie Yang'
__filename__ = 'data.py'
__copyright__ = 'Copyright 2020, '
__email__ = 'zijiey@student.unimelb.edu.au'

import json
import logging


class Data:

    def __init__(self):
        self.logger = logging.getLogger("server.Data")

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

