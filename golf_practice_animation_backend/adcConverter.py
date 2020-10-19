#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Qionghui Cai'

import numpy as np
import math


class ADC:

    def __init__(self, dataSet):

        self.binary_list = dataSet
        self.array1 = []
        self.array2 = []
        self.array3 = []
        self.array4 = []

    def bin2Int(self):

        for elem in self.binary_list:
            self.array1.append(elem[0] / 1024 * 3.3)
            self.array2.append(elem[1] / 1024 * 3.3)
            self.array3.append(elem[2] / 1024 * 3.3)
            self.array4.append(elem[3] / 1024 * 3.3)

        print(self.array1)
        print(self.array2)
        print(self.array3)
        print(self.array4)
        # for data1 in self.binary_list1:
        #     self.array1.append(data1/1024*3.3)
        #
        # for data2 in self.binary_list2:
        #     self.array2.append(data2/1024*3.3)
        #
        # for data3 in self.binary_list3:
        #     self.array3.append(data3/1024*3.3)
        #
        # for data4 in self.binary_list4:
        #     self.array4.append(data4/1024*3.3)

    def phaseDifference(self):
        l1 = len(self.array1)
        l2 = len(self.array2)
        l3 = len(self.array3)
        l4 = len(self.array4)
        self.peak1 = []
        self.peak2 = []
        self.peak3 = []
        self.peak4 = []

        for i in range(1, l1 - 1):
            if self.array1[i - 1] < self.array1[i] and self.array1[i] > self.array1[i + 1]:
                self.peak1.append(i)
        count1 = len(self.peak1)

        for j in range(1, l2 - 1):
            if self.array2[j - 1] < self.array2[j] and self.array2[j] > self.array2[j + 1]:
                self.peak2.append(j)
        count2 = len(self.peak2)

        for m in range(1, l3 - 1):
            if self.array3[m - 1] < self.array3[m] and self.array3[m] > self.array3[m + 1]:
                self.peak3.append(m)
        count3 = len(self.peak3)

        for n in range(1, l4 - 1):
            if self.array4[n - 1] < self.array4[n] and self.array4[n] > self.array4[n + 1]:
                self.peak4.append(n)
        count4 = len(self.peak4)

        # fs = 200000
        fs = 100000000000
        T1 = (self.peak1[1] - self.peak1[0]) * (1 / fs)
        T2 = (self.peak2[1] - self.peak2[0]) * (1 / fs)
        T3 = (self.peak3[1] - self.peak3[0]) * (1 / fs)
        T4 = (self.peak4[1] - self.peak4[0]) * (1 / fs)
        self.f1 = 1 / T1
        print(self.f1)
        self.Phase_azimuthin = (abs(self.peak1[0] - self.peak2[0]) / fs / T1) * 2 * math.pi
        self.Phase_elevation = (abs(self.peak3[0] - self.peak4[0]) / fs / T3) * 2 * math.pi

    def initialValue(self):
        c = 3 * 10 ** 8
        d = 0.00775
        ft = 10.525 * 10 ** 9
        fs = 200000
        wavelength = c / ft
        fd = self.f1 - ft
        velocity = wavelength * fd / 2
        azimuthin = math.asin(wavelength * self.Phase_azimuthin / (2 * math.pi * d))
        elevation = math.asin(wavelength * self.Phase_elevation / (2 * math.pi * d))

        print("velocity:%.2f" % velocity)
        print("azimuthin:%.2f" % azimuthin)
        print("elevation:%.2f" % elevation)
        return velocity, azimuthin, elevation

    def convert(self):
        self.bin2Int()
        self.phaseDifference()
        return self.initialValue()


# a1 = [1, 3, 2, 4, 5, 6, 8, 7]
# a2 = [4, 5, 6, 8, 7, 9, 11, 10]
# a3 = [1, 3, 2, 4, 5, 6, 8, 7]
# a4 = [4, 5, 6, 8, 7, 9, 11, 10]
#
# test = ADC([b'0000', b'0011', b'0010', b'0100', b'0101', b'0110', b'1000', b'0111'],
#            [b'0100', b'0101', b'0110', b'1000', b'0111', b'1001', b'1011', b'1010'],
#            [b'0000', b'0011', b'0010', b'0100', b'0101', b'0110', b'1000', b'0111'],
#            [b'0100', b'0101', b'0110', b'1000', b'0111', b'1001', b'1011', b'1010'])
# test.bin2Int()
# test.phaseDifference()
# test.initialValue()
