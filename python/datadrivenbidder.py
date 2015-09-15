import numpy as np
import os
import sys
from scipy.optimize import curve_fit

class DD_ORTB1():
    def __init__(self):
        self.c    = None
        self.lamb = None
        pass

    def batch_fit(self, data):
        # data need to be in table format preferably or csv file
        # (bid, paying price)
        # preferably tuple list
        pp = sorted([x[1] for x in data]) #paying price
        de = [float(x) / (len(pp) + 1) for x in range(1, len(pp)+1)]

        popt, pcov = curve_fit(self.__wining_function, pp, de)
        print(popt)
        print(pcov)
        sys.exit(1)
        pass

    def bidding(pctr):
        pass

    def __wining_function(self, bid, c):
        return(float(bid)/(bid + c))


class DD_ORTB2():
    def __init__(self):
        self.c    = None
        self.lamb = None
        pass

    def batch_fit(self, data):
        # data need to be in table format preferably or csv file
        # bid, paying price
        # preferably tuple list
        pp = [x[1] for x in data] #paying price
        pass

    def bidding(pctr):
        pass

    def __wining_function(self, bid):
        return(float(bid**2)/(bid**2 + self.c**2))