#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Qionghui Cai'

import math

# from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np


class Trajectory():

    def __init__(self, velocity, azimuthin, elevation):
        self.velocity = velocity
        self.azimuthin = azimuthin * math.pi / 180
        self.elevation = elevation * math.pi / 180

    def trajectoryPrediction(self, verticalScale=1):
        k = 0.5 * 0.5 * 1.293 * math.pi * np.square((0.04267 / 2)) * 0.35
        m = 0.046
        g = 9.8

        x0 = 0
        y0 = 0
        z0 = 0

        Vx0 = self.velocity * math.cos(self.elevation) * math.cos(self.azimuthin)
        Vy0 = self.velocity * math.cos(self.elevation) * math.sin(self.azimuthin)
        Vz0 = self.velocity * math.sin(self.elevation)

        trise = math.sqrt(m / (g * k)) * math.atan(math.sqrt(k / (m * g)) * Vz0)
        Zmax = -m / k * math.log(math.cos(math.atan(math.sqrt(k / (m * g)) * Vz0))) + z0
        tfall = math.sqrt(m / (k * g)) * math.log(
            (2 - math.exp(-k / m * Zmax) + 2 * math.sqrt(1 - math.exp(-k / m * Zmax))) / math.exp(-k * Zmax / m))
        tfly = trise + tfall

        t = np.arange(0, tfly, 0.01)
        x = []
        y = []

        for t_l in t:

            if Vx0 > 0:
                x_1 = m / k * math.log(1 + k * Vx0 * t_l / m) + x0
            else:
                x_1 = -m / k * math.log(1 - k * Vx0 * t_l / m) + x0
            x.append(x_1)

            if Vy0 > 0:
                y_1 = m / k * math.log(1 + k * Vy0 * t_l / m) + y0

            else:
                y_1 = -m / k * math.log(1 - k * Vy0 * t_l / m) + y0
            y.append(y_1)

        n1 = np.arange(0, trise, 0.01)

        z1 = []

        for t1 in n1:
            z_1 = -m / k * math.log(math.cos(math.atan(math.sqrt(k / (m * g)) * Vz0)) / (
                math.cos(math.atan(math.sqrt(k / (m * g)) * Vz0) - t1 * math.sqrt(g * k / m))))
            z1.append(z_1 * verticalScale)

        n2 = np.arange(trise + 0.01, tfly, 0.01)
        z2 = []

        for t2 in n2:
            z_2 = Zmax + m / k * math.log(4 * math.exp(math.sqrt(k * g / m) * (t2 - trise)) / np.square(
                (1 + math.exp(math.sqrt(k * g / m) * (t2 - trise)))))
            z2.append(z_2 * verticalScale)

        x_mp = 1.0936 * np.array(x)
        y_mp = 1.0936 * np.array(y)

        z_mp = 1.0936 * np.array(z1 + z2)

        max_x_mp = max(x_mp)
        max_y_mp = max(y_mp)
        carry = math.sqrt(np.square(max_x_mp) + np.square(max_y_mp))
        height = m / (2 * k) * np.square(math.log(1 + math.exp(2 * trise * math.sqrt(k * g / m)))) / (
                4 * math.exp(2 * trise * math.sqrt(k * g / m)))
        peak = height * 1.0936

        print("carry:%.2f" % carry)
        print("peak:%.2f" % peak)
        return carry, peak, x_mp, y_mp, z_mp

    def plot(self):
        fig = plt.figure(figsize=(12, 8))
        ax = fig.gca(projection='3d')
        ax.plot(x_mp, y_mp, z_mp)
        elev = 20
        azim = 220.5
        ax.view_init(elev, azim)
        ax.grid(False)

        plt.xlabel('x')
        plt.ylabel('y')
        plt.show()

# tra = Trajectory(111.7 * 1.609 * 0.278, -1.9, 19.4)
# tra.trajectoryPrediction()
