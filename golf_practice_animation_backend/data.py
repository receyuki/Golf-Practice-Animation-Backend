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

    def encode(speed, launchAngle, sideAngle, carry, peak, x, y, z, self):
        trajectory = []
        self.logger.info("speed: " + speed)
        self.logger.info("launchAngle: " + launchAngle)
        self.logger.info("sideAngle: " + sideAngle)
        self.logger.info("carry: " + carry)
        self.logger.info("peak: " + peak)
        self.logger.info("trajectory: " + trajectory)

        for i in range(len(x)):
            trajectory.append({"x": x[i], "y": y[i], "z": z[i]})

        data = {"speed": speed,
                "launchAngle": launchAngle,
                "sideAngle": sideAngle,
                "carry": carry,
                "peak": peak,
                "trajectory": trajectory}

        self.logger.info("data: " + data)

        return json.dumps(data)
