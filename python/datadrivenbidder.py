import numpy as np
import os
import sys
import math
from scipy.optimize import curve_fit

def ortb1_win(x, c):
    return(x/(x+c))

def ortb2_win(x,c):
    return((x**2)/(x**2 + c**2))

class DD_ORTB1():
    def __init__(self):
        self.c    = None
        self.lamb = None
        pass

    def batch_fit(self, data):
        # data need to be in table format preferably or csv file
        # IsClick, paying price, pctr
        # preferably tuple list
        pp = sorted([x[1] for x in data]) #paying price
        de = [float(x) / (len(pp) + 1) for x in range(1, len(pp)+1)]
        popt, pcov = curve_fit(ortb1_win, pp, de)
        self.c = popt[0]
        # Fitting lambda
        # gs = [x * 1E-07 for x in range(1, 50)] # Greed Search for lambda parameter
        # TODO
        self.lamb = 5.2*1E-07

    def bidding(self, pctr):
        sq = math.sqrt(self.c * pctr/float(self.lamb) + self.c**2) - self.c
        return int(sq)

class DD_ORTB2():
    def __init__(self):
        self.c    = None
        self.lamb = None
        pass

    def batch_fit(self, data):
        # data need to be in table format preferably or csv file
        # IsClick, paying price, pctr
        # preferably tuple list
        pp = sorted([x[1] for x in data]) #paying price
        de = [float(x) / (len(pp) + 1) for x in range(1, len(pp)+1)]
        popt, pcov = curve_fit(ortb2_win, pp, de)
        self.c = popt[0]
        # TODO tune lambda
        self.lamb = 1E-06

    def bidding(self, pctr):
        s1 = (pctr + math.sqrt((self.c*self.lamb)**2 + pctr**2)) / (self.c * self.lamb)
        s2 = (self.c * self.lamb) / (pctr + math.sqrt((self.c*self.lamb)**2 + pctr**2))
        sq = self.c * (s1**(1./3) - s2**(1./3))
        
        return int(sq)





