import numpy as np
import os
import sys
import math
from scipy.optimize import curve_fit

def ortb1_win(x, c):
    return(x/(x+c))

def ortb2_win(x,c):
    ans = [x1*x1/(x1*x1 + c*c) for x1 in x]
    return(np.array(ans))

class DD_ORTB1():
    def __init__(self, c = None, lamb = None):
        self.c    = c
        self.lamb = lamb

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

    def getC(self):
        return(self.c)

class DD_ORTB2():
    def __init__(self, c = None, lamb = None):
        self.c    = c
        self.lamb = lamb
        pass

    def batch_fit(self, data):
        # data need to be in table format preferably or csv file
        # IsClick, paying price, pctr
        # preferably tuple list
        pp = sorted([x[1] for x in data]) #paying price
        de = [float(x) / (len(pp) + 1) for x in range(1, len(pp)+1)]
        popt, pcov = curve_fit(ortb2_win, pp, de)
	print(popt)
	print(pcov)
        self.c = popt[0]
        # TODO tune lambda
        self.lamb = 1E-06

    def bidding(self, pctr):
        s1 = (pctr + math.sqrt((self.c*self.lamb)**2 + pctr**2)) / (self.c * self.lamb)
        s2 = (self.c * self.lamb) / (pctr + math.sqrt((self.c*self.lamb)**2 + pctr**2))
        sq = self.c * (s1**(1./3) - s2**(1./3))
        
        return int(sq)

class const_bidder():
    def __init__(self, constbid = None):
        self.constbid = constbid

    def fit(self, data):
        # Optional function: you can specify exact parameter using constbid
        # data is list of (isclick, pay_price, ...)
        contstant_pars = range(5, 300, 10)
        best_par       = None
        best_score     = 0
        sum_cost       = sum[x[1] for x in data]
        budget         = sum_cost * 1. / 32
        simulator      = train_rtb_simulator()
        for par in contstant_pars:
            self.constbid  = par 
            score          = simulator.simulate(budge, self, data)
            if score > best_score:
                best_score = score
                best_par   = par

        self.constbid   = best_par
        self.best_score = best_score

    def bidding(self, pctr):
        if self.constbid == None:
            print("Constant Bid not Specified.")
            sys.exit(1)
        return(self.constbid)

class train_rtb_simulator():
    def __init__(self):
        pass

    def simulate(self, budget, strategy, data):
        # data - list of (click, cost, pctr) #Warning can overfit!11
        sum_goal = 0
        spend    = 0.
        for d in data:
            if spend > budget:
                break
            if strategy.bidding(d[2]) > d[1]:
                sum_goal += d[0]
                spend    += d[1]

        return(sum_goal)



