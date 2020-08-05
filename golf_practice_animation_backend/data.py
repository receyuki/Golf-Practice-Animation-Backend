# -*- encoding:utf-8 -*-
__author__ = 'Zijie Yang'
__filename__ = 'data.py'
__copyright__ = 'Copyright 2020, '
__email__ = 'zijiey@student.unimelb.edu.au'

import json

class Data:

    def __init__(self):
        pass

    def encode(speed, launchAngle, sideAngle, carry, peak, x, y, z):
        trajectory = []

        for i in range(len(x)):
            trajectory.append({"x":x[i], "y":y[i], "z":z[i]})

        data = {"speed":speed,
                "launchAngle":launchAngle,
                "sideAngle":sideAngle,
                "carry":carry,
                "peak":peak,
                "trajectory":trajectory}

        return json.dumps(data)